# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import base64
import datetime
import hashlib
import json
import os
import socket
import sys
import time
import typing as t

import werkzeug.serving

import lawwenda.datafiles
import lawwenda.server


class Share:

    def __init__(self, path: str, *, configuration: 'Configuration', name: str, title: str, readonly: bool = True,
                 hide_by_patterns: t.Iterable[str] = (), hide_by_tags: t.Iterable[str] = (),
                 include_by_patterns: t.Optional[t.Iterable[str]] = None,
                 include_by_tags: t.Optional[t.Iterable[str]] = None,
                 exclude_by_patterns: t.Iterable[str] = (), exclude_by_tags: t.Iterable[str] = (),
                 exclude_hidden: bool = False,
                 password_scrypt: t.Optional[str] = None, password_salt: t.Optional[str] = None,
                 active_until_timestamp: t.Optional[float] = None):
        self.__path = os.path.abspath(path)
        self.__configuration = configuration
        self.__name = name
        self.__title = title
        self.__readonly = readonly
        self.__hide_by_patterns = hide_by_patterns
        self.__hide_by_tags = hide_by_tags
        self.__include_by_patterns = include_by_patterns
        self.__include_by_tags = include_by_tags
        self.__exclude_by_patterns = exclude_by_patterns
        self.__exclude_by_tags = exclude_by_tags
        self.__exclude_hidden = exclude_hidden
        self.__password_scrypt = password_scrypt or None
        self.__password_salt = password_salt
        self.__active_until_timestamp = active_until_timestamp
        self.__cache_tag = None

    @property
    def path(self) -> str:
        return self.__path

    @property
    def name(self) -> str:
        return self.__name

    @property
    def configuration(self) -> 'Configuration':
        return self.__configuration

    @property
    def title(self) -> str:
        return self.__title

    @property
    def readonly(self) -> bool:
        return self.__readonly

    @property
    def hide_by_patterns(self) -> t.Iterable[str]:
        return self.__hide_by_patterns

    @property
    def hide_by_tags(self) -> t.Iterable[str]:
        return self.__hide_by_tags

    @property
    def include_by_patterns(self) -> t.Iterable[str]:
        return self.__include_by_patterns

    @property
    def include_by_tags(self) -> t.Iterable[str]:
        return self.__include_by_tags

    @property
    def exclude_by_patterns(self) -> t.Iterable[str]:
        return self.__exclude_by_patterns

    @property
    def exclude_by_tags(self) -> t.Iterable[str]:
        return self.__exclude_by_tags

    @property
    def exclude_hidden(self) -> bool:
        return self.__exclude_hidden

    @property
    def password_scrypt(self) -> t.Optional[str]:
        return self.__password_scrypt

    @property
    def password_salt(self) -> t.Optional[str]:
        return self.__password_salt

    @property
    def active_until(self) -> t.Optional[datetime.datetime]:
        return datetime.datetime.fromtimestamp(self.active_until_timestamp) if self.active_until_timestamp else None

    @property
    def active_until_timestamp(self) -> t.Optional[float]:
        return self.__active_until_timestamp

    @property
    def is_active(self) -> bool:
        return (self.active_until_timestamp is None) or (self.active_until_timestamp >= time.time())

    @property
    def cache_tag(self) -> object:
        return self.__cache_tag

    def __str__(self):
        return (f"Share {self.name}\n"
                f"- path: {self.path}\n"
                f"- title: {self.title}\n"
                f"- readonly: {self.readonly}\n"
                f"- active until timestamp: {self.active_until_timestamp}\n"
                f"- hide by patterns: {self.hide_by_patterns}\n"
                f"- hide by tags: {self.hide_by_tags}\n"
                f"- include by patterns: {self.include_by_patterns}\n"
                f"- include by tags: {self.include_by_tags}\n"
                f"- exclude by patterns: {self.exclude_by_patterns}\n"
                f"- exclude by tags: {self.exclude_by_tags}\n"
                f"- exclude hidden: {self.exclude_hidden}\n"
                f"- password protected: {bool(self.password_scrypt)}\n")

    def _set_cache_tag(self, t: object) -> None:
        self.__cache_tag = t

    def _to_dict(self):
        return {k: getattr(self, k) for k in ["path", "name", "title", "readonly",
                                              "hide_by_patterns", "hide_by_tags", "include_by_patterns",
                                              "include_by_tags", "exclude_by_patterns", "exclude_by_tags",
                                              "exclude_hidden", "password_scrypt", "password_salt",
                                              "active_until_timestamp"]}


class Configuration:

    def __init__(self, cfgpath: t.Optional[str] = None):
        self.__cfgpath = cfgpath or "/etc/lawwenda"
        self.__cfgsharespath = f"{self.__cfgpath}/shares"

    @property
    def path(self) -> str:
        return self.__cfgpath

    def __str__(self):
        return f"Configuration in {self.path!r}"

    def peek_share_cache_tag(self, name: str) -> t.Optional[object]:
        try:
            return os.stat(f"{self.__cfgsharespath}/{name}").st_mtime
        except OSError:
            return None

    def get_shares(self) -> t.List[Share]:
        if not os.path.isdir(self.__cfgsharespath):
            return []
        result = None
        tnow = time.time()
        itries = 0
        while result is None:
            itries += 1
            try:
                result_ = []
                for name in os.listdir(self.__cfgsharespath):
                    cachetag = self.peek_share_cache_tag(name)
                    if not cachetag:
                        raise OSError("No cachetag.")
                    with open(f"{self.__cfgsharespath}/{name}", "r") as f:
                        sharedict = json.load(f)
                    if cachetag != self.peek_share_cache_tag(name):
                        raise OSError("cachetag changed.")
                    share = Share(**sharedict, configuration=self)
                    # noinspection PyProtectedMember
                    share._set_cache_tag(cachetag)
                    if share.is_active:
                        result_.append(share)
                    else:
                        self.remove_share(share.name)
                result = result_
            except IOError as e:
                if (time.time() - tnow > 10) and (itries > 100):
                    raise e
        return result

    def get_share_by_name(self, name: str) -> t.Optional[Share]:
        for share in self.get_shares():
            if share.name == name:
                return share

    def add_share(self, path: str, *, name: str, password: t.Optional[str],
                  title: t.Optional[str] = None, readonly: bool = True,
                  hide_by_patterns: t.Iterable[str] = (), hide_by_tags: t.Iterable[str] = (),
                  include_by_patterns: t.Optional[t.Iterable[str]] = None,
                  include_by_tags: t.Optional[t.Iterable[str]] = None,
                  exclude_by_patterns: t.Iterable[str] = (), exclude_by_tags: t.Iterable[str] = (),
                  exclude_hidden: bool = False,
                  active_until: t.Optional[datetime.datetime] = None) -> Share:
        self.__verify_valid_name(name)
        if password:
            pwsalt = os.urandom(16)
            pwscrypt = hashlib.scrypt(password.encode(), salt=pwsalt, n=2**14, r=8, p=1)
            password_scrypt = base64.b64encode(pwscrypt).decode()
            password_salt = base64.b64encode(pwsalt).decode()
        else:
            password_scrypt = password_salt = None
        share = Share(path, configuration=self, name=name, title=title or name, readonly=readonly,
                      hide_by_patterns=hide_by_patterns, hide_by_tags=hide_by_tags,
                      include_by_patterns=include_by_patterns, include_by_tags=include_by_tags,
                      exclude_by_patterns=exclude_by_patterns, exclude_by_tags=exclude_by_tags,
                      exclude_hidden=exclude_hidden, password_scrypt=password_scrypt, password_salt=password_salt,
                      active_until_timestamp=active_until.timestamp() if active_until else None)
        os.makedirs(self.__cfgsharespath, exist_ok=True)
        # noinspection PyProtectedMember
        jshare = json.dumps(share._to_dict())
        if self.get_share_by_name(name):
            raise ValueError(f"The name '{name}' is already in use.")
        with open(f"{self.__cfgsharespath}/{name}", "w") as f:
            f.write(jshare)
        return self.get_share_by_name(name)

    def remove_share(self, name: str) -> None:
        self.__verify_valid_name(name)
        fp = f"{self.__cfgsharespath}/{name}"
        try:
            os.unlink(fp)
        except IOError:
            if os.path.exists(fp):
                raise

    def run_dev_server(self) -> None:
        for port in range(49152, 65536):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(("localhost", port)):
                    break
        else:
            raise RuntimeError("No free tcp port found")
        print("Please use the server address mentioned later with your share name appended.\n"
              "The server will block this console. Feel free to open another one as needed.")
        sys.stdout.flush()
        werkzeug.serving.run_simple("localhost", port, lawwenda.server.Server(cfgpath=self.__cfgpath),
                                    processes=1, threaded=True)

    def generate_wsgi(self) -> str:
        fwsgi = lawwenda.datafiles.find_data_file("lawwenda.wsgi")
        if not fwsgi:
            raise EnvironmentError("Your installation is not able to generate wsgi.")
        with open(fwsgi, "r") as f:
            return f.read().format(lawwendadir=repr(lawwenda.datafiles.lawwendadir), cfgpath=repr(self.path))

    @staticmethod
    def __verify_valid_name(name: str) -> None:
        if (not name) or name != os.path.basename(name):
            raise ValueError(f"Invalid share name '{name}'")


# TODO nice __str__ in some (more) classes for console; also __repr__ (easier on console) ?!
