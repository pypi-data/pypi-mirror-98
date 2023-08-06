from enum import Enum
from typing import Callable, Awaitable, AsyncGenerator, Dict

AsyncChunkIterator = Callable[[int], Awaitable[AsyncGenerator[None, bytes]]]
AsyncLineIterator = AsyncGenerator[None, str]


class RestMethod(Enum):
    GET = 'GET'
    POST = 'POST'


class API:

    def __init__(self, func, method: RestMethod, content_type: str, is_instance_method: bool):
        annotations = func.__annotations__
        self._is_instance_method = is_instance_method
        self._func = func
        self._method = method
        if 'return' not in annotations:
            raise TypeError(f"No annotation for return type in {func}")
        self._arg_annotations = {name: typ for name, typ in annotations.items() if name != 'return'}
        self._async_arg_annotations = {
            name: typ for name, typ in self._arg_annotations.items() if typ in (bytes, AsyncChunkIterator, AsyncLineIterator)
        }
        if len(self._async_arg_annotations) > 1:
            raise TypeError("At most one parameter can be and async iterator in a web_api request")
        self._return_type = annotations['return']
        self._has_streamed_response = False
        if str(self._return_type).startswith('typing.AsyncIterator'):
            self._return_type = self._return_type.__args__[0]
            self._has_streamed_response = True
        elif str(self._return_type).startswith('typing.AsyncGenerator'):
            self._return_type = self._return_type.__args__[1]
            self._has_streamed_response = True
        self._content_type = content_type if not self.has_streamed_response else 'text/streamed; charset=x-user-defined'

    @property
    def name(self):
        return self._func.__name__

    @property
    def qualname(self):
        return self._func.__qualname__

    @property
    def module(self):
        return self._func.__module__

    @property
    def doc(self):
        return self._func.__doc__

    @property
    def method(self):
        return self._method

    @property
    def is_instance_method(self):
        return self._is_instance_method

    @property
    def content_type(self):
        return self._content_type

    @property
    def arg_annotations(self):
        return self._arg_annotations

    @property
    def async_arg_annotations(self):
        return self._async_arg_annotations

    @property
    def synchronous_arg_annotations(self):
        return [a for a in self._arg_annotations if a not in self._async_arg_annotations]

    @property
    def return_type(self):
        return self._return_type

    @property
    def has_streamed_request(self) -> bool:
        return len(self._async_arg_annotations) > 0

    @property
    def has_streamed_response(self) -> bool:
        return self._has_streamed_response

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


class APIDoc:
    """
    Class for converting python docs to target language/protocol (javascript, ReST API, ...)
    """

    class Flavor(Enum):
        JAVASCRIPT: str = "javascript"
        REST: str = "rest"
        PYTHON: str = "python"

    # noinspection PyProtectedMember
    @classmethod
    def generate(cls, flavor: Flavor, api: API, indent: str = "") -> str:
        """
        Add documentation for given method.

        :param flavor: which language/protocol to document
        :param api: which api to document
        :param indent: how much to indent each doc line by
        """
        if flavor == cls.Flavor.PYTHON:
            return '"""\n' + api._func.__doc__ + '\n"""\n'
        main_doc = ""
        type_names: Dict[str, str] = {}
        if flavor == cls.Flavor.REST:
            route = '/' + api._func.__qualname__.replace('.', '/')
            top_line = f"ROUTE: {api.method.value} {route}"
            main_doc += f"\n{top_line}\n"
            main_doc += '~'*len(top_line) + '\n'
            main_doc += f"\nContent-Type: {api.content_type}\n"
        elif flavor == cls.Flavor.JAVASCRIPT:
            main_doc += f"{indent}/**"
        return_type_name = cls._get_type_name(api.return_type) if api.return_type else None
        for line in (api._func.__doc__ or "<<no documentation provided>>").splitlines():
            line = line.strip()
            if line.startswith('...') or line.startswith('>>>'):
                continue
            if line.startswith(':param '):
                name, doc = line[6:].strip().split(':', maxsplit=1)
                if name not in api.arg_annotations:
                    raise LookupError(f"Paremeter with name {name} found in doc string but no such parameter"
                                      f"exists in {api._func}")
                typ = api.arg_annotations[name]
                type_names[name] = cls._get_type_name(typ)
                main_doc += indent + f"**param**: $${name}$$ -- {doc}\n"
            elif line.startswith(':return'):
                _, doc = line[7:].strip().split(':', maxsplit=1)
                if api.has_streamed_response:
                    doc = "[$$streamed$$] " + doc
                main_doc += '\n' + indent + f"$$return$$ {doc}\n"
            elif line.startswith(':raises'):
                _, doc = line[7:].strip().split(':', maxsplit=1)
                main_doc += indent + f"$$raises$$ {doc}"
            else:
                main_doc += indent + line + '\n'
        for name in [arg for arg in api.arg_annotations if arg not in type_names]:
            main_doc += f"\n{indent}*undocumented param*: {name} of type {cls._get_type_name(api.arg_annotations[name])}"
            type_names[name] = api.arg_annotations[name]
        main_doc += "\n"
        if flavor == cls.Flavor.JAVASCRIPT:
            for name in api.arg_annotations:
                main_doc = main_doc.replace(f"$${name}$$", f"{name} {{{type_names[name]}}}")
            main_doc = main_doc.replace("$$return$$", f"@return {{{return_type_name}}}")
            main_doc = main_doc.replace('**param**', '@param')
            main_doc = main_doc.replace('**return**', '@return')
            main_doc = main_doc.replace('$$raises$$', 'raises exception:')
            main_doc = main_doc.replace('$$streamed$$', 'iterator')
        elif flavor == cls.Flavor.REST:
            for name in api.arg_annotations:
                main_doc = main_doc.replace(f"$${name}$$", f"{name} *{type_names[name]}* -- ")
            from .http import WebApplication
            if api in WebApplication._instance_methods_class_map or api.name == '_expire':
                self_param = "**param**: self {{string}} -- unique id of a created instance"
                if '**param**' in main_doc:
                    main_doc = main_doc.replace('**param**', self_param + '\n**param**', 1)
                elif '**return**' in main_doc:
                    main_doc = main_doc.replace('**return**', self_param + '\n**return**', 1)
                else:
                    main_doc += self_param + '\n'

            main_doc = main_doc.replace('**return**', "**response** ")
            main_doc = main_doc.replace('**param**', "\n**param** ")
            main_doc = main_doc.replace('$$return$$', f"**response**: *{return_type_name}* -- ")
            main_doc = main_doc.replace('$$raises$$', "**error status**")
            main_doc = main_doc.replace('$$streamed$$', 'streamed')
        else:
            raise ValueError(f"Unknown doc type: {flavor}")
        if flavor == cls.Flavor.JAVASCRIPT:
            main_doc += f"{indent}**/\n"
        else:
            main_doc += "\n"
        return main_doc

    @staticmethod
    def _get_type_name(typ) -> str:
        """
        :return: string name for given type
        """
        if str(typ).startswith('typing.AsyncIterator') or str(typ).startswith('typing.AsyncGenerator'):
            root_type = str(typ).split('[')[1].replace(']', '')
            if ',' in root_type:
                root_type = root_type.split(',')[1]
            return f"iterator of type {root_type}"
        elif str(typ).startswith('typing.Union'):
            root_type = str(typ).split('[')[1].split(',')[0]
            return f"[optional] {root_type}"
        elif str(typ).startswith('typing.List'):
            root_type = str(typ).split('[')[1].replace(']', '')
            return f"list of {root_type}"
        elif str(typ).startswith('typing.Dict') or str(typ).startswith('typing.Mapping'):
            root_type = str(typ).split('[')[1].replace(']', '')
            return f"dict of {root_type}"
        elif str(typ).startswith('typing.Dict') or str(typ).startswith('typing.Mapping'):
            key_type, value_type = str(typ).split('[')[1].replace(']', '').split(',')
            return f"Dictionary of key type {key_type} and value type {value_type}"
        else:
            # noinspection PyProtectedMember
            return typ.__name__ if hasattr(typ, '__name__') else typ._name if hasattr(typ, '_name') else str(typ)
