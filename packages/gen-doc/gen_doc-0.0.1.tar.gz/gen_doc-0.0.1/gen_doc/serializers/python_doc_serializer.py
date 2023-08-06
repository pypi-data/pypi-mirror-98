"""
Module with serializer python files
"""
# pylint: disable=invalid-name,too-many-statements
import os
from collections.abc import Iterable
from pathlib import Path
from typing import List, Dict

arguments_to_ignore = [
    'self'
]

name_key_words = [
    ':param', ':example', ':return'
]


class PythonDocSerializer:
    """
    Serializer for python doc
    """

    @staticmethod
    def serialize(path_to_file: Path,
                  dict_data: dict,
                  deep: int = 1) -> List[str]:
        documentation = list()
        documentation.append('#' * deep + ' ' + path_to_file.name)

        # add module doc string
        if dict_data.get('module_doc_string'):
            documentation.append('#' * (deep + 1) + ' ' + dict_data['module_doc_string'])

        documentation.extend(PythonDocSerializer.serialize_parts(dict_data, deep + 1))
        return documentation

    @staticmethod
    def serialize_parts(dict_data: dict, deep: int = 1, object_name: str = '') -> List[str]:
        """
        Method serialize all existed parts
        :param dict_data:
        :param deep:
        :param object_name:
        :return:
        """
        documentation = list()
        if dict_data.get('assigns'):
            documentation.extend(PythonDocSerializer.serialize_assigns(dict_data['assigns'],
                                                                       deep))
        if dict_data.get('functions'):
            documentation.extend(PythonDocSerializer.serialize_functions(dict_data['functions'],
                                                                         deep,
                                                                         class_name=object_name))
        if dict_data.get('classes'):
            documentation.extend(PythonDocSerializer.serialize_classes(dict_data['classes'],
                                                                       deep))
        return documentation

    @staticmethod
    def serialize_assigns(assigns_data: dict,
                          deep: int = 1,
                          title: str = 'Variable assignment'):
        """
        Method for serialize assigns
        :param assigns_data:
        :param deep:
        :param title:
        :return:
        """
        documentation = list()
        for assign_data in assigns_data:
            row = f"+ `{assign_data['name_variable']}`" \
                  f"{': ' + assign_data['declared_type'] if assign_data.get('declared_type') else ''} = " \
                  f"{PythonDocSerializer.build_type_assigns(assign_data['value'])}: {assign_data['type']}"
            documentation.append(row)
        if documentation:
            row = '#' * deep + f' {title}'
            documentation.insert(0, row)
        return documentation

    @staticmethod
    def serialize_functions(functions_data,
                            deep: int = 1,
                            class_name: str = ''):
        """
        Method for serialize functions
        :param functions_data:
        :param deep:
        :param class_name:
        :return:
        """
        documentation = list()
        if class_name:
            class_name += '.'

        for function_data in functions_data:
            name = f"Function {'`async` ' if function_data['is_async'] else ''}" \
                   f"`{class_name + function_data['name']}`"
            documentation.append('#' * deep + ' ' + name)
            if function_data.get('doc_string'):
                documentation.extend(PythonDocSerializer.serialize_doc_string_comment(
                    function_data['doc_string'],
                    function_data['arguments'],
                    deep + 1
                ))
            else:
                arguments = list()
                for arg in function_data['arguments']:
                    _type = PythonDocSerializer.build_type(arg['value'])
                    row = f'+ `{arg["name"]}`: {_type if _type else "unknown"}'
                    arguments.append(row)
                if arguments:
                    documentation.append('#' * (deep + 1) + ' **Arguments**:')
                    documentation.extend(arguments)
            if function_data.get('decorators'):
                documentation.extend(PythonDocSerializer.build_decorators(function_data, deep))
            if function_data.get('returns'):
                documentation.append(
                    '#' * (deep + 2) + ' ' + f'Declared '
                                             f'returns: `{PythonDocSerializer.build_type(function_data["returns"])}`'
                )
            if function_data['body']:
                documentation.extend(
                    PythonDocSerializer.serialize_parts(function_data['body'], deep=deep + 1)
                )

        return documentation

    @staticmethod
    def serialize_classes(classes_data: Dict,
                          deep: int = 1,
                          class_name: str = '') -> List[str]:
        """
        Method for serialize classes
        :param classes_data:
        :param deep:
        :param class_name:
        :return:
        """
        documentation = list()
        for class_data in classes_data:

            additional_class_str = ''
            pre_additional_class_str = ''
            if class_name:
                pre_additional_class_str = f'{class_name}.'
            if class_data.get('bases'):
                additional_class_str = f'({",".join(class_data["bases"])})'
            row = pre_additional_class_str + class_data["name"] + additional_class_str
            name = f'Class  `{row}`'
            documentation.append('#' * deep + ' ' + name)
            if class_data.get('doc_string'):
                documentation.append(f"`{class_data['doc_string']}`")
            if class_data.get('decorators'):
                documentation.extend(PythonDocSerializer.build_decorators(class_data, deep))
            if class_data.get('body'):
                if class_data['body'].get('assigns'):
                    documentation.extend(
                        PythonDocSerializer.serialize_assigns(class_data['body']['assigns'],
                                                              deep + 2,
                                                              'Class variables')
                    )

                if class_data['body'].get('functions'):
                    documentation.extend(PythonDocSerializer
                                         .serialize_functions(class_data['body']['functions'],
                                                              class_name=class_data["name"],
                                                              deep=deep + 1))
                if class_data['body'].get('classes'):
                    documentation.extend(PythonDocSerializer
                                         .serialize_classes(class_data['body']['functions'],
                                                            class_name=class_data["name"],
                                                            deep=deep + 1))
        return documentation

    @staticmethod
    def build_decorators(object_data, deep) -> List[str]:
        """
        Method for build decorators
        :param object_data:
        :param deep:
        :return:
        """
        data_decorators = list()
        for decorator in object_data['decorators']:
            params = list()
            if decorator.get('args'):
                for arg in decorator['args']:
                    params.append(f"{arg['value']}")
            if decorator.get('keywords'):
                for arg in decorator['keywords']:
                    params.append(f"{arg['name']}={arg['value']}")
            additional_row = ', '.join(params)
            data_decorators.append(
                f'+ @{decorator["name"]}{f" ({additional_row})" if additional_row else ""}'
            )
        if data_decorators:
            data_decorators.insert(0,
                                   '#' * (deep + 2) + ' ' + 'Decorators')
        return data_decorators

    @staticmethod
    def build_type(data):
        """
        Method for build types methods
        :param data:
        :return:
        """
        if not isinstance(data, Iterable):
            return str(data)
        if isinstance(data, str):
            return data
        _type = data['value']
        if data.get('sub_value'):
            if isinstance(data['sub_value'], dict):
                _type += f"[{PythonDocSerializer.build_type(data['sub_value'])}]"
            elif isinstance(data['sub_value'], list):
                types = [
                    PythonDocSerializer.build_type(v)
                    for v in data['sub_value']
                ]
                _type += f'[{",".join(types)}]'
            else:
                _type += f'[{data["sub_value"]}]'
        return _type

    @staticmethod
    def build_type_assigns(data):
        """
        Method for build types assigns
        :param data:
        :return:
        """
        if isinstance(data, str):
            return data
        if not isinstance(data, Iterable):
            return str(data)

        if isinstance(data, list):
            return "[{}]".format(','.join(["'{}'".format(d['value']) for d in data]))
        elif isinstance(data, dict):
            if data.get('type') and data['type'] == 'object':
                return f"{data['value']}()"
            return str(data)
        return 'unknown'

    @staticmethod
    def serialize_doc_string_comment(doc_string,
                                     args: List, deep=1) -> List[str]:
        """
        method build documentation for method by doc string
        :param doc_string:
        :param args:
        :param deep:
        :return:
        """

        def splitter(doc_str):
            def extract_doc_str(lr):
                resp = list()
                is_break = False
                for row in lr:
                    if not row:
                        continue
                    for kw in name_key_words:
                        if row.lower()[:len(kw)] == kw:
                            is_break = True
                            break
                    else:
                        resp.append(row)
                    if is_break:
                        break
                return f'{os.linesep}'.join(resp)

            def extract_params(lr, key):
                resp = list()
                i = 0
                is_break = False

                while i < len(lr):
                    row = lr[i]
                    is_break = False

                    if row.lower()[:len(key)] == key:
                        tmp = [lr[i]]
                        i += 1
                        is_break = False
                        while i < len(lr):
                            if not lr[i]:
                                i += 1
                                continue
                            for kw in name_key_words:
                                if lr[i].lower()[:len(kw)] == kw:
                                    is_break = True
                                    break
                            else:
                                tmp.append(lr[i])
                                i += 1
                            if is_break:
                                resp.append(tmp)
                                break
                        else:
                            resp.append(tmp)
                    if is_break:
                        continue

                    i += 1

                respons = [f'{os.linesep}'.join(val) for val in resp]
                return respons

            tmp = doc_str.split(os.sep)
            if len(tmp) == 1:
                tmp = doc_str.split('\n')
            # drop empty
            str_list = [str_row.strip() for str_row in tmp if str_row]
            doc_str = extract_doc_str(str_list)
            _params = extract_params(str_list, ':param')
            new_params = dict()
            for p in _params:
                parts = p.split(':')[1:]
                block = parts[0].split()
                if len(block) == 2:
                    new_params[block[-1]] = {
                        'type': '',
                        'description': ':'.join(parts[1:])
                    }
                else:
                    new_params[block[-1]] = {
                        'type': ' '.join(block[1:-1]),
                        'description': ':'.join(parts[1:])
                    }
            _example = extract_params(str_list, ':example')
            _return = extract_params(str_list, ':return')
            return {
                'description': doc_str,
                'params': new_params,
                'example': _example,
                'return': _return
            }

        rows = list()

        resp = splitter(doc_string)
        params = resp['params']
        if resp['description']:
            rows.append(f" ``` \n {resp['description']} \n ```")
        if args:
            rows.append('#' * deep + ' ' + '**Arguments**:')
            for _args in args:
                _declared_type = PythonDocSerializer.build_type(_args['value'])
                parsed_type = params.get(_args['name'], dict()).get('type')
                if _declared_type:
                    arg_type = _declared_type
                elif parsed_type:
                    arg_type = parsed_type
                else:
                    arg_type = 'unknown'
                description = params.get(_args['name'], dict()).get('description')
                if not description:
                    description = 'empty description'
                row = f" + `{_args['name']}`: `{arg_type}` - {description}"
                rows.append(row)

        if resp.get('return'):
            returns = list()
            for row in resp['return']:
                row = row.replace(':return:', '')
                if row:
                    returns.append(row)
            if returns:
                rows.append('#' * deep + ' ' + '**Returns**:')
                rows.append('```console')
                rows.append('\n'.join(returns))
                rows.append('```')
        if resp.get('example'):
            rows.append('#' * deep + ' ' + '**Examples**:')
            for example in resp['example']:
                _row = example.replace(':example:', '') \
                    .replace(':Example:', '') \
                    .strip()
                rows.append(f" ```python\n {_row} \n```")
        return rows
