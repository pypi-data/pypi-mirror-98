# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import json
import typing as t

import werkzeug.wrappers.json
import werkzeug.wsgi


class Request(werkzeug.wrappers.Request, werkzeug.wrappers.json.JSONMixin):
    pass


class JsonedResponse(werkzeug.wrappers.Response):

    def __init__(self, data: t.Optional[t.Any], **kwargs):
        super().__init__(json.dumps(data), mimetype="application/json", **kwargs)
