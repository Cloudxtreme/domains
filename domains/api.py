from __future__ import print_function

from os import environ
from traceback import format_exc
from operator import attrgetter, itemgetter, methodcaller


from six import u

from libcloud.dns.providers import get_driver


from .utils import preprocess


class Domains(object):

    def __init__(self, config):
        self.config = config

        self._drivercache = {}

    def _driver(self, name, key=None):
        key = key or environ.get("{0}_ACCESS_TOKEN".format(name.upper()))
        return self._drivercache.get(name, get_driver(name)(key))

    def _status(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        zones = driver.list_zones()

        if domain in map(attrgetter("domain"), zones):
            zone = driver.get_zone(domain)
            records = [record for record in zone.list_records() if record.type != "NS"]
            remote = sorted(map(attrgetter("name"), records))
            local = sorted(map(itemgetter("name"), self.config[domain]["records"]))
            status = "M" if local != remote else " "
        else:
            status = "?"

        return status, domain

    def _create(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        records = self.config[domain]["records"]

        zone = driver.create_zone(domain=domain)
        map(methodcaller("delete"), zone.list_records())

        for record in records:
            if record["type"] == "MX":
                extra = {"priority": record["priority"]}
            else:
                extra = {}
            zone.create_record(
                name=record["name"], type=record["type"],
                data=record["data"], extra=extra,
            )

    def _delete(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        zone = driver.get_zone(domain)
        zone.delete()

    def _update(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        zone = driver.get_zone(domain)

        remote = dict(
            (record.name, record)
            for record in zone.list_records()
            if record.type != "NS"
        )

        local = dict(
            (record["name"], record)
            for record in self.config[domain]["records"]
        )

        for k, v in local.items():
            if k not in remote:
                extra = {"priority": v["priority"]} if v["type"] == "MX" else {}
                zone.create_record(
                    name=v["name"], type=v["type"],
                    data=v["data"], extra=extra,
                )
            else:
                if remote[k].data == "@" and v["data"] == "{0}.".format(domain):
                    continue
                if remote[k].data != v["data"]:
                    extra = {"priority": v["priority"]} if v["type"] == "MX" else {}
                    remote[k].update(data=v["data"], extra=extra)

        for k, v in remote.items():
            if k not in local:
                v.delete()

    def _view(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        zones = driver.list_zones()
        domains = map(attrgetter("domain"), zones)

        if domain not in domains:
            return u("404 Not Found: {0}".format(domain))

        zone = driver.get_zone(domain)

        return zone.export_to_bind_format()

    def delete(self, domains=None):
        domains = domains or self.config.keys()
        for domain in domains:
            try:
                print("Deleting domain: {0} ... ".format(domain), end="")
                self._delete(domain)
                print("OK")
            except Exception as e:
                print("ERR\nERROR: {0}\n{1}".format(e, format_exc()))

    def list(self):
        print("\n".join(self.config.keys()))

    def sync(self, context=None):
        preprocess(self.config, context)

        domains = self.config.keys()
        for status, domain in map(self._status, domains):
            if status == " ":
                return

            if status == "?":
                action, f = ("Creating", self._create)
            else:
                action, f = ("Updating", self._update)

            print("{0} domain: {1} ... ".format(action, domain), end="")

            try:
                f(domain)
                print("OK")
            except Exception as e:
                print("ERR\nERROR: {0}\n{1}".format(e, format_exc()))

    def status(self, context=None):
        preprocess(self.config, context)

        domains = self.config.keys()

        for status, domain in map(self._status, domains):
            print("{0:<8} {1}".format(status, domain))

    def view(self, domain):
        print(self._view(domain))
