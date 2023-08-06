import os

from employee_info import load_data


class TestData:
    def __init__(self):
        folder = os.path.dirname(__file__)
        self.file = os.path.join(folder, '', 'stamdata_multi.xml')

    @staticmethod
    def load_functions():
        load_data.load_functions()

    def load_organisations(self):
        load_org = load_data.LoadOrganisations(self.file, 'AK')
        load_org.load()

    def load_resources(self):
        load_resources = load_data.LoadResources(self.file, 'AK')
        load_resources.load()

    def load_test_data(self):
        self.load_functions()
        self.load_organisations()
        self.load_resources()
