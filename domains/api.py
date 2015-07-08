from __future__ import print_function


class Domains(object):

    def __init__(self, config):
        self.config = config

    def list(self):
        print("list")

    def sync(self):
        print("sync")

    def status(self):
        print("status")
