import os.path
import yaml

class Config:
    def __init__(self, org_name, file_path):
        self.org = org_name
        self.__file_path = file_path

        self.__data = {}
        self.__read_config(org_name)

    def get(self, name, default=None):
        value = self.__data

        parts = name.split(':')
        for part_name in parts:
            value = value.get(part_name, default)

        return value

    # parts - list of config setting names - will be joined to form a path
    # final path will be expanded
    def path(self, *parts):
        data = []
        # resolve each config setting name
        for p in parts:
            data.append(self.get(p, p))

        path = os.path.join(*data)
        return os.path.expanduser(path)

    def __read_config(self, org_name):
        config_data = {}
        with open(self.__file_path, "r") as fh:
            config_data = yaml.full_load(fh)

        if org_name:
            self.__data = config_data.get(org_name)
            if not self.__data:
                raise Exception("No data found for organization '%s'" % (org_name))
        else:
            raise Exception("Organization Name Missing. Please set PLEBEIANS_ORG.")
