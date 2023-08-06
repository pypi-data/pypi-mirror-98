# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import logging
import re
import subprocess
import typing as t
import urllib.parse

import lawwenda._aux.PiMetadataInterpreter.pimetadatainterpreter as pimetadatainterpreter

if t.TYPE_CHECKING:
    import lawwenda.fs
    FilesystemNode = lawwenda.fs.Filesystem.Node
    FilesystemNodes = t.Iterable[FilesystemNode]


def _query_by_tree_traversal(node: 'FilesystemNode',
                             decidefct: t.Callable[['FilesystemNode'], bool]) -> 'FilesystemNodes':
    for n, _ in node.traverse_dir(raise_on_circle=False):
        if decidefct(n):
            yield n


def _termstring_to_termlist(term: str) -> t.List[str]:
    return [ss for ss in [s.strip() for s in term.split(" ")] if ss]


class Search:

    def query(self, node: 'FilesystemNode') -> 'FilesystemNodes':
        raise NotImplementedError()


class DeeplySearch(Search):

    def __init__(self, term: str):
        self.__term = term
        self.__terms = _termstring_to_termlist(term.lower())

    def query(self, node):
        if not self.__terms:
            return []
        idxdata = self.__try_get_index(node)
        return self.__query_indexed(node, idxdata) if idxdata else self.__query_unindexed(node)

    def __try_get_index(self, node: 'FilesystemNode') -> object:
        nodefullpath = node.try_get_fullpath(writable=False)
        if not nodefullpath:
            return None
        try:
            recollans = subprocess.check_output(["recollq", "-m", "-a", "-c", "/data/daemondata/recoll", self.__term],
                                                stderr=subprocess.DEVNULL)
            return recollans, nodefullpath
        except OSError:
            return None

    def __query_indexed(self, node: 'FilesystemNode', idxdata: object) -> 'FilesystemNodes':
        recollans, nodefullpath = idxdata
        nodefullpathlen = len(nodefullpath)
        if not nodefullpath.endswith("/"):
            nodefullpath += "/"
        for line in recollans.split(b"\n"):
            if line.startswith(b"url ="):
                url = line[5:].decode().strip()
                fullpath = urllib.parse.urlparse(url).path
                if fullpath.startswith(nodefullpath):
                    linepath = fullpath[nodefullpathlen:]
                    linenode = node.child_by_name(linepath)
                    if linenode.exists:
                        yield linenode

    def __query_unindexed(self, node: 'FilesystemNode') -> 'FilesystemNodes':
        logging.debug("Searching deeply without recoll index.")
        return _query_by_tree_traversal(node, self.__decide_unindexed)

    def __decide_unindexed(self, node: 'FilesystemNode') -> bool:
        for term in self.__terms:
            if term not in node.name.lower():
                break
        else:
            return True
        for term in self.__terms:
            if term not in node.comment.lower():
                break
        else:
            return True
        for term in self.__terms:
            for tag in node.tags:
                if term in tag.lower():
                    break
            else:
                break
        else:
            return True
        if node.is_file:
            try:
                with node.read_file() as f:
                    fcontenthead = f.read(10 * 1024 ** 2)
                for term in self.__terms:
                    for bterm in [term.encode(), term.encode("utf-16")]:
                        if re.search(re.escape(bterm), fcontenthead, re.IGNORECASE):
                            break
                    else:
                        break
                else:
                    return True
            except IOError as e:
                logging.warning(e)
        return False


class ByNameSearch(Search):

    def __init__(self, term: str):
        self.__terms = _termstring_to_termlist(term.lower())

    def query(self, node):
        if not self.__terms:
            return []
        return _query_by_tree_traversal(node, self.__decide)

    def __decide(self, node: 'FilesystemNode') -> bool:
        for term in self.__terms:
            if term not in node.name.lower():
                return False
        return True


class ByTagSearch(Search):

    def __init__(self, term: str):
        self.__tags = _termstring_to_termlist(term)

    def query(self, node):
        if not self.__tags:
            return []
        return _query_by_tree_traversal(node, self.__decide)

    def __decide(self, node: 'FilesystemNode') -> bool:
        for tag in self.__tags:
            if tag not in node.tags:
                return False
        return True


class ByGeoSearch(Search):

    def __init__(self, position: str, radius: str):
        if position:
            self.__position = pimetadatainterpreter.GeoLocation.from_geostring(position)
            self.__position.set_accuracy_meters(float(radius or 0))
        else:
            self.__position = None

    def query(self, node):
        if not self.__position:
            return []
        return _query_by_tree_traversal(node, self.__decide)

    def __decide(self, node: 'FilesystemNode') -> bool:
        if not node.geo_obj:
            return False
        return self.__position.distance_meters_interval(node.geo_obj)[0] <= 0


def create_search(mode: str, **kwargs) -> Search:
    if mode == "deeply":
        return DeeplySearch(**kwargs)
    elif mode == "byname":
        return ByNameSearch(**kwargs)
    elif mode == "bytag":
        return ByTagSearch(**kwargs)
    elif mode == "bygeo":
        return ByGeoSearch(**kwargs)
    else:
        raise ValueError(f"Invalid mode: {mode}")
