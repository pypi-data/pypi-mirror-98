# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import typing as t

import werkzeug.exceptions
import werkzeug.serving
import werkzeug.wsgi

import lawwenda.fmapp
import lawwenda.fs


class Server:

    class _ShareAppInst:

        def __init__(self, share: 'lawwenda.Share'):
            self.__share = share
            self.__app = lawwenda.fmapp.FmApp(share)

        @property
        def app(self) -> 'lawwenda.fmapp.FmApp':
            return self.__app

        @property
        def is_active(self) -> bool:
            s = self.__share
            return s.is_active and (s.configuration.peek_share_cache_tag(s.name) == s.cache_tag)

    def __init__(self, *, cfgpath: t.Optional[str] = None):
        self.__config = lawwenda.Configuration(cfgpath)
        self.__shareapps = {}

    def __get_app_for_share(self, sharename: str):
        shareappinst = self.__shareapps.get(sharename)
        if shareappinst and not shareappinst.is_active:
            shareappinst = self.__shareapps[sharename] = None
        if not shareappinst:
            share = self.__config.get_share_by_name(sharename)
            if share:
                shareappinst = self.__shareapps[sharename] = self._ShareAppInst(share)
        return shareappinst.app if shareappinst else None

    def __call__(self, environ, start_response):
        request = werkzeug.wrappers.Request(environ)
        sharename = werkzeug.wsgi.pop_path_info(request.environ)
        shareapp = self.__get_app_for_share(sharename)
        return (shareapp or werkzeug.exceptions.NotFound())(environ, start_response)
