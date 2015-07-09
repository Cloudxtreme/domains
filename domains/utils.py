"""Utilities"""


from jinja2 import Template


def process(domain, record):
    for k, v in record.items():
        t = Template(v)
        record[k] = t.render(domain=domain)


def preprocess(config):
    for domain, data in config.items():
        for i, record in enumerate(data["records"]):
            process(domain, record)
