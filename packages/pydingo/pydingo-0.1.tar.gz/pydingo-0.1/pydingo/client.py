import io

import PIL.Image

from .client_stub import ClientStub

class Client(object):
    def __init__(self, loop = None):
        self.stub = ClientStub(loop)

    @property
    def hostname(self):
        return self.stub.hostname

    @property
    def port(self):
        return self.stub.port

    def connect(self, address, port = 8080):
        self.stub.connect(address, port)

    def image(self):
        obj, bufs = self.stub.remote_call('image', return_buffers = True)
        return PIL.Image.open(io.BytesIO(bufs[0]))

    def image_selection(self):
        return self.stub.remote_call('image_selection', object_type = tuple)

    def image_size_max(self):
        return self.stub.remote_call('image_size_max')

    def touch(self):
        return self.stub.remote_call('touch')

    def video(self):
        from ipydingo import DeviceVideo

        return DeviceVideo(hostname = self.hostname, port = self.port)
