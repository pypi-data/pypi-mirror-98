import json
import os
import shutil
from collections import OrderedDict
from os.path import isdir, isfile
from src.directory import Directory

UNKNOWN_FILE_EXTENSION = "unknown"
DEF_DIR_FILTERS = [
    "__pycache__",
    "vscode",
    "py",
    "ds_store",
    ".DS_Store",
    ".git",
    ".idea",
]


class DirectoryHandler:
    def __init__(
        self, file_exts=[], ext_filters=DEF_DIR_FILTERS, directory_path=os.getcwd()
    ):
        self.recognized_file_exts = file_exts
        self.extention_filters = ext_filters
        self.has_applied_exts = file_exts
        self.root_path = directory_path
        self.scan(directory_path)

    def scan(self, directory_path=os.getcwd()):
        """
        Refresh & Update governed directories and folders.
        """
        self.organized_files = OrderedDict()
        self.folder_list = []
        self.filter_cwd(directory_path)
        self.init_directory_objects()
        self.compile_file_list()
        return self

    def compile_file_list(self):
        self.file_list = []
        for file_set in self.organized_files.values():
            for file in file_set:
                self.file_list.append(file)

    def __repr__(self):
        s = ""
        for key, val in self.organized_files.items():
            if not key == UNKNOWN_FILE_EXTENSION:
                s = s + str(key).upper() + "\n"
                for item in val:
                    s = s + "-->" + str(item) + "\n"
        return s

    def passes_filter(self, path):
        """
        Utility function used to filter out un-wanted/un-needed folders.
        """
        for filter_name in self.extention_filters:
            filter_name = filter_name.upper()
            path = path.upper()
            if filter_name in path or (filter_name in path.split("/")):
                return False
        return True

    def filter_cwd(self, cwd):
        """
        Gathers all directories, and sub-directories.
        Filters out non-important directories.
        """
        self.master_dir_list = []
        self.levels = []

        for path in [directory[0] for directory in os.walk(cwd)]:
            if self.passes_filter(path):
                level = path.count("/")
                if not level == 0:  # If the line is not empty
                    self.levels.append(level)
                    self.master_dir_list.append(path)

    def init_directory_objects(self):
        self.folder_list = []
        for dir_idx, path in enumerate(self.master_dir_list):
            self.folder_list.append(
                Directory(path, dir_idx, self.levels[dir_idx], self)
            )

    def add_file(self, file):
        """
        Adds file to master list.
        Called in file class when file is found.
        """
        if self.has_applied_exts != []:
            if file.ext and file.ext in self.recognized_file_exts:
                self.verify_extension(file.ext)
                self.organized_files[file.ext].append(file)

            elif not file.ext in self.extention_filters:
                self.verify_extension(UNKNOWN_FILE_EXTENSION)
                self.organized_files[UNKNOWN_FILE_EXTENSION].append(file)
        else:
            if self.passes_filter(file.path):
                self.verify_extension(file.ext)
                self.organized_files[file.ext].append(file)

    def verify_extension(self, extension):
        """
        Adds file extension to recognized extensions.
        """
        try:
            self.organized_files[extension]
        except KeyError:
            self.organized_files[extension] = []

    def get_files_by_ext(self, extension):
        """
        Returns all files of given file extension.
        """
        try:
            return self.organized_files[extension]
        except KeyError:
            print("That file extention does not exist!")
            return None

    def make_directory(self, path=None, name=None):
        created = False
        if path:
            if not self.exists(path):
                os.makedirs(path)
                created = True
        elif name:
            path = self.root_path + "/" + name
            if not self.exists(path):
                os.makedirs(path)
                created = True
        if created:
            self.scan()

    def make_file(self, file_name, insertion_path=None, data=None):

        if insertion_path:
            path = insertion_path
        else:
            path = self.root_path

        file_path = path + "/" + file_name

        if file_name.split(".")[1] == "json":
            with open(file_path, "w+", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            f = open(file_path, "w")
            f.write(str(data))
            f.close()

        self.scan()

        return self.find_files_by_name(file_name, return_first_found=True)

    def exists(self, path):
        if not isdir(path) and not isfile(path):
            return False
        return True

    def rmtree(self, directory):
        try:
            shutil.rmtree(directory)
        except FileNotFoundError as e:
            print(e)

    def delete_file(self, file_obj):
        if not isinstance(file_obj, str):
            # ext = file_obj.ext
            file_obj = file_obj.path

        try:
            os.remove(file_obj)
            self.scan()

        except FileNotFoundError as e:
            print(e)

    def find_files_by_name(self, file_name_to_find, return_first_found=False):
        found_files = []
        if file_name_to_find:
            split_file_name = file_name_to_find.split(".")
            if len(split_file_name) == 2:
                name = split_file_name[0]
                ext = split_file_name[1]
                for file in self.get_files_by_ext(ext):
                    if file.name == name:
                        if return_first_found:
                            return file
                        found_files.append(file)

            elif len(split_file_name) > 2:

                for file_list in self.organized_files.values():
                    for file in file_list:
                        if file.file_string == file_name_to_find and file:
                            if return_first_found:
                                return file.path
                            found_files.append(file)

            else:
                for file_list in self.organized_files.values():
                    for file in file_list:
                        if file.name == file_name_to_find:
                            if return_first_found:
                                return file
                            found_files.append(file)

        return found_files

    def find_file_by_path(self, path_to_find):
        for file_list in self.organized_files.values():
            for file in file_list:
                if file.path == path_to_find:
                    return file

    def find_file_in(self, folder_name, file_name):
        return self.find_folder_by_name(
            folder_name, return_first_found=True
        ).find_file_by_name(file_name)

    def find_folder_by_name(self, folder_name, return_first_found=True):
        found_folders = []

        for folder in self.folder_list:
            if folder.name.lower() == folder_name.lower():
                if return_first_found:
                    return folder
                else:
                    found_folders.append(folder)
        return found_folders

    def find_dir_via_path(self, folder_sub_path):
        for folder in self.folder_list:
            if folder_sub_path in folder.path:
                return folder

    def get_all_files_in(self, sub_path):
        self.scan()
        found_files = []
        for file_set in self.organized_files.values():  # All File Types
            for file in file_set:
                if sub_path in file.path:
                    found_files.append(file)
        return found_files

    def read_file(self, file_name, file_extention="json"):
        for file in self.organized_files[file_extention]:
            if file_name in file.name:
                return file.read()
        return None


if __name__ == "__main__":
    pass
