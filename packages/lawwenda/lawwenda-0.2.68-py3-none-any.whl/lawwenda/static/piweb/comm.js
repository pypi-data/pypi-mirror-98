/**
* @license
* SPDX-FileCopyrightText: © 2021 Josef Hahn
* SPDX-License-Identifier: AGPL-3.0-only
*/


/**
* Error in processing an Ajax request.
*/
export class AjaxError extends Error {

    constructor(url, response) {
        super(`Server request '${url}' failed: ${response.status}`);
        this.response = response;
    }

}

/**
* Makes an Ajax request.
*/
export async function ajax(cfg) {
    cfg.cache = "no-cache";
    cfg.headers = cfg.headers || {};
    var url = cfg.url;
    var method = (cfg.method || "GET").toUpperCase();
    var data = cfg.data || {};
    if (method != "GET") {
        if (data instanceof FormData)
            cfg.body = data;
        else {
            cfg.headers["Content-Type"] = "application/json";
            cfg.body = JSON.stringify(data);
        }
    }
    else {
        var querystrparts = [];
        for (var p in data)
            querystrparts.push(encodeURIComponent(p) + "=" + encodeURIComponent(cfg.data[p]));
        var querystr = querystrparts.join("&");
        if (querystr)
            url += "?" + querystr;
    }
    var answer = await fetch(url, cfg);
    if (!answer.ok)
        throw new AjaxError(cfg.url, answer);
    return answer.json();
}
