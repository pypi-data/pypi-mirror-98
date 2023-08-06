import csv
import json
from jsondatahelper import clean_for_storage as standardize
from lxml import etree as ET

UNKNOWN_FILE_EXTENSION = "unknown"


class File:
    def __init__(self, file_string, path, handler_reference):
        self.file_string = file_string
        self.name, self.ext = self.check_for_file_extention(file_string)
        self.path = str(path) + "/" + file_string
        self.handler_reference = handler_reference
        self.handler_reference.add_file(self)
        self.associations = {}

    def check_for_file_extention(self, file_string):
        try:
            name, ext = file_string.split(".")
        except ValueError:
            name, ext = file_string.split("."), UNKNOWN_FILE_EXTENSION
        return name, ext

    def get_association_names(self):
        return self.associations.keys()

    def write(self, data):
        ext = self.ext.lower()
        if ext == "json":
            if data:
                with open(self.path, "w+", encoding="utf-8") as f:
                    json.dump(
                        standardize(data), f, ensure_ascii=True, indent=4,
                    )
        else:
            print("Can't write to that file format!")

    def read(self):
        ext = self.ext.lower()
        if ext == "json":
            with open(self.path, "r+") as file_contents:
                try:
                    result = json.load(file_contents)
                    return convert_bytes(result)
                except json.decoder.JSONDecodeError:
                    print(
                        "There was a decoding error for file:",
                        self.path,
                        "please double check the syntax!",
                    )
                    return None

        elif ext == "csv":
            return CsvFile(file=self).to_dict()

        elif ext == "xml":
            return ET.parse(self.path).getroot()

        return None

    def update(self, new_data):
        if self.ext.lower() == "json":
            with open(self.path, "r+") as f:
                f.seek(0)  # rewind
                json.dump(
                    standardize(new_data), f, ensure_ascii=True, indent=4,
                )
                f.truncate()

    def associate(self, association_name, association):
        self.associations[association_name] = association

    def to_json(self, output_dir):

        if self.associations:
            new_json_name = output_dir + "/" + self.name + ".json"
            association_collection = {}

            for association_name, dictionary in self.associations.items():
                association_collection[association_name] = dictionary

            with open(new_json_name, "w", encoding="utf-8") as f:
                json.dump(association_collection, f, ensure_ascii=False, indent=2)
        else:
            print("No associations have been made with that file yet!")

    def __repr__(self):
        return self.path


class CsvFile:
    def __init__(self, file):
        self.__build(file)
        self.get_rows()

    def __build(self, file):
        if isinstance(file, str):
            self.__build_by_path(file)
        else:
            self.__build_by_file_obj(file)

    def __build_by_path(self, file_path):
        self.file_string = file_path.split("/")[-1]
        self.name, self.ext = self.file_string.split(".")
        self.path = file_path
        # self.starting_row = starting_row

    def __build_by_file_obj(self, file):
        self.file_string = file.file_string
        self.name = file.name
        self.ext = file.ext
        self.path = file.path

        # self.starting_row = starting_row

    def get_rows(self):
        self.rows = []
        with open(self.path, "r", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                self.rows.append(row)

    def to_dict(self):

        self.as_dict = {}
        if len(self.rows) > 0:
            headers = self.rows[0]
            for i, header in enumerate(headers):
                if header:
                    self.as_dict[header] = []
                    for j, row in enumerate(self.rows):
                        if j > 0:
                            try:
                                self.as_dict[header].append(row[i])
                            except IndexError:
                                pass

        return self.as_dict


def convert_bytes(loaded_json):
    for key, val in loaded_json.items():
        if isinstance(val, dict):
            loaded_json[key] = convert_bytes(val)
        elif isinstance(val, list):
            for index, item in enumerate(val):
                if isinstance(item, dict):
                    loaded_json[key][index] = convert_bytes(item)
                elif isinstance(item, str) and item.startswith("b'"):
                    loaded_json[key][index] = bytes.fromhex(item.split("b'")[1])
        elif isinstance(val, str) and val.startswith("b'"):
            loaded_json[key] = bytes.fromhex(val.split("b'")[1])

    return loaded_json
