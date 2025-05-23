import logging
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Literal, Protocol, overload

import cython
import lxml.etree as tree
from lxml.etree import CDATA, Element
from sizestr import sizestr

from app.config import XML_PARSE_MAX_SIZE
from app.lib.date_utils import parse_date
from app.lib.exceptions_context import raise_for
from app.lib.format_style_context import format_is_json

_PARSER = tree.XMLParser(
    recover=True,
    remove_blank_text=True,
    remove_comments=True,
    remove_pis=True,
    collect_ids=False,
    resolve_entities=False,
)


class XMLToDict:
    @staticmethod
    def parse(
        xml_bytes: bytes, *, size_limit: int | None = XML_PARSE_MAX_SIZE
    ) -> dict[str, list[tuple[str, Any]] | dict[str, Any]]:
        """Parse XML string to dict."""
        if size_limit is not None and len(xml_bytes) > size_limit:
            raise_for.input_too_big(len(xml_bytes))

        logging.debug('Parsing %s XML string', sizestr(len(xml_bytes)))
        root = tree.fromstring(xml_bytes, parser=_PARSER)
        root_element = _parse_element(root)

        if isinstance(root_element, str):  # type: ignore
            raise_for.bad_xml(
                root.tag, f'XML contains only text: {root_element}', xml_bytes
            )

        return {_strip_namespace(root.tag): root_element}

    @staticmethod
    @overload
    def unparse(d: dict[str, Any]) -> str: ...
    @staticmethod
    @overload
    def unparse(d: dict[str, Any], *, raw: Literal[True]) -> bytes: ...
    @staticmethod
    @overload
    def unparse(d: dict[str, Any], *, raw: Literal[False]) -> str: ...
    @staticmethod
    def unparse(d: dict[str, Any], *, raw: bool = False) -> str | bytes:
        """Unparse dict to XML string."""
        if len(d) != 1:
            raise ValueError(f'Invalid root element count {len(d)}')

        root_k, root_v = next(iter(d.items()))
        elements = _unparse_element(root_k, root_v)
        root_element = next(iter(elements), None)

        # always return the root element, even if it's empty
        if root_element is None:
            root_element = Element(root_k)

        result = tree.tostring(root_element, encoding='UTF-8', xml_declaration=True)
        logging.debug('Unparsed %s XML string', sizestr(len(result)))
        return result if raw else result.decode()


@cython.cfunc
def _parse_element(element: tree._Element):
    # parse attributes
    # read property once for performance
    value_postprocessor: dict[str, Callable[[str], Any]] = _VALUE_POSTPROCESSOR
    parsed: list[tuple[str, Any]] = [
        (f'@{k}', call(v) if (call := value_postprocessor.get(k)) is not None else v)  # pyright: ignore[reportArgumentType]
        for k, v in element.attrib.items()
    ]

    # parse children
    sequence_mark: cython.bint = False
    if children := list(element):
        # read property once for performance
        force_sequence_root: set[str] = _FORCE_SEQUENCE_ROOT
        force_list: set[str] = _FORCE_LIST
        parsed_children: dict[str, Any | list[Any]] = {}

        for child in children:
            k = _strip_namespace(child.tag)
            v = _parse_element(child)

            if isinstance(v, str) and (call := value_postprocessor.get(k)) is not None:  # pyright: ignore [reportUnnecessaryIsInstance]
                v = call(v)

            # in sequence mode, return root element as tuple
            if k in force_sequence_root:
                parsed.append((k, v))
                sequence_mark = True

            # merge with existing value
            elif (parsed_v := parsed_children.get(k)) is not None:
                if isinstance(parsed_v, list):
                    parsed_v.append(v)
                else:
                    # upgrade from single value to list
                    parsed_children[k] = [parsed_v, v]

            # add new value
            else:
                parsed_children[k] = [v] if k in force_list else v

        if parsed_children:
            parsed.extend(parsed_children.items())

    # parse text content
    if (text := element.text) is not None and (text := text.strip()):
        if not parsed:
            return text
        parsed.append(('#text', text))

    # in sequence mode, return element as tuple
    return parsed if sequence_mark else dict(parsed)


@cython.cfunc
def _unparse_element(key: str, value: Any) -> list[tree._Element]:
    k: str
    v: Any

    # encode dict
    if isinstance(value, dict):
        element = Element(key)
        element_attrib = element.attrib  # read property once for performance
        element_extend = element.extend
        for k, v in value.items():
            if k[0] == '@':
                element_attrib[k[1:]] = _to_string(v)
            elif k == '#text':
                element.text = _to_string(v)
            else:
                element_extend(_unparse_element(k, v))
        return [element]

    # encode sequence of ...
    elif isinstance(value, (list, tuple)):
        if not value:
            return []
        first = value[0]

        # encode sequence of dicts
        if isinstance(first, dict):
            return [e for v in value for e in _unparse_element(key, v)]

        # encode sequence of (key, value) tuples
        elif isinstance(first, (list, tuple)):
            element = Element(key)
            element_attrib = element.attrib  # read property once for performance
            element_extend = element.extend
            for k, v in value:
                if k[0] == '@':
                    element_attrib[k[1:]] = _to_string(v)
                elif k == '#text':
                    element.text = _to_string(v)
                else:
                    element_extend(_unparse_element(k, v))
            return [element]

        # encode sequence of scalars
        else:
            result: list[tree._Element] = [None] * len(value)  # type: ignore
            i: cython.Py_ssize_t
            for i, v in enumerate(value):
                element = Element(key)
                element.text = _to_string(v)
                result[i] = element
            return result

    # encode scalar
    else:
        element = Element(key)
        element.text = _to_string(value)
        return [element]


# tags that will become tuples (order-preserving): [('tag', ...), ('tag', ...), ...]
_FORCE_SEQUENCE_ROOT: set[str] = {
    'bounds',
    'create',
    'modify',
    'delete',
    'node',
    'way',
    'relation',
}

# tags that will become a list of values: {'tag': [...]}
_FORCE_LIST: set[str] = {
    'member',
    'tag',
    'nd',
    'trk',
    'trkseg',
    'trkpt',
    'preference',
    'note',
    'comment',
    'gpx_file',
}


@cython.cfunc
def _parse_xml_bool(value: str):
    return value == 'true'


@cython.cfunc
def _parse_xml_version(value: str):
    # for simplicity, we don't support floating-point versions
    return int(value) if '.' not in value else float(value)


@cython.cfunc
def _parse_xml_date(value: str):
    return datetime.fromisoformat(value) if ' ' not in value else parse_date(value)


_VALUE_POSTPROCESSOR: dict[str, Callable[[str], Any]] = {
    'changeset': int,
    'changes_count': int,
    'closed_at': _parse_xml_date,
    'comments_count': int,
    'created_at': _parse_xml_date,
    'date': _parse_xml_date,
    'id': int,
    'lat': float,
    'lon': float,
    'ele': float,
    'max_lat': float,
    'max_lon': float,
    'min_lat': float,
    'min_lon': float,
    'num_changes': int,
    'open': _parse_xml_bool,
    'pending': _parse_xml_bool,
    'ref': int,
    'time': _parse_xml_date,
    'timestamp': _parse_xml_date,
    'uid': int,
    'updated_at': _parse_xml_date,
    'version': _parse_xml_version,
    'visible': _parse_xml_bool,
}


@cython.cfunc
def _to_string(v: Any):
    if isinstance(v, (str, CDATA)):
        return v

    if isinstance(v, datetime):
        # strip timezone for backwards-compatible format
        tzinfo = v.tzinfo
        if tzinfo is not None:
            assert tzinfo is UTC, f'Timezone must be UTC, got {tzinfo!r}'
            v = v.replace(tzinfo=None)
        return v.isoformat() + 'Z'

    if isinstance(v, bool):
        return 'true' if v is True else 'false'

    return str(v)


@cython.cfunc
def _strip_namespace(tag: str) -> str:
    return tag.rsplit('}', 1)[-1] if tag[0] == '{' else tag


class _XAttrCallable(Protocol):
    def __call__(self, name: str, xml: str | None = None) -> str: ...


def _xattr_json(name: str, xml=None) -> str:
    return name


def _xattr_xml(name: str, xml: str | None = None) -> str:
    return '@' + (xml or name)


def get_xattr(*, is_json: bool | None = None) -> _XAttrCallable:
    """
    Return a function to format attribute names.

    If is_json is None (default), then the current format is detected.
    """
    return (
        _xattr_json
        if (is_json if is_json is not None else format_is_json())
        else _xattr_xml
    )
