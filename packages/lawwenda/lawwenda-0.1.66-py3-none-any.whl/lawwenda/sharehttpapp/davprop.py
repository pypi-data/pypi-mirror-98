# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t
import xml.etree.ElementTree as ET

import werkzeug.http

import lawwenda.fs


all_props = []


def register_prop(prop: t.Type['DavProp']):
    all_props.append(prop())
    return prop


def get_prop_by_davname(davname: str) -> t.Optional['DavProp']:
    for prop in all_props:
        if prop.davname == davname:
            return prop


class DavProp:

    def __init__(self, davname: str, *, is_writable: bool):
        self.__davname = davname
        self.__is_writable = is_writable

    @property
    def davname(self) -> str:
        return self.__davname

    @property
    def is_writable(self) -> bool:
        return self.__is_writable

    def get_for_node(self, fsnode: lawwenda.fs.Filesystem.Node) -> t.Optional[str]:
        pass


@register_prop
class ResourceTypeDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:}resourcetype", is_writable=False)

    def get_for_node(self, fsnode):
        return ET.Element("{DAV:}collection") if fsnode.is_dir else ""


@register_prop
class SizeDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:}getcontentlength", is_writable=False)

    def get_for_node(self, fsnode):
        return fsnode.size


@register_prop
class MtimeDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:}getlastmodified", is_writable=False)

    def get_for_node(self, fsnode):
        return werkzeug.http.http_date(fsnode.mtime_ts)


@register_prop
class CommentDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:xattr}xdg.comment", is_writable=True)

    def get_for_node(self, fsnode):
        return fsnode.comment


@register_prop
class TagsDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:xattr}xdg.tags", is_writable=True)

    def get_for_node(self, fsnode):
        return fsnode.tagstring


@register_prop
class RatingDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:xattr}baloo.rating", is_writable=True)

    def get_for_node(self, fsnode):
        return fsnode.rating


@register_prop
class GeoDavProp(DavProp):

    def __init__(self):
        super().__init__("{DAV:xattr}pino.geo", is_writable=True)

    def get_for_node(self, fsnode):
        return fsnode.geo
