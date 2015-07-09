from __future__ import print_function

from os import environ
from traceback import format_exc
from itertools import izip_longest
from operator import attrgetter, itemgetter


from libcloud.dns.providers import get_driver


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
            import pudb; pudb.set_trace()
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
        for record in records:
            zone.create_record(name=record["name"], type=record["type"], data=record["data"])

    def _delete(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        zone = driver.get_zone(domain)
        zone.delete()

    def _update(self, domain):
        driver = self._driver(self.config[domain]["driver"])

        zone = driver.get_zone(domain)

        records = [record for record in zone.list_records() if record.type != "NS"]
        remote = sorted(records, key=attrgetter("name"))
        local = sorted(self.config[domain]["records"], key=itemgetter("name"))

        for x, y in izip_longest(local, remote):
            if y is None:
                zone.create_record(name=x["name"], type=x["type"], data=x["data"])

    def delete(self, domain):
        print("Deleting domain: {0} ... ".format(domain), end="")

        try:
            self._delete(domain)
            print("OK")
        except Exception as e:
            print("ERR\nERROR: {0}\n{1}".format(e, format_exc()))

    def list(self):
        print("\n".join(self.config.keys()))

    def sync(self):
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

    def status(self):
        domains = self.config.keys()
        for status, domain in map(self._status, domains):
            print("{0:<8} {1}".format(status, domain))
