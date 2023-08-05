"""Utilities for communicating with a Tinychain host."""

import json
import logging
import os
import pathlib
import requests
import subprocess
import sys
import time
import urllib.parse

from .error import *
from .util import to_json, uri


DEFAULT_PORT = 8702
ENCODING = "utf-8"


class Host(object):
    """A Tinychain host."""

    @staticmethod
    def encode_params(params):
        return urllib.parse.urlencode({k: json.dumps(v) for k, v in params.items()})

    def __init__(self, address):
        self.__uri__ = address

    def _handle(self, req):
        response = req()
        status = response.status_code
        response = response.text

        if status == 200:
            return json.loads(response)
        elif status == 204:
            return None
        elif status == 400:
            raise BadRequest(response)
        elif status == 401:
            raise Unauthorized(response)
        elif status == 403:
            raise Forbidden(response)
        elif status == 404:
            raise NotFound(response)
        elif status == 405:
            raise MethodNotAllowed(response)
        elif status == 501:
            raise NotImplemented(response)
        else:
            raise UnknownError(f"HTTP error code {status}: {response}")

    def link(self, path):
        """Return a link to the given path at this host."""

        return "http://{}{}".format(uri(self), path)

    def get(self, path, key=None, auth=None):
        """Execute a GET request."""

        url = self.link(path)
        headers = auth_header(auth)
        if key:
            key = json.dumps(to_json(key)).encode(ENCODING)
            request = lambda: requests.get(url, params={"key": key}, headers=headers)
        else:
            request = lambda: requests.get(url, headers=headers)

        return self._handle(request)

    def put(self, path, key, value, auth=None):
        """Execute a PUT request."""

        url = self.link(path)
        headers = auth_header(auth)
        key = json.dumps(to_json(key)).encode(ENCODING)
        value = json.dumps(to_json(value)).encode(ENCODING)
        request = lambda: requests.put(url, params={"key": key}, data=value, headers=headers)

        return self._handle(request)

    def post(self, path, data={}, auth=None):
        """Execute a POST request."""

        url = self.link(path)
        data = json.dumps(to_json(data)).encode(ENCODING)
        headers = auth_header(auth)
        request = lambda: requests.post(url, data=data, headers=headers)

        return self._handle(request)

    def delete(self, path, key=None, auth=None):
        """Execute a DELETE request."""

        url = self.link(path)
        headers = auth_header(auth)
        if key:
            key = json.dumps(to_json(key)).encode(ENCODING)
            request = lambda: requests.delete(url, params={"key": key}, headers=headers)
        else:
            request = lambda: requests.delete(url, headers=headers)

        return self._handle(request)

    def resolve(self, state, auth=None):
        """Resove the given state."""

        return self.post("/transact/execute", state, auth)


class Local(Host):
    """A local Tinychain host."""

    ADDRESS = "127.0.0.1"
    STARTUP_TIME = 0.5

    def __init__(self,
            path,
            workspace,
            data_dir=None,
            clusters=[],
            port=DEFAULT_PORT,
            log_level="warn",
            force_create=False):

        # set _process first so it's available to __del__ in case of an exception
        self._process = None

        if port is None or not int(port) or int(port) < 0:
            raise ValueError(f"invalid port: {port}")

        if clusters and data_dir is None:
            raise ValueError("Hosting a cluster requires specifying a data_dir")

        maybe_create_dir(workspace, force_create)

        if data_dir:
            maybe_create_dir(data_dir, force_create)

        address = "{}:{}".format(self.ADDRESS, port)
        Host.__init__(self, address)

        args = [
            path,
            f"--http_port={port}",
            f"--log_level={log_level}",
        ]

        if data_dir:
            args.append(f"--data_dir={data_dir}")

        args.extend([f"--cluster={cluster}" for cluster in clusters])

        self._args = args

    def start(self):
        if self._process:
            raise RuntimeError("tried to start a host that's already running")

        self._process = subprocess.Popen(self._args)        
        time.sleep(self.STARTUP_TIME)

        if self._process is None or self._process.poll() is not None:
            raise RuntimeError(f"Tinychain process at {uri(self)} crashed on startup")
        else:
            logging.info(f"new instance running at {uri(self)}")

    def stop(self):
        """Shut down this host."""

        logging.info(f"Shutting down Tinychain host {uri(self)}")
        self._process.terminate()
        self._process.wait()
        logging.info(f"Host {uri(self)} shut down successfully")
        self._process = None

    def __del__(self):
        if self._process:
            self.stop()


def auth_header(token):
    return {"Authorization": f"Bearer {token}"} if token else {}


def maybe_create_dir(path, force):
    path = pathlib.Path(path)
    if path.exists() and path.is_dir():
        return
    elif force:
        os.makedirs(path)
    else:
        raise RuntimeError(f"no directory at {path}")

