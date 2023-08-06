"""
Generator documentation for python language
"""
# pylint: disable=no-else-return,too-many-return-statements
from __future__ import annotations

import ast
from ast import stmt
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional

from ..doc_creator import DocGenerator
from ..serializers import PythonDocSerializer

arguments_to_ignore = [
    'self'
]


class  PythonDocGenerator(DocGenerator):
    """
    Class for retrieving information about python module
    """
    short_name = 'py'
    types_of_file_to_process = [
        '.py'
    ]
    folders_to_ignore = [
        '__pycache__',
        '.git'
    ]
    files_to_ignore = [
        'setup.py'
    ]
    type_to_save = '.MD'

    def _parse_obj(self, obj: stmt) -> Tuple[Any, Any]:
        """
        Method for defining the handler object
        the method contains all objects for analysis
        :param stmt obj: object to process if exist handler
        :return: type, info
        """
        if isinstance(obj, ast.ClassDef):
            return 'class', self.parse_class(obj)
        elif isinstance(obj, ast.FunctionDef):
            return 'function', self.parse_function(obj, is_async=False)
        elif isinstance(obj, ast.AsyncFunctionDef):
            return 'function', self.parse_function(obj, is_async=True)
        elif isinstance(obj, ast.Assign):
            return 'assign', self.parse_assign(obj)
        elif isinstance(obj, ast.AnnAssign):
            return 'assign', self.parse_ann_assign(obj)
        return None, None

    def parse_assign(self, obj: stmt) -> List[Dict]:
        """
        Function parse assigns
        :param ast.Assign obj: value to parse
        :return: List[{'name_variable': variable.id,
                    'value': _value,
                    'type': _type}]
        """
        variables = obj.targets[0]
        values = obj.value
        result = list()
        if isinstance(variables, ast.Tuple):
            if isinstance(values, ast.Tuple):
                for variable, value in zip(variables.elts, values.elts):
                    _value, _type = self._get_value(value)
                    result.append({
                        'name_variable': variable.id,
                        'value': _value,
                        'type': _type
                    })
            if isinstance(values, ast.Call):
                name_variable = ', '.join([str(v.id) for v in variables.elts])

                result.append({
                    'name_variable': name_variable,
                    'value': values.func.id,
                    'type': 'function'
                })

        elif isinstance(variables, ast.Name):
            _value, _type = self._get_value(values)
            result.append({
                'name_variable': variables.id,
                'value': _value,
                'type': _type
            })
        else:
            print("unknown_assign", variables)
        return result

    def parse_ann_assign(self, obj: stmt) -> List[Dict]:
        """
        Parse annotated assigns
        :param ast.AnnAssign obj: value to parse
        :return: [{
                'name_variable':,
                'value':,
                'type': ,
                'declared_type':,
            }]
        """
        _value, _type = self._get_value(obj.value)
        return [
            {
                'name_variable': obj.target.id,
                'value': _value,
                'type': _type,
                'declared_type': obj.annotation.id,
            }
        ]

    def parse_function(self,
                       obj: stmt,
                       is_async: bool = False) -> Dict:
        """
        Method retrieves available information about a method
        :param stmt obj: object function for parse info
        :param bool is_async:
        :return: {
            'name': str
            'is_async': bool,
            'arguments': list[dict],
            'decorators': list[dict],
            'returns': dict,
            'doc_string': optional[str],
        }
        """
        function_decorators = self._get_decorators(obj)
        function_args = self._get_arguments(obj)
        returns = None
        if obj.returns:
            returns, _ = self._get_value(obj.returns)
        function_doc_string = ast.get_docstring(obj)
        function_data = {
            'name': obj.name,
            'is_async': is_async,
            'arguments': function_args,
            'decorators': function_decorators,
            'returns': returns,
            'doc_string': function_doc_string,
        }
        return function_data

    def _get_decorators(self,
                        obj: stmt) -> List[Dict]:
        """
        Function get list decorators object
        :param obj: object to get decorators
        :return: [{'name'}, {'name','args':[{value, type],keywords:[name,value,type] ]
        """
        decorators = list()
        for decorator in obj.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append({
                    'name': decorator.id
                })
            elif isinstance(decorator, ast.Call):
                args = list()
                keywords = list()

                for arg in decorator.args:
                    _value, _type = self._get_value(arg)
                    args.append({
                        'value': _value,
                        'type': _type
                    })
                for keyword in decorator.keywords:
                    _value, _type = self._get_value(keyword.value)
                    keywords.append({
                        'name': keyword.arg,
                        'value': _value,
                        'type': _type
                    })
                decorators.append({
                    'name': decorator.func.id,
                    'args': args,
                    'keywords': keywords
                })
            elif isinstance(decorator, ast.Attribute):
                decorators.append({
                    'name': f'{decorator.value.id}.{decorator.attr}'
                })
            else:
                print('unknown decorator', decorator)
        return decorators

    def _get_arguments(self,
                       obj: stmt) -> List[Dict]:
        """
        Function get arguments
        :param obj:
        :return:[{name, value, type}]
        """
        arguments = list()
        for arg in obj.args.args:
            if arg.arg in arguments_to_ignore:
                continue
            if arg.annotation:
                _value, _type = self._get_value(arg.annotation)
            else:
                _value, _type = None, None
            arguments.append({
                'name': arg.arg,
                'value': _value,
                'type': _type
            })
        return arguments

    def _get_value(self,
                   obj: stmt) -> Tuple[Any, str]:
        """
        Method for parse values with type value
        :param stmt obj: object to get value
        :return: value, type
        """
        if obj is None:
            return None, 'none'
        elif obj in [True, False]:
            return obj, 'bool'
        elif isinstance(obj, ast.Num):
            return obj.n, 'num'
        elif isinstance(obj, ast.Str):
            return obj.s, 'str'
        elif isinstance(obj, ast.Name):
            return obj.id, 'object'
        elif isinstance(obj, ast.NameConstant):
            return self._get_value(obj.value)
        elif isinstance(obj, ast.Dict):
            return {self._get_value(key)[0]: self._get_value(value)[0]
                    for key, value in zip(obj.keys, obj.values)}, 'dict'
        elif isinstance(obj, (ast.List, ast.Tuple)):
            resp = list()
            for value in obj.elts:
                _value, _type = self._get_value(value)
                resp.append(
                    {
                        'value': _value,
                        'type': _type})
            return resp, 'list' if isinstance(obj, ast.List) else 'tuple'
        elif isinstance(obj, ast.Subscript):
            _value, _type = self._get_value(obj.value)
            sub_value, sub_type = self._get_value(obj.slice.value)
            data = {
                'value': _value,
                'type': _type,
                'sub_type': sub_type,
                'sub_value': sub_value
            }
            return data, 'subscript'
        elif isinstance(obj, ast.Call):
            _value, _type = self._get_value(obj.func)

            args = list()
            keywords = list()

            for arg in obj.args:
                _value, _type = self._get_value(arg)
                args.append({
                    'value': _value,
                    'type': _type
                })
            for keyword in obj.keywords:
                _value, _type = self._get_value(keyword.value)
                keywords.append({
                    'name': keyword.arg,
                    'value': _value,
                    'type': _type
                })
            data = {
                'value': _value,
                'type': _type,
                'keywords': keywords,
                'args': args
            }
            return data, 'object'
        else:
            print('unknown value', obj)
        return "can't parse", 'unknown'

    def parse_class(self, obj: stmt) -> Dict:
        """
        Method retrieves available information about a class
        :param stmt obj:
        :return:
        """
        keywords = list()
        for keyword in obj.keywords:
            _value, _type = self._get_value(keyword.value)
            keywords.append({
                'name': keyword.arg,
                'value': _value,
                'type': _type
            })
        class_decorators = self._get_decorators(obj)
        bases = self._get_bases(obj)
        class_doc_string = ast.get_docstring(obj)
        class_data = {
            'name': obj.name,
            'decorators': class_decorators,
            'bases': bases,
            'keywords': keywords,
            'doc_string': class_doc_string

        }
        return class_data

    def _get_bases(self, obj: stmt) -> List[str]:
        """
        Method extract base classes
        :param stmt obj: obj class
        :return: list[str] base classes
        """
        return [
            self._get_value(base)[0]
            for base in obj.bases
        ]

    def _parse_file(self, path_to_file: Path) -> Dict:
        """
        Main processing method
        Reads the file and starts the parsing process
        :param Path path_to_file: path to the file to be processed
        :return: dict with extracted information from file
        """
        file_to_parse = open(path_to_file, 'r', encoding='utf-8').read()
        tree = ast.parse(file_to_parse)
        dict_resp = dict()
        module_doc_string = ast.get_docstring(tree)
        dict_resp['module_doc_string'] = module_doc_string if module_doc_string else ''
        for obj in tree.body:
            obj_type, object_documentation = self._parse_obj(obj)
            data_body = self.parse_body(obj, obj_type)
            dict_resp = self.organize_received_info(obj_type,
                                                    object_documentation,
                                                    dict_resp,
                                                    data_body)
        return dict_resp

    def parse_body(self, to_parse: stmt, _type: str) -> Optional[Dict]:
        """
        Method parse body objects who have it
        :param stmt to_parse: object to procee
        :param _type: type current object in system
        :return: optional[dict] information about objects in body
        """
        if _type not in ['class', 'function']:
            return None
        with_assign = True
        if _type == 'function':
            with_assign = False
        dict_resp = dict()
        for obj in to_parse.body:
            if isinstance(obj, (ast.Assign, ast.AnnAssign)):
                if not with_assign:
                    continue
            obj_type, object_documentation = self._parse_obj(obj)
            if not obj_type:
                continue
            if obj_type == 'assign' and not with_assign:
                continue
            data_body = self.parse_body(obj, obj_type)
            dict_resp = self.organize_received_info(obj_type,
                                                    object_documentation,
                                                    dict_resp,
                                                    data_body)
        return dict_resp

    @staticmethod
    def organize_received_info(_type: str,
                               value: Any,
                               dict_to_process: Dict,
                               body: Dict = None):
        """
        Method for add info to dict
        :param _type:
        :param value:
        :param dict_to_process:
        :param body:
        :return:
        """
        if _type == 'assign':
            assigns_list = dict_to_process.get('assigns', list())
            assigns_list.extend(value)
            dict_to_process['assigns'] = assigns_list
        elif _type == 'function':
            functions_list = dict_to_process.get('functions', list())
            value['body'] = body
            functions_list.append(value)
            dict_to_process['functions'] = functions_list
        elif _type == 'class':
            class_list = dict_to_process.get('classes', list())
            value['body'] = body
            class_list.append(value)
            dict_to_process['classes'] = class_list
        return dict_to_process

    def build_documentation_file(self,
                                 path_to_file: Path,
                                 deep: int = 1) -> List[str]:
        """

        :param Path path_to_file: path to the file to be processed
        :param int deep: deep for print
        :return: list[str] for build info in readme
        """
        dict_info = self._parse_file(path_to_file)
        file_info = PythonDocSerializer.serialize(path_to_file,
                                                  dict_data=dict_info,
                                                  deep=deep)
        return file_info
