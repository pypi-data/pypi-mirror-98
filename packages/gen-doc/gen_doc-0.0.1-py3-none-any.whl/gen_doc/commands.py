"""
Module with commands command line for run from console
as system command
"""
# pylint: disable=broad-except,unused-variable
import argparse
import inspect
import sys
import traceback
from typing import Dict

import gen_doc.extensions as extensions


def get_extensions() -> Dict:
    """
    Method build dict existed extensions for doc generator
    :return: dict[short_name: doc_generator
    """
    _val = dict()
    for _, clazz in inspect.getmembers(extensions,
                                                inspect.isclass):
        if _val.get(clazz.short_name):
            raise ValueError('not unique command')
        _val[clazz.short_name] = clazz
    return _val


dict_val = get_extensions()


class BuildDocumentation:
    """
    class for handling system commane
    """

    def __init__(self, argv):
        self.argv = argv
        self.parser = self.init_arg_parse()

    @staticmethod
    def init_arg_parse():
        """
        method for init all commands
        :return: parser
        """
        parser = argparse.ArgumentParser('Documentation builder')
        parser.add_argument('lang',
                            help='for which language to create documentation',
                            choices=dict_val.keys()
                            )
        parser.add_argument('-p', '--path_to_root_folder',
                            required=False, default='./',
                            help='path to the directory for which documentation should be compiled')
        parser.add_argument('-r', '--repository_main_url',
                            required=False,
                            help='url of the repository where this project is located')
        parser.add_argument('-t', '--title',
                            required=False,
                            default='',
                            help='title for header (if `-hi False`)')
        parser.add_argument('-p2s', '--path_to_save',
                            required=False,
                            help='path to the directory where to save'
                            )
        parser.add_argument('-f2s', '--file_to_save',
                            required=False,
                            help='name_file to save (if `-hi False`)')
        parser.add_argument('-hi', '--extract_with_same_hierarchy',
                            required=False, default=True,
                            help='if False extract all to one file if True'
                                 ' create file for every file')
        parser.add_argument('-o', '--overwrite_if_file_exists',
                            required=False, default=False,
                            help='for overwriting if file exist')

        return parser

    def execute(self):
        """
        main method for execute options
        :return:
        """
        res = self.parser.parse_args()
        print(res)
        data = {
            key: getattr(res, key)
            for key in dir(res) if key[0] != '_' and key != 'lang'
        }
        builder = dict_val[res.lang](**data)
        builder.build_documentation()


def main() -> None:
    """
    Main method for run in console
    :return:
    """
    try:
        builder = BuildDocumentation(sys.argv)
        builder.execute()
    except SystemExit:
        pass
    except Exception as exc:
        traceback.print_exc()


if __name__ == '__main__':
    main()
