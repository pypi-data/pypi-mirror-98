# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import datetime
import logging
import mimetypes
import os
import re
import shutil
import traceback
import typing as t

import lawwenda._aux.PiMetadataInterpreter.pimetadatainterpreter as pimetadatainterpreter

import lawwenda.previewer.commonimages
import lawwenda.previewer.commonvideos


FilesystemNodePredicate = t.Callable[['Filesystem.Node'], bool]


class Filesystem:

    class ReadHandle:
        """
        Read and write handles are just a stupid container that hold one :py:class:`Filesystem.Node`.

        This looks stupid at first, because you could just use this node directly instead. The added value of handles
        are a central mechanism for access control, which would be a bit less obvious and more scattered in code without
        this indirection.

        Of course it cannot avoid a way around it in code. An attacker that can change the code has won anyway. It just
        simplifies writing correct code that hopefully does not provide ways around it for the client.

        See :py:meth:`Filesystem.get_readhandle` and :py:meth:`Filesystem.get_writehandle`.
        """

        def __init__(self, node: 'Filesystem.Node'):
            self.readable_node = node

    class WriteHandle(ReadHandle):
        """
        See :py:class:`Filesystem.ReadHandle`.
        """

        def __init__(self, node: 'Filesystem.Node'):
            super().__init__(node)
            self.writable_node = node

    @staticmethod
    def sanitize_abspath(path: str) -> str:
        """
        Sanitizes slashes in a path and returns a path in the form `/foo/bar`. Precisely:

        - with a slash in the beginning
        - without a slash at the end
        - without double slashes
        - with `..` and `.` resolved
        - root path: `/`

        :param path: The input path.
        """
        path = os.path.abspath(f"/{path}")
        while "//" in path:
            path = path.replace("//", "/")
        while path[1:].endswith("/"):
            path = path[:-1]
        return path

    @property
    def rootnode(self) -> 'Filesystem.Node':
        return self.node_by_path("")

    def node_by_path(self, path: str) -> 'Filesystem.Node':
        return Filesystem.Node(path, filesystem=self)

    def get_readhandle(self, node: 'Filesystem.Node') -> 'Filesystem.ReadHandle':
        raise NotImplementedError()

    def get_writehandle(self, node: 'Filesystem.Node') -> 'Filesystem.WriteHandle':
        raise NotImplementedError()

    def try_get_fullpath(self, handle: t.Union['Filesystem.ReadHandle', 'Filesystem.WriteHandle'], *,
                         writable: bool) -> t.Optional[str]:
        return None

    def child_nodes(self, handle: 'Filesystem.ReadHandle') -> t.List['Filesystem.Node']:
        raise NotImplementedError()

    def is_hidden(self, handle: 'Filesystem.ReadHandle') -> bool:
        raise NotImplementedError()

    def is_dir(self, handle: 'Filesystem.ReadHandle') -> bool:
        raise NotImplementedError()

    def is_file(self, handle: 'Filesystem.ReadHandle') -> bool:
        raise NotImplementedError()

    def is_link(self, handle: 'Filesystem.ReadHandle') -> bool:
        raise NotImplementedError()

    def exists(self, handle: 'Filesystem.ReadHandle') -> bool:  # TODO xx noh review complete module
        raise NotImplementedError()

    def size(self, handle: 'Filesystem.ReadHandle') -> int:
        raise NotImplementedError()

    def mimetype(self, handle: 'Filesystem.ReadHandle') -> str:
        raise NotImplementedError()

    def mtime(self, handle: 'Filesystem.ReadHandle') -> datetime.datetime:
        raise NotImplementedError()

    def has_thumbnail(self, handle: 'Filesystem.ReadHandle') -> bool:
        raise NotImplementedError()

    def has_preview(self, handle: 'Filesystem.ReadHandle') -> bool:
        raise NotImplementedError()

    def comment(self, handle: 'Filesystem.ReadHandle') -> str:
        raise NotImplementedError()

    def rating(self, handle: 'Filesystem.ReadHandle') -> int:
        raise NotImplementedError()

    def tags(self, handle: 'Filesystem.ReadHandle') -> t.List[str]:
        raise NotImplementedError()

    def geo(self, handle: 'Filesystem.ReadHandle') -> pimetadatainterpreter.GeoLocation:
        raise NotImplementedError()

    def preview_html(self, handle: 'Filesystem.ReadHandle') -> str:
        raise NotImplementedError()

    def thumbnail(self, handle: 'Filesystem.ReadHandle') -> bytes:
        raise NotImplementedError()

    def delete(self, handle: 'Filesystem.WriteHandle') -> None:
        raise NotImplementedError()

    def mkdir(self, handle: 'Filesystem.WriteHandle') -> None:
        raise NotImplementedError()

    def copy_to(self, srchandle: 'Filesystem.ReadHandle', desthandle: 'Filesystem.WriteHandle') -> None:
        raise NotImplementedError()

    def move_to(self, srchandle: 'Filesystem.WriteHandle', desthandle: 'Filesystem.WriteHandle') -> None:
        raise NotImplementedError()

    def set_comment(self, handle: 'Filesystem.WriteHandle', comment: str) -> None:
        raise NotImplementedError()

    def set_geo(self, handle: 'Filesystem.WriteHandle', geo: str) -> None:
        raise NotImplementedError()

    def set_rating(self, handle: 'Filesystem.WriteHandle', rating: int) -> None:
        raise NotImplementedError()

    def add_tag(self, handle: 'Filesystem.WriteHandle', tag: str) -> None:
        raise NotImplementedError()

    def remove_tag(self, handle: 'Filesystem.WriteHandle', tag: str) -> None:
        raise NotImplementedError()

    def read_file(self, handle: 'Filesystem.ReadHandle') -> t.BinaryIO:
        raise NotImplementedError()

    def write_file(self, handle: 'Filesystem.WriteHandle', content: t.Union[bytes, t.BinaryIO]) -> None:
        raise NotImplementedError()

    def known_tags(self) -> t.List[str]:
        raise NotImplementedError()

    class Node:

        def __init__(self, path: str, *, filesystem: 'Filesystem'):
            self.__path = filesystem.sanitize_abspath(path)
            self.__filesystem = filesystem

        @property
        def path(self) -> str:
            return self.__path

        @property
        def _filesystem(self) -> 'Filesystem':
            return self.__filesystem

        @property
        def name(self) -> str:
            return os.path.basename(self.__path)

        @property
        def dirpath(self) -> str:
            return os.path.dirname(self.__path)

        @property
        def is_writable(self) -> bool:
            try:
                self.__filesystem.get_writehandle(self)
                return True
            except Exception:
                return False

        @property
        def is_hidden(self) -> bool:
            return self.__filesystem.is_hidden(self.__filesystem.get_readhandle(self))

        @property
        def is_dir(self) -> bool:
            return self.__filesystem.is_dir(self.__filesystem.get_readhandle(self))

        @property
        def is_file(self) -> bool:
            return self.__filesystem.is_file(self.__filesystem.get_readhandle(self))

        @property
        def is_link(self) -> bool:
            return self.__filesystem.is_link(self.__filesystem.get_readhandle(self))

        @property
        def exists(self) -> bool:
            return self.__filesystem.exists(self.__filesystem.get_readhandle(self))

        @property
        def size(self) -> int:
            return self.__filesystem.size(self.__filesystem.get_readhandle(self))

        @property
        def mimetype(self) -> str:
            return self.__filesystem.mimetype(self.__filesystem.get_readhandle(self)) or "application/octet-stream"

        @property
        def mtime(self) -> datetime.datetime:
            return self.__filesystem.mtime(self.__filesystem.get_readhandle(self))

        @property
        def mtime_ts(self) -> float:
            return self.mtime.timestamp()

        @property
        def icon_name(self) -> t.Optional[str]:
            if self.has_thumbnail:
                return None
            elif self.is_dir:
                return "dir"
            else:
                return "file"

        @property
        def has_thumbnail(self) -> bool:
            return self.__filesystem.has_thumbnail(self.__filesystem.get_readhandle(self))

        @property
        def has_preview(self) -> bool:
            return self.__filesystem.has_preview(self.__filesystem.get_readhandle(self))

        @property
        def comment(self) -> str:
            return self.__filesystem.comment(self.__filesystem.get_readhandle(self))

        @property
        def rating(self) -> int:
            return self.__filesystem.rating(self.__filesystem.get_readhandle(self))

        @property
        def tags(self) -> t.List[str]:
            return self.__filesystem.tags(self.__filesystem.get_readhandle(self))

        @property
        def tagstring(self) -> str:
            return pimetadatainterpreter.TagAssignments.tags_to_tagstring(self.tags)

        @property
        def geo(self) -> str:
            geoobj = self.geo_obj
            return geoobj.to_geostring() if geoobj else ""

        @property
        def geo_obj(self) -> pimetadatainterpreter.GeoLocation:
            return self.__filesystem.geo(self.__filesystem.get_readhandle(self))

        @property
        def basics_as_dict(self):
            return {k: getattr(self, k) for k in ["name", "dirpath", "is_dir", "is_file", "is_link", "size", "mtime_ts",
                                                  "icon_name"]}

        @property
        def full_as_dict(self):
            return {**{k: getattr(self, k) for k in ["comment", "rating", "tags", "geo", "preview_html"]},
                    **self.basics_as_dict}

        @property
        def preview_html(self) -> str:
            return self.__filesystem.preview_html(self.__filesystem.get_readhandle(self))

        @property
        def child_nodes(self) -> t.List['Filesystem.Node']:
            if not self.is_dir:
                return []
            return self.__filesystem.child_nodes(self.__filesystem.get_readhandle(self))

        @property
        def parent_node(self) -> 'Filesystem.Node':
            return self.child_by_name("..")

        def traverse_dir(self, *, raise_on_circle: bool,
                         param_path: str = "") -> t.Iterable[t.Tuple['Filesystem.Node', str]]:
            nodes = [(self, self.__filesystem.sanitize_abspath(param_path))]
            seen = set()
            while nodes:
                n, nparampath = nodes.pop()
                # noinspection PyProtectedMember
                seenkey = n.path, n._filesystem
                if seenkey in seen:
                    if raise_on_circle:
                        raise CircularTraversalError()
                    else:
                        continue
                seen.add(seenkey)
                yield n, nparampath
                for cn in n.child_nodes:
                    nodes.append((cn, self.__filesystem.sanitize_abspath(f"{nparampath}/{cn.name}")))

        def try_get_fullpath(self, *, writable: bool) -> t.Optional[str]:
            handle = self.__filesystem.get_writehandle(self) if writable else self.__filesystem.get_readhandle(self)
            return self.__filesystem.try_get_fullpath(handle, writable=writable)

        def child_by_name(self, name: str) -> 'Filesystem.Node':
            return self.__filesystem.node_by_path(f"{self.path}/{name}")

        def read_file(self) -> t.BinaryIO:
            return self.__filesystem.read_file(self.__filesystem.get_readhandle(self))

        def thumbnail(self) -> bytes:
            return self.__filesystem.thumbnail(self.__filesystem.get_readhandle(self))

        def delete(self) -> None:
            self.__filesystem.delete(self.__filesystem.get_writehandle(self))

        def mkdir(self) -> None:
            self.__filesystem.mkdir(self.__filesystem.get_writehandle(self))

        def copy_to(self, newpath: str) -> None:
            self.__filesystem.copy_to(self.__filesystem.get_readhandle(self),
                                      self.__filesystem.get_writehandle(self.__filesystem.node_by_path(newpath)))

        def move_to(self, newpath: str) -> None:
            self.__filesystem.move_to(self.__filesystem.get_writehandle(self),
                                      self.__filesystem.get_writehandle(self.__filesystem.node_by_path(newpath)))

        def set_comment(self, comment: str) -> None:
            self.__filesystem.set_comment(self.__filesystem.get_writehandle(self), comment)

        def set_geo(self, geo: str) -> None:
            self.__filesystem.set_geo(self.__filesystem.get_writehandle(self), geo)

        def set_rating(self, rating: int) -> None:
            self.__filesystem.set_rating(self.__filesystem.get_writehandle(self), rating)

        def add_tag(self, tag: str) -> None:
            self.__filesystem.add_tag(self.__filesystem.get_writehandle(self), tag)

        def remove_tag(self, tag: str) -> None:
            self.__filesystem.remove_tag(self.__filesystem.get_writehandle(self), tag)

        def write_file(self, content: t.Union[bytes, t.BinaryIO]) -> None:
            self.__filesystem.write_file(self.__filesystem.get_writehandle(self), content)


class CircularTraversalError(IOError):
    pass


class LocalFilesystem(Filesystem):

    def __init__(self, rootpath: str):
        super().__init__()
        self.__rootpath = rootpath
        self.__previewers = [lawwenda.previewer.commonimages.CommonImagesPreviewer(),
                             lawwenda.previewer.commonvideos.CommonVideosPreviewer()]
        # TODO text, pdf, libreoffice, audio (without thumbnails though), ... ?!

    def __path_to_fullpath(self, path: str) -> str:
        result = self.sanitize_abspath(f"{self.__rootpath}/{path}")
        if not f"{result}/".startswith(f"{self.__rootpath}/"):
            raise PermissionError(f"path '{path}' is outside of the specified filesystem.")
        return result

    def try_get_fullpath(self, handle, *, writable):
        return self.__path_to_fullpath(handle.writable_node.path if writable else handle.readable_node.path)

    def get_readhandle(self, node):
        return self.ReadHandle(node)

    def get_writehandle(self, node):
        return self.WriteHandle(node)

    def child_nodes(self, handle):
        result = []
        hpath = handle.readable_node.path
        for n in os.listdir(self.__path_to_fullpath(hpath)):
            result.append(self.node_by_path(f"{hpath}/{n}"))
        return result

    def is_hidden(self, handle):
        return handle.readable_node.name.startswith(".")

    def is_dir(self, handle):
        return os.path.isdir(self.__path_to_fullpath(handle.readable_node.path))

    def is_file(self, handle):
        return os.path.isfile(self.__path_to_fullpath(handle.readable_node.path))

    def is_link(self, handle):
        return os.path.islink(self.__path_to_fullpath(handle.readable_node.path))

    def exists(self, handle):
        return os.path.lexists(self.__path_to_fullpath(handle.readable_node.path))

    def size(self, handle):
        return os.path.getsize(self.__path_to_fullpath(handle.readable_node.path))

    def mimetype(self, handle):
        return mimetypes.guess_type(handle.readable_node.name, strict=False)[0] or ""

    def mtime(self, handle):
        nmtime = os.path.getmtime(self.__path_to_fullpath(handle.readable_node.path))
        return datetime.datetime.fromtimestamp(nmtime)

    def has_thumbnail(self, handle):
        if not handle.readable_node.is_file:
            return False
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_thumbnailable(iar):
                    return True
            except Exception:
                logging.error(traceback.format_exc())
        return False

    def has_preview(self, handle):
        if not handle.readable_node.is_file:
            return False
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_previewable(iar):
                    return True
            except Exception:
                logging.error(traceback.format_exc())
        return False

    def comment(self, handle):
        return pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.readable_node.path)).comment()

    def rating(self, handle):
        return pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.readable_node.path)).rating()

    def tags(self, handle):
        return [tg.tagname() for tg in pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(
            handle.readable_node.path)).tags()]

    def geo(self, handle):
        return pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.readable_node.path)).geo()

    def preview_html(self, handle):
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_previewable(iar):
                    return previewer.preview_html(handle.readable_node)
            except Exception:
                logging.error(traceback.format_exc())
        return ""

    def thumbnail(self, handle):
        iar = lawwenda.previewer.IsAbleRequest(handle.readable_node.name, handle.readable_node.mimetype)
        for previewer in self.__previewers:
            try:
                if previewer.is_thumbnailable(iar):
                    return previewer.thumbnail(handle.readable_node)
            except Exception:
                logging.error(traceback.format_exc())
        return b""

    def delete(self, handle):
        hfullpath = self.__path_to_fullpath(handle.writable_node.path)
        if self.is_link:
            os.unlink(hfullpath)
        elif self.is_dir:
            shutil.rmtree(hfullpath)
        else:
            os.unlink(hfullpath)

    def mkdir(self, handle):
        os.makedirs(self.__path_to_fullpath(handle.writable_node.path), exist_ok=True)

    def copy_to(self, srchandle, desthandle):
        # TODO metadata, xattr, ... (also for dirs!)
        # TODO what with links
        srcreadnode = srchandle.readable_node
        destwritenode = desthandle.writable_node
        if srcreadnode.is_dir:
            destwritenode.mkdir()
            for child in srcreadnode.child_nodes:
                self.copy_to(self.get_readhandle(child), self.get_writehandle(destwritenode.child_by_name(child.name)))
        else:
            shutil.copyfile(self.__path_to_fullpath(srcreadnode.path),
                            self.__path_to_fullpath(destwritenode.path))

    def move_to(self, srchandle, desthandle):
        os.rename(self.__path_to_fullpath(srchandle.writable_node.path),
                  self.__path_to_fullpath(desthandle.writable_node.path))

    def set_comment(self, handle, comment):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).set_comment(comment)

    def set_geo(self, handle, geo):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).set_geo(geo)

    def set_rating(self, handle, rating):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).set_rating(rating)

    def add_tag(self, handle, tag):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).add_tag(tagname=tag)

    def remove_tag(self, handle, tag):
        pimetadatainterpreter.get_interpreter(self.__path_to_fullpath(handle.writable_node.path)).remove_tag(tag)

    def read_file(self, handle):
        return open(self.__path_to_fullpath(handle.readable_node.path), "rb")

    def write_file(self, handle, content):
        handle.writable_node.parent_node.mkdir()
        with open(self.__path_to_fullpath(handle.writable_node.path), "wb") as f:
            if isinstance(content, bytes):
                f.write(content)
            else:
                while True:
                    buf = content.read(8096)
                    if len(buf) == 0:
                        break
                    f.write(buf)

    def known_tags(self):
        return ["foo", "bar", "baz"]


# noinspection PyAbstractClass
class AbstractFilesystemDecorator(Filesystem):  # TODO child_nodes broken (e.g. wrong "filesystem")?

    def __init__(self, inner: Filesystem):
        super().__init__()
        self._inner = inner

    def _eval_predicate(self, pred, node):
        return pred(self._inner.node_by_path(node.path))

    def __getattribute__(self, item):
        if (item not in ["_inner", "node_by_path",
                         "rootnode"]) and (not type(self).__dict__.get(item)) and hasattr(self._inner, item):
            return getattr(self._inner, item)
        else:
            return super().__getattribute__(item)


# noinspection PyAbstractClass
class HideNodesFilesystemAdapter(AbstractFilesystemDecorator):

    def __init__(self, inner: Filesystem, pred: FilesystemNodePredicate):
        super().__init__(inner)
        self.__pred = pred

    def is_hidden(self, handle):
        return self._eval_predicate(self.__pred, handle.readable_node) or self._inner.is_hidden(handle)


# noinspection PyAbstractClass
class ExcludeNodesFilesystemAdapter(AbstractFilesystemDecorator):
    # TODO check if all parent dirs are also not excluded?!

    def __init__(self, inner: Filesystem, pred: FilesystemNodePredicate):
        super().__init__(inner)
        self.__pred = pred

    def child_nodes(self, handle: 'Filesystem.ReadHandle') -> t.List['Filesystem.Node']:
        return [n for n in self._inner.child_nodes(handle) if not self._eval_predicate(self.__pred, n)]

    def get_readhandle(self, node):
        if self._eval_predicate(self.__pred, node):
            raise PermissionError(f"no read access for {node.path}")
        return self._inner.get_readhandle(node)  # TODO noh dangerous trap: must not use super() here (better api?!)

    def get_writehandle(self, node):
        if self._eval_predicate(self.__pred, node):
            raise PermissionError(f"no write access for {node.path}")
        return self._inner.get_writehandle(node)


# noinspection PyAbstractClass
class ReadOnlyFilesystemAdapter(AbstractFilesystemDecorator):

    def get_writehandle(self, node):
        raise PermissionError(f"no write access for {node.path}")


class _PredicateFactory:

    # noinspection PyUnusedLocal
    @staticmethod
    def false(node):
        return False

    @staticmethod
    def p_or(*preds):
        def npred(node):
            for pred in preds:
                if pred(node):
                    return True
        return npred

    @staticmethod
    def p_not(pred):
        def npred(node):
            return not pred(node)
        return npred

    @staticmethod
    def p_descending(pred):
        def npred(node):  # TODO cache
            for ccn, _ in node.traverse_dir(raise_on_circle=False):
                if pred(ccn):
                    return True
            return False
        return npred

    @staticmethod
    def p_regexp(restr):
        repat = re.compile(restr)
        def npred(node):
            return bool(repat.fullmatch(node.path))
        return npred

    @staticmethod
    def p_tag(tag):
        def npred(node):
            return tag in node.tags
        return npred


def create_filesystem(rootpath: str, *, readonly: bool, hide_by_patterns: t.Iterable[str] = (),
                      hide_by_tags: t.Iterable[str] = (), include_by_patterns: t.Optional[t.Iterable[str]] = None,
                      include_by_tags: t.Optional[t.Iterable[str]] = None,
                      exclude_by_patterns: t.Iterable[str] = (), exclude_by_tags: t.Iterable[str] = (),
                      exclude_hidden: bool = False) -> Filesystem:
    # TODO xx refactor and test all this scariness
    preds = _PredicateFactory
    fs = LocalFilesystem(rootpath)
    if readonly:
        fs = ReadOnlyFilesystemAdapter(fs)
    hidepred = preds.false
    for hide_by_pattern in hide_by_patterns:
        hidepred = preds.p_or(hidepred, preds.p_regexp(hide_by_pattern))
    for hide_by_tag in hide_by_tags:
        hidepred = preds.p_or(hidepred, preds.p_tag(hide_by_tag))
    if hidepred != preds.false:
        fs = HideNodesFilesystemAdapter(fs, hidepred)
    excludepred = preds.false
    for exclude_by_pattern in exclude_by_patterns:
        excludepred = preds.p_or(excludepred, preds.p_regexp(exclude_by_pattern))
    for exclude_by_tag in exclude_by_tags:
        excludepred = preds.p_or(excludepred, preds.p_tag(exclude_by_tag))
    if (include_by_patterns is not None) or (include_by_tags is not None):
        includepred = preds.false
        for include_by_pattern in include_by_patterns or []:
            includepred = preds.p_or(includepred, preds.p_regexp(include_by_pattern))
        for include_by_tag in include_by_tags or []:
            includepred = preds.p_or(includepred, preds.p_tag(include_by_tag))
        excludepred = preds.p_or(excludepred, preds.p_not(preds.p_descending(includepred)))
    if exclude_hidden:
        def _excludehidden_pred(n):
            return n.is_hidden
        excludepred = preds.p_or(excludepred, _excludehidden_pred)
    if excludepred != preds.false:
        fs = ExcludeNodesFilesystemAdapter(fs, excludepred)
    return fs


"""
# TODO xx
def link_target(self, node: FilesystemNode, *, recursive: bool) -> t.Optional[FilesystemNode]:
    if not node.is_link:
        return node
    lnktgt = os.readlink(self._path_to_fullpath(node.path))
    rlnktgt = os.path.relpath(lnktgt if os.path.isabs(lnktgt) else f"{node.dirpath}/{lnktgt}", self.__rootpath)
    result = self.node(rlnktgt)
    if recursive:
        result = self.link_target(result, recursive=True)
    return result
"""

# TODO xx umask 007 ?!
# TODO i18n
# TODO noh py&js: docstrings
# TODO occassionally crashes (at least with firefox dev tools open)
