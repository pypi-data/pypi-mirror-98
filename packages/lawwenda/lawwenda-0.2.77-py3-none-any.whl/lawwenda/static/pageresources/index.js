/**
* @license
* SPDX-FileCopyrightText: © 2021 Josef Hahn
* SPDX-License-Identifier: AGPL-3.0-only
*/

import {backend, relativePathByRefPath, sanitizePath, urlInternalsName} from '../backend/common.js';
import {addNotification} from '../components/notification.js';
import {choiceDialog, confirmationYesNoMessageDialog, inputDialog, messageDialog} from '../piweb/conversationdialog.js';


var locationbar = document.getElementById("locationbar");
var dirview = document.getElementById("dirview");
var detailspanel = document.getElementById("detailspanel");
var mainmenu = document.getElementById("mainmenu");
var searchouter = document.getElementById("searchouter");

const rootname = document.body.getAttribute("data-rootname");

function gotoDir(path, skipPushHistory) {
    path = sanitizePath(path);
    if (!skipPushHistory && dirview.path?.__proto__) {
        var newUrl = relativePathByCurrentDir(path) + "/";
        if (newUrl != "/")
            window.history.pushState({path: path}, "", newUrl + document.location.search);
    }
    dirview.path = path;
    locationbar.path = path;
    detailspanel.path = undefined;
    document.title = (path == "") ? rootname : `${rootname}: ${path}`;
}

function refresh() {
    gotoDir(dirview.path);
}

export function relativePathByCurrentDir(path) {
    return relativePathByRefPath(path, dirview.path);
}

const _args = new URLSearchParams(document.location.search);

function getArgument(key) {
    return _args.get(key);
}

function setArgument(key, value) {
    var prms = new URLSearchParams(document.location.search);
    if (value === undefined)
        prms.delete(key);
    else
        prms.set(key, value);
    var search = prms.toString();
    if (search)
        search = "?" + search;
    document.location.search = search;
}

function getArgumentBoolean(key) {
    return _args.has(key);
}

function setArgumentBoolean(key, value) {
    setArgument(key, value?"":undefined);
}

function setHiddenFilesVisible(value) {
    setArgumentBoolean("reveal_hidden", value);
}

function isHiddenFilesVisible() {
    return getArgumentBoolean("reveal_hidden");
}

function setSmallRows(value) {
    setArgumentBoolean("small_rows", value);
}

function isSmallRows() {
    return getArgumentBoolean("small_rows");
}

class SearchManager {

    startSearch(config) {
        this.stopSearch();
        var self = this;
        var searchpanel = this._searchpanel = document.createElement("lawwenda-searchpanel");
        searchpanel.expanded = true;
        searchpanel.addEventListener("close", () => {
            self.stopSearch();
        });
        searchpanel.addEventListener("changed", () => {
            self._fireSearch(searchpanel.configDict);
        });
        searchouter.appendChild(searchpanel);
        if (config) {
            searchpanel.configDict = config;
            this.collapseSearch();
        }
        self._fireSearch(searchpanel.configDict);
    }

    stopSearch() {
        this._searchpanel = undefined;
        searchouter.innerHTML = "";
        this._fireSearch(undefined);
    }

    get isSearchOpen() {
        return searchouter.children.length > 0;
    }

    collapseSearch() {
        if (this._searchpanel)
            this._searchpanel.expanded = false;
    }

    expandSearch() {
        if (this._searchpanel)
            this._searchpanel.expanded = true;
    }

    _fireSearch(config) {
        dirview.searchConfig = config ? JSON.stringify(config) : "";
    }

}

const searchManager = new SearchManager();

function setSortConfig(column, descending) {
    if (column == "name" && !descending)
        var sortstr = undefined;
    else {
        var sortstr = column;
        if (descending)
            sortstr += " desc";
    }
    setArgument("sort", sortstr);
}

function getSortConfig() {
    var column = "name";
    var descending = false;
    var sortstr = getArgument("sort");
    if (sortstr) {
        if (sortstr.endsWith(" desc")) {
            descending = true;
            column = sortstr.substring(0, sortstr.length-5);
        }
        else
            column = sortstr;
    }
    return {column: column, descending: descending};
}

function globbingPatternToRegExp(globpat) {
    var repat = "";
    for (let char of globpat) {
        if (char == "*")
            repat += ".*";
        else if (char == "?")
            repat += ".";
        else
            repat += (".?+*^$|({[\\".includes(char) ? "\\" : "") + char;
    }
    return new RegExp("^"+repat+"$", "i");
}

//TODO set all "dirview" config in one step (less http requests fired in background)?

mainmenu.querySelector("[value=revealhidden]").checked = dirview.isHiddenFilesVisible = isHiddenFilesVisible();

dirview.sortColumn = getSortConfig().column;
dirview.sortDescending = getSortConfig().descending;

mainmenu.querySelector("[value=smallrows]").checked = isSmallRows();
if (isSmallRows())
    document.body.classList.add("smallrows");

var initialpath = document.body.getAttribute("data-initialpath");

gotoDir(initialpath);

window.addEventListener("popstate", (event) => {
    gotoDir(event.state ? event.state.path : initialpath, true);
});

locationbar.addEventListener("pathSelected", (event) => {
    gotoDir(event.detail.path);
});

dirview.addEventListener("pathSelected", (event) => {
    gotoDir(event.detail.path);
});

detailspanel.addEventListener("pathSelected", async (event) => {
    gotoDir(event.detail.paths[0]);
});

dirview.addEventListener("openFile", (event) => {
    window.open(relativePathByCurrentDir(event.detail.path));
});

dirview.addEventListener("entriesSelected", (event) => {
    detailspanel.paths = event.detail.paths;
});

dirview.addEventListener("uploadEntries", async (event) => {
    await backend.upload(event.detail.files, event.detail.destpath);
    refresh();
});

mainmenu.addEventListener("sl-select", async (event) => {
    var action = event.detail.item.value;
    if (action == "newdir") {
        var dirname = await inputDialog({message: "Please enter the new directory name."});
        if (!dirname)
            return;
        await backend.createDirectory(`${dirview.path}/${dirname}`);
        refresh();
    }
    else if (action == "upload") {
        var uploaderform = document.createElement("form");
        uploaderform.action = "";
        uploaderform.method = "POST";
        var uploader = document.createElement("input");
        uploader.type = "file";
        uploader.multiple = true;
        uploader.addEventListener("change", async (event) => {
            await backend.upload(uploader.files, dirview.path);
            refresh();
        });
        uploader.click();
    }
    else if (action == "search") {
        if (searchManager.isSearchOpen)
            searchManager.stopSearch();
        else
            searchManager.startSearch();
    }
    else if (action == "sort") {
        var sortcols = ["name", "size", "modification time"];
        var isortcol = await choiceDialog({message: "Please choose a sort criterion.", choices: sortcols});
        if (isortcol === undefined)
            return;
        var sortords = ["ascending", "descending"];
        var isortord = await choiceDialog({message: "Please choose a sort order.", choices: sortords});
        if (isortord === undefined)
            return;
        setSortConfig(["name", "size", "mtime"][isortcol], isortord == 1);
    }
    else if (action == "revealhidden")
        setHiddenFilesVisible(!isHiddenFilesVisible());
    else if (action == "smallrows")
        setSmallRows(!isSmallRows());
    else if (action == "select") {
        var isel = await choiceDialog({message: "Please choose which elements to select.",
                                       choices: ["all", "none", "invert current", "by name pattern"]});
        if (isel === undefined)
            return;
        var doselectcheck;
        var nowselected = dirview.selectedEntries;
        if (isel == 0)
            doselectcheck = () => true;
        else if (isel == 1)
            doselectcheck = () => false;
        else if (isel == 2)
            doselectcheck = (entry) => !nowselected.includes(entry);
        else if (isel == 3) {
            var msg = "Please enter a file name pattern to select.\n\n"
                    + "Each '*' matches none, one or many characters. Each '?' matches one character. "
                    + "Matching will be case insensitive.";
            var globpat = await inputDialog({message: msg, defaultAnswer: "*.mp3"});
            if (globpat === undefined)
                return;
            var reglob = globbingPatternToRegExp(globpat);
            doselectcheck = (entry) => entry.name.match(reglob);
        }
        else
            throw new Error(`Invalid isel: ${isel}`);
        dirview.resetSelection();
        for (let entry of dirview.allEntries) {
            if (doselectcheck(entry))
                dirview.addEntryToSelection(entry);
        }
        //TODO noh refresh details panel
    }
    else if (action == "help")
        window.open(`${urlInternalsName}/help`);
});

detailspanel.addEventListener("downloadzip", async (event) => {
    var paths = dirview.selectedEntries.map(x => x.path);
    window.open(await backend.zipEntries(paths));
});

detailspanel.addEventListener("copy", async (event) => {
    _doCopyMove("copy");
});

detailspanel.addEventListener("move", async (event) => {
    _doCopyMove("move");
});

function _doCopyMove(action) {
    var ntfpiece = document.createElement("lawwenda-notificationpiece-copymove");
    var selectedEntries = dirview.selectedEntries;
    ntfpiece.label = selectedEntries[0].name;
    if (selectedEntries.length > 1)
        ntfpiece.label = `${ntfpiece.label} & ${selectedEntries.length-1} more`;
    ntfpiece.action = `${action} to here`;
    var ntf = addNotification(ntfpiece);
    var srcpaths = selectedEntries.map(x => x.path);
    ntfpiece.addEventListener("cancel", () => {
        ntf.close();
    });
    ntfpiece.addEventListener("trigger", async () => {
        ntf.close();
        await backend[{"copy": "copyEntries", "move": "moveEntries"}[action]](srcpaths, dirview.path);
        refresh();
    });
}

detailspanel.addEventListener("rename", async (event) => {
    var entry = dirview.selectedEntries[0];
    var newname = await inputDialog({message: "Please enter the new name.", defaultAnswer: entry.name});
    if (!newname)
        return;
    await backend.renameEntry(entry.path, newname);
    refresh();
});

detailspanel.addEventListener("delete", async (event) => {
    if (dirview.selectedEntries.length == 1)
        var q = `Do you really want to remove '${dirview.selectedEntries[0].name}'?`;
    else
        var q = `Do you really want to remove the selected ${dirview.selectedEntries.length} entries?`;
    if (!await confirmationYesNoMessageDialog({message: q}))
        return;
    await backend.deleteEntries(dirview.selectedPaths);
    refresh();
});

detailspanel.addEventListener("changecomment", async (event) => {
    if (dirview.selectedEntries.length == 1)
        var dc = (await backend.entryDetails(dirview.selectedEntries[0].path)).comment;
    else
        var dc = "";
    var newcomment = await inputDialog({message: "Please enter a comment.", defaultAnswer: dc});
    if (!newcomment)
        return;
    await backend.commentEntries(dirview.selectedPaths, newcomment);
    refresh();
});

detailspanel.addEventListener("addtag", async (event) => {
    var tags = await backend.knownTags();  // TODO cache a bit?!
    if (dirview.selectedEntries.length == 1)
        var q = `Please choose the tag to add to '${dirview.selectedEntries[0].name}'.`;
    else
        var q = `Please choose the tag to add to the selected ${dirview.selectedEntries.length} entries.`;
    var newtag = await inputDialog({message: q});  //TODO auto completion?! (also in tag search)
    if (!newtag)
        return;
    backend.addTagToEntries(dirview.selectedPaths, newtag);
    refresh();
});

detailspanel.addEventListener("removetag", async (event) => {
    if (dirview.selectedEntries.length == 1) {
        var entry = dirview.selectedEntries[0];
        var tags = (await backend.entryDetails(entry.path)).tags;
        var q = `Please choose the tag to remove from '${entry.name}'.`;
    }
    else {
        var tags = await backend.knownTags();
        var q = `Please choose the tag to remove from the selected ${dirview.selectedEntries.length} entries.`;
    }
    var rmtag = await choiceDialog({message: q, choices: tags});
    if (rmtag === undefined)
        return;
    backend.removeTagFromEntries(dirview.selectedPaths, tags[rmtag]);
    refresh();
});

detailspanel.addEventListener("browsetag", async (event) => {
    searchManager.startSearch({mode: "bytag", term: event.detail.tag});  // TODO not only in the current dir
});

detailspanel.addEventListener("changegeo", async (event) => {
    var pnlchangegeo = document.createElement("div");
    var map = document.createElement("piweb-map");
    map.style.height = "10rem";
    map.zoomLevel = 0;
    var pnlaccuracy = document.createElement("div");
    pnlaccuracy.style.marginTop = "0.25rem";
    pnlaccuracy.append("Accuracy: ");
    var edtaccuracy = document.createElement("sl-input");
    edtaccuracy.size = "small";
    edtaccuracy.style.width = "10rem";
    var sufedtaccuracy = document.createElement("div");
    sufedtaccuracy.textContent = "meters";
    sufedtaccuracy.slot = "suffix";
    edtaccuracy.appendChild(sufedtaccuracy);
    edtaccuracy.style.display = "inline-block";
    pnlaccuracy.appendChild(edtaccuracy);
    edtaccuracy.value = "0";
    pnlchangegeo.appendChild(map);
    pnlchangegeo.appendChild(pnlaccuracy);
    var _marker;
    async function setmarker(pos) {
        if (_marker)
            _marker.remove();
        _marker = await map.addMarker(pos);
    }
    map.addEventListener("locationpicked", (event) => {
        setmarker(event.detail.location);
    });
    if (dirview.selectedEntries.length == 1) {
        var entry = await backend.entryDetails(dirview.selectedEntries[0].path);
        var q = `Please choose the geo location of '${entry.name}'.`;
        if (entry.geo) {
            map.position = entry.geo;
            setTimeout(()=>{
                setmarker(entry.geo);
            }, 0);
            map.zoomLevel = 14;
            edtaccuracy.value = new URLSearchParams(entry.geo).get("acc") || edtaccuracy.value;
        }
    }
    else
        var q = `Please choose the geo location of the selected ${dirview.selectedEntries.length} entries.`;
    if (await messageDialog({message: q, buttons: ["Cancel", "OK"], contentnodes: [pnlchangegeo],
                             defaultCancelAnswer: 0, defaultAcceptAnswer: 1}) == 0)
        return;
    var geostr = "";
    if (_marker) {
        var geodict = {acc: parseFloat(edtaccuracy.value)};
        for(const [k, v] of new URLSearchParams(_marker.position.toValueString()).entries())
            geodict[k] = v;
        geostr = new URLSearchParams(geodict).toString();
    }
    await backend.setEntriesGeo(dirview.selectedPaths, geostr);
    refresh();
});

detailspanel.addEventListener("changerating", async (event) => {
    if (dirview.selectedEntries.length > 1)
        if (!await confirmationYesNoMessageDialog({
            message: `Do you really want to rate the selected ${dirview.selectedEntries.length} entries?`
        }))
            return;
    await backend.rateEntries(dirview.selectedPaths, event.detail.rating);
    refresh();
});

detailspanel.addEventListener("resizepanel", async (event) => {
    document.body.classList.toggle("fullsizedetails"); // TODO seems broken -> test preview  (in large and small window)
    //TODO automatically collapse again in some situations (e.g. when nothing is selected at all and you cant disable it at all?)
});

detailspanel.addEventListener("selectpreviousentry", async (event) => {
    dirview.selectEntryByOffset(-1);
});

detailspanel.addEventListener("selectnextentry", async (event) => {
    dirview.selectEntryByOffset(+1);
});

//TODO map in search panel is broken until manual window resize
//TODO fix last searching glitches: dont show dirs? show full path in entries instead? ...?
//TODO flickering on selection change
//TODO sort tags: indirect first
//TODO keyboard
//TODO opening a file opens a url with the `?...` crap included
