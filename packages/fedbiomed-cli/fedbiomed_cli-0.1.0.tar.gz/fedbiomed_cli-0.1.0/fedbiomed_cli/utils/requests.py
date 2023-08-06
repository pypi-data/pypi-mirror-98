import os
import uuid
from collections import OrderedDict


class MultipartFileEncoder(object):

    def __init__(self, field, fp, filename=None, boundary=None, headers=None):
        self.field = field
        self.fp = fp
        self.filename = filename
        self.boundary = (boundary or uuid.uuid4().hex).encode('ascii')
        self.content_type = b'multipart/form-data; boundary=' + self.boundary

        headers = dict(headers or {})

        if 'Content-Disposition' not in headers:
            disposition = 'form-data; name="{}"'.format(self.field)
            if self.filename:
                disposition += '; filename="{}"'.format(self.filename)
            headers['Content-Disposition'] = disposition

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/octet-stream'

        self.headers = b'\r\n'.join('{}: {}'.format(k, v).encode('ascii') for k, v in headers.items())

    def compute_size(self, include_final_boundary=True):
        pos = self.fp.tell()
        self.fp.seek(0, os.SEEK_END)
        size = self.fp.tell()
        self.fp.seek(pos)
        size += len(self.boundary) + 4 + 4 + len(self.headers) + 2
        if include_final_boundary:
            size += 6 + len(self.boundary)
        return size

    def iter_encode(self, include_final_boundary=True, chunksize=8096):
        yield b'--'
        yield self.boundary
        yield b'\r\n'

        yield self.headers
        yield b'\r\n'
        yield b'\r\n'

        # TODO: Check if boundary value occurs in data body.
        while True:
            data = self.fp.read(chunksize)
            if not data: break
            yield data

        yield b'\r\n'

        if include_final_boundary:
            yield b'--'
            yield self.boundary
            yield b'--\r\n'


class GeneratorFileReader(object):

    def __init__(self, gen):
        self.gen = gen
        self.buffer = b''

    def readable(self):
        return True

    def read(self, n=None):
        if n is None:
            res = self.buffer + b''.join(self.gen)
            self.buffer = b''
            return res
        elif n <= 0:
            return b''
        else:
            res = b''
            while n > 0:
                part = self.buffer[:n]
                res += part
                self.buffer = self.buffer[n:]
                n -= len(part);
                assert n >= 0
                if not self.buffer:
                    try:
                        self.buffer = next(self.gen)
                    except StopIteration:
                        break
                else:
                    break
            return res


class FileMonitor(object):

    def __init__(self, fp, callback=None):
        self.fp = fp
        self.bytes_read = 0
        self.callback = callback

    def __getattr__(self, key):
        return getattr(self.fp, key)

    def read(self, n):
        res = self.fp.read(n)
        self.bytes_read += len(res)
        if self.callback:
            self.callback(self)
        return res


def stream_file(fp, chunksize=8192):
    while True:
        data = fp.read(chunksize)
        if data:
            yield data
        else:
            break


def encode_file(file_path, params={}):
    filename = os.path.basename(file_path)
    fp = open(file_path, 'rb')

    encoder = MultipartFileEncoder('file', fp, filename=filename)
    stream = GeneratorFileReader(encoder.iter_encode())
    headers = {'Content-Type': encoder.content_type}

    return {'headers': headers, 'data': stream_file(stream), 'params': params}


import io
import torch
import tempfile
import requests


def upload_model_params_fileio(params: OrderedDict):
    with tempfile.NamedTemporaryFile(suffix='.pt') as fp:
        model_io = io.BytesIO()
        torch.save(params, model_io)

        request_kwargs = encode_file(fp.name)
        res = requests.post('https://file.io', **request_kwargs)

        return res.json()


import uuid
from .. import UPLOADS_URL


def upload(params):
    model_io = io.BytesIO()
    torch.save(params, model_io)

    filename = f'{uuid.uuid4()}.pt'
    files = {'file': (filename, model_io.getvalue())}

    res = requests.post(UPLOADS_URL, files=files)
    return res.json()
