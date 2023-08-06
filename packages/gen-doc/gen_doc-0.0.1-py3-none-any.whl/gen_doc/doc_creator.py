"""
Main Class DocGenerator
"""
# pylint: disable=too-many-arguments
import os
from abc import ABC, abstractmethod
from distutils import util
from pathlib import Path
from typing import Union, List


class DocGenerator(ABC):
    """
    Abstract class for build documentation by doc strings
    """

    @property
    def short_name(self):
        """
        Property for short name in commands
        :return: str short name
        :example:
        >>> short_name = 'py'  # for python
        """
        raise NotImplementedError

    # type of documents for which to create documentation
    @property
    def types_of_file_to_process(self):
        """
        Property for concrete language
        :return: List[str] is list of string types to build docs
        :example:
            >>> types_of_file_to_process = ['.py']  # for python
        """
        raise NotImplementedError

    @property
    def files_to_ignore(self):
        """
        Which files names will not be considered
        :return: List[str]
        :example:
            >>> files_to_ignore = ['setup.py'] # for python
        """
        raise NotImplementedError

    @property
    def folders_to_ignore(self):
        """
        Which folder names will not be considered
        :return: List[str]
        :example:
            >>> folders_to_ignore = ['__pycache__'] # for python
        """
        raise NotImplementedError

    @property
    def type_to_save(self):
        """
        In what type to save the file with documentation
        :example:
            >>> type_to_save = 'MD'
        """
        raise NotImplementedError

    def __init__(self,
                 path_to_root_folder: Union[str, Path] = './',
                 repository_main_url: str = None,
                 title: str = '',
                 extract_with_same_hierarchy: bool = True,
                 overwrite_if_file_exists: bool = False,
                 path_to_save: Path = None,
                 file_to_save: str = None,
                 ):
        """

        :param path_to_root_folder:
        """
        # folder data
        if isinstance(path_to_root_folder, str):
            path_to_root_folder = Path(path_to_root_folder)
        if path_to_root_folder.name == '':
            path_to_root_folder = Path(f'..{os.sep}' + path_to_root_folder.absolute().name)
        self.directory = path_to_root_folder

        # repository
        self.repository = repository_main_url

        # title
        self.title = title

        self.extract_with_same_hierarchy = extract_with_same_hierarchy

        self.path_to_save = path_to_save
        if not self.path_to_save:
            self.path_to_save = Path(self.directory.name + '_doc')
        self.overwrite_if_file_exists = overwrite_if_file_exists
        self.file_to_save = file_to_save
        if not self.file_to_save:
            self.file_to_save = self.directory.name + self.type_to_save \
                if '.' in self.type_to_save \
                else '.' + self.type_to_save
        if '.' not in self.file_to_save:
            self.file_to_save += self.type_to_save \
                if '.' in self.type_to_save \
                else '.' + self.type_to_save
        if not isinstance(self.extract_with_same_hierarchy, bool):
            self.extract_with_same_hierarchy = bool(util.strtobool(
                self.extract_with_same_hierarchy))

        if not isinstance(self.overwrite_if_file_exists, bool):
            self.overwrite_if_file_exists = bool(util.strtobool(
                self.overwrite_if_file_exists))

    def build_documentation(self):
        """

        :return:
        """
        list_documentation_data = list()

        self.directory = Path(str(self.directory))

        list_folders_with_files_to_parse = [
            (dir_path, file_names)
            for (dir_path, dir_names, file_names) in os.walk(self.directory)
            if file_names
        ]
        for folder_path, list_files in list_folders_with_files_to_parse:
            folder = Path(folder_path)
            if not self.extract_with_same_hierarchy:
                deep = len(str(folder)[len(str(self.directory)):].split(os.sep))
            else:
                deep = 1
            if folder.name in self.folders_to_ignore:
                continue
            for file in list_files:
                if file in self.files_to_ignore:
                    continue
                file = Path(file)
                if file.suffix not in self.types_of_file_to_process:
                    continue
                list_documentation_rows = self.build_documentation_file(folder / file,
                                                                        deep=deep)
                if list_folders_with_files_to_parse:
                    list_documentation_data.append({
                        'path': folder / file,
                        'file_data': list_documentation_rows
                    })

        if self.extract_with_same_hierarchy:
            for data_file in list_documentation_data:
                tmp = Path(str(data_file['path'])[len(str(self.directory)):])
                tmp_path = Path(str(self.path_to_save) + str(tmp))
                os.makedirs(tmp_path.parent, exist_ok=True)
                file = tmp_path.stem + self.type_to_save if '.' in self.type_to_save \
                    else '.' + self.type_to_save
                self._save_documentation(Path(tmp_path.parent)
                                         / Path(file), data_file['file_data'], title=file)

        else:
            one_documentation = [
                row
                for data_documentation in list_documentation_data
                for row in data_documentation['file_data']
            ]
            self._save_documentation(Path(self.path_to_save)
                                     / Path(self.file_to_save), one_documentation)

    def _save_documentation(self,
                            path_to_save: Path,
                            data_to_save: List[str],
                            title=None) -> None:
        """
        Method for save documentation to file
        Method save if `data_to_save` not empty
        and file not exist and `overwrite_if_file_exists` is False
        :param Path path_to_save: path where you want to save the file
        :param List[] data_to_save : list docs strings
        :param str title: header page
        """
        if not title:
            title = self.title
        # if empty docs to write don't create docs
        if not data_to_save:
            return
        # check exist file or not
        if os.path.isfile(path_to_save):
            if not self.overwrite_if_file_exists:
                print(f'File {path_to_save} exist and is not overwritten')
                return

        # data_to_save.insert(0, f'# {title}')
        with open(path_to_save, 'w', encoding='utf-8') as file:
            file.write('\n\n'.join(data_to_save))

    @abstractmethod
    def build_documentation_file(self, path_to_file: Path, deep: int = 1) -> List[str]:
        """Method to overwriting in sub class for concrete ProgramLanguage
        :param Path path_to_file: file for which build documentation
        :param int optional int deep: at what nesting level is the file
        :return: list[str] docs
        """
        raise NotImplementedError
