import os
from os.path import isdir, isfile, join
from file import File

class Directory:
    def __init__(self, path, index, level, handler_reference):
        self.children = []
        self.path = path
        self.index = index
        self.level = level
        self.handler_reference = handler_reference
        self.name = path.split("/")[-1]
        self.files = self.gather_files()
        self.parent = self.get_parent_folder_name()
        self.gather_children_folders()
        self.dict_rep = {
            "Name": self.name,
            "Files": self.files,
            "Parent": self.parent,
            "Children": self.children,
        }

    def gather_files(self):
        self.files = [
            File(f, self.path, self.handler_reference)
            for f in os.listdir(self.path)
            if isfile(join(self.path, f))
        ]
        return self.files

    def gather_children_folders(self):
        self.children = [f for f in os.listdir(self.path) if isdir(join(self.path, f))]
        # self.children_folder_objs = [
        #     self.handler_reference.find_folder_by_name(obj) for obj in self.children
        # ]

    def get_parent_folder_name(self):
        return self.path.replace("/" + self.name, "").split("/")[-1]

    def find_folder_by_name(self, folder_name):
        for folder in self.children:
            if folder_name in folder:
                return folder
        return None

    def find_file_by_name(self, file_name):
        for file in self.files:
            if file.name == file_name:
                return file
        print("File of name:", file_name, "not found in folder:", self.name)
        return None

    def find_files_by_ext(self, extention):
        found_files = []
        for file in self.files:
            if file.ext == extention:
                found_files.append(file)
        return found_files

    def __repr__(self):
        s = ""
        for key, val in self.dict_rep.items():
            s = s + key + "\n"
            if isinstance(val, list):
                for item in val:
                    s = s + str(item) + "\n"
            else:
                s = s + val + "\n"
        return s
