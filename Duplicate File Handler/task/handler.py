import os
import argparse
import hashlib


class FileHandler:
    def __init__(self, directory):
        self.directory = directory
        self.file_format = None
        self.sorting_option = None
        self.files_dict = dict()
        self.dict_items = None
        self.numbered_dict = dict()
        self.get_format()
        self.get_sorting_option()
        self.walk_dir()
        self.list_same_sized_files()
        self.check_duplicates()
        self.delete_files()

    def get_format(self):
        self.file_format = input("Enter file format:\n")

    def get_sorting_option(self):
        print("Size sorting options:")
        print("1. Descending")
        print("2. Ascending\n")
        while True:
            self.sorting_option = int(input("Enter a sorting option:\n"))
            print()
            if self.sorting_option not in (1, 2):
                print("\nWrong option\n")
            else:
                break

    def walk_dir(self):
        for root, directories, filenames in os.walk(self.directory):
            for file in filenames:
                if self.file_format != "":
                    if self.file_format != os.path.splitext(file)[-1].split(".")[-1]:
                        continue
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                if file_size in self.files_dict.keys():
                    self.files_dict[file_size].append(file_path)
                else:
                    self.files_dict[file_size] = [file_path]

    def list_same_sized_files(self):
        if self.sorting_option == 1:
            dict_items = list(reversed(sorted(self.files_dict.items())))
        elif self.sorting_option == 2:
            dict_items = sorted(self.files_dict.items())

        for size, files in dict_items:
            print(f"{size} bytes")
            for file in files:
                print(file)
            print()

        self.dict_items = dict_items

    def check_duplicates(self):
        while True:
            answer = input("Check for duplicates?\n")
            if answer not in ("yes", "no"):
                continue
            else:
                break

        if answer == "no":
            return
        else:
            n_duplicate = 1
            for size, files in self.dict_items:
                print(f"\n{size} bytes")
                hash_dict = dict()
                for file in files:
                    hash_maker = hashlib.md5()

                    with open(file, "rb") as f:
                        hash_maker.update(f.read())
                    if hash_maker.hexdigest() not in hash_dict.keys():
                        hash_dict[hash_maker.hexdigest()] = [file]
                    else:
                        hash_dict[hash_maker.hexdigest()].append(file)

                for key, values in hash_dict.items():
                    if len(values) > 1:
                        print(f"Hash: {key}")
                        for value in values:
                            print(f"{n_duplicate}. {value}")
                            self.numbered_dict[n_duplicate] = value
                            n_duplicate += 1

    def delete_files(self):
        while True:
            answer = input("Delete files?\n")
            if answer not in ("yes", "no"):
                continue
            else:
                break

        if answer == "no":
            return
        else:
            while True:
                answer = input("Enter file numbers to delete:\n")
                try:
                    files_to_delete = list(map(int, answer.split()))
                    if len(files_to_delete) == 0:
                        raise ValueError
                    if any(n not in self.numbered_dict.keys() for n in files_to_delete):
                        raise ValueError
                    break
                except ValueError:
                    print("\nWrong format\n")

            freed_space = 0
            for file in files_to_delete:
                freed_space += os.path.getsize(self.numbered_dict[file])
                os.remove(self.numbered_dict[file])
            print(f"Total freed up space: {freed_space} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory").required = False
    args = parser.parse_args()
    if args.directory is None:
        print("Directory is not specified")
    file_handler = FileHandler(args.directory)
