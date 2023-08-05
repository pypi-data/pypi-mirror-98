# -*- coding: utf-8 -*-

"""
Copyright (c) 2018 Keijack Wu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import threading
import inspect
import importlib
import re
import ssl as _ssl

from typing import Dict

import simple_http_server.http_server as http_server

from simple_http_server import _get_filters, _get_request_mappings, _get_websocket_handlers, _get_error_pages
from simple_http_server import request_map
from simple_http_server import StaticFile
from simple_http_server.logger import get_logger


__logger = get_logger("simple_http_server.server")
__lock = threading.Lock()
_server = None


def _is_match(string="", regx=r""):
    if not regx:
        return True
    pattern = re.compile(regx)
    match = pattern.match(string)
    return True if match else False


def _to_module_name(fpath="", regx=r""):
    fname, fext = os.path.splitext(fpath)

    if fext != ".py":
        return
    mname = fname.replace(os.path.sep, '.')
    if _is_match(fpath, regx) or _is_match(fname, regx) or _is_match(mname, regx):
        return mname


def _load_all_modules(work_dir, pkg, regx):
    abs_folder = work_dir + "/" + pkg
    all_files = os.listdir(abs_folder)
    modules = []
    folders = []
    for f in all_files:
        if os.path.isfile(os.path.join(abs_folder, f)):
            mname = _to_module_name(os.path.join(pkg, f), regx)
            if mname:
                modules.append(mname)
        elif f != "__pycache__":
            folders.append(os.path.join(pkg, f))

    for folder in folders:
        modules += _load_all_modules(work_dir, folder, regx)
    return modules


def _import_module(mname):
    try:
        importlib.import_module(mname)
    except:
        __logger.warning(f"Import moudle [{mname}] error!")


def scan(base_dir: str = "", regx: str = r"", project_dir: str = "") -> None:
    if project_dir:
        work_dir = project_dir
    else:
        ft = inspect.currentframe()
        fts = inspect.getouterframes(ft)
        entrance = fts[-1]
        work_dir = os.path.dirname(inspect.getabsfile(entrance[0]))
    modules = _load_all_modules(work_dir, base_dir, regx)

    for mname in modules:
        __logger.info(f"Import controllers from module: {mname}")
        _import_module(mname)


def start(host: str = "",
          port: int = 9090,
          ssl: bool = False,
          ssl_protocol: int = _ssl.PROTOCOL_TLS_SERVER,
          ssl_check_hostname: bool = False,
          keyfile: str = "",
          certfile: str = "",
          keypass: str = "",
          ssl_context: _ssl.SSLContext = None,
          resources: Dict[str, str] = {}) -> None:
    with __lock:
        global _server
        if _server is not None:
            _server.shutdown()
        _server = http_server.SimpleDispatcherHttpServer(host=(host, port),
                                                         ssl=ssl,
                                                         ssl_protocol=ssl_protocol,
                                                         ssl_check_hostname=ssl_check_hostname,
                                                         keyfile=keyfile,
                                                         certfile=certfile,
                                                         keypass=keypass,
                                                         ssl_context=ssl_context,
                                                         resources=resources)

    filters = _get_filters()
    # filter configuration
    for ft in filters:
        _server.map_filter(ft["url_pattern"], ft["func"])

    request_mappings = _get_request_mappings()
    # request mapping
    for ctr in request_mappings:
        _server.map_request(ctr)

    ws_handlers = _get_websocket_handlers()

    for endpoint, clz in ws_handlers.items():
        _server.map_websocket_handler(endpoint, clz)

    err_pages = _get_error_pages()
    for code, func in err_pages.items():
        _server.map_error_page(code, func)

    # start the server
    _server.start()


def is_ready() -> bool:
    return _server and _server.ready


def stop() -> None:
    with __lock:
        global _server
        if _server is not None:
            __logger.info("shutting down server...")
            _server.shutdown()
            _server = None


@request_map("/favicon.ico")
def _favicon():
    root = os.path.dirname(os.path.abspath(__file__))
    return StaticFile(f"{root}/favicon.ico", "image/x-icon")
