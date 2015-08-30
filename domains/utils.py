"""Utilities"""


from jinja2 import Template


def process(domain, record, context=None):
    context = context or {}
    context["domain"] = domain

    for k, v in record.items():
        if isinstance(v, (str, unicode,)):
            t = Template(v)
            record[k] = t.render(**context)


def preprocess(config, context=None):
    for domain, data in config.items():
        for i, record in enumerate(data["records"]):
            process(domain, record, context=context)
