from io import BufferedReader
from typing import Callable, Optional

from hansken_extraction_plugin.runtime import unpack
from hansken_extraction_plugin.runtime.constants import MAX_CHUNK_SIZE


class _LazyBufferedReader(BufferedReader):
    """
    This is a lazy implementation of the BufferedReader. It only gets the current data block requested by
    read(__size). This behaviour can easily be overridden by requesting the total length of the stream as the __size
    param.
    """

    def __init__(self, grpc_handler_read: Callable, stream_offset: int, size: int):
        """
        @param grpc_handler_read: hansken_extraction_plugin.runtime.extraction_plugin_server.ProcessHandler.read
        @param stream_offset: offset the buffer starts at
        @param size: total size of the buffer
        """
        self._grpc_handler_read = grpc_handler_read
        self._stream_offset = stream_offset
        self._size = size
        self._byte_array: bytes = bytes()
        self._position = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _read_chunks(self, size: int):
        """
        This method divides the requested data into chunks of the maximum allowed size per gRPC message.
        @param size: length of the requested data
        @return: a bytes() representation of the RpcBytes response from the server
        """
        offset = self._stream_offset + self._position
        # just one chunk
        if size <= MAX_CHUNK_SIZE:
            self._byte_array = unpack.bytez(self._grpc_handler_read(offset=offset, size=size))
        else:
            # multiple chunks
            no_of_chunks = size // MAX_CHUNK_SIZE
            for i in range(no_of_chunks):
                chunk_offset = offset + (i * MAX_CHUNK_SIZE)
                self._byte_array += \
                    unpack.bytez(self._grpc_handler_read(offset=chunk_offset, size=MAX_CHUNK_SIZE))
            last_offset = offset + no_of_chunks * MAX_CHUNK_SIZE
            last_size = size - last_offset
            if last_size > 0:
                self._byte_array += unpack.bytez(self._grpc_handler_read(offset=last_offset, size=last_size))

    def _clear_buffer(self):
        self._byte_array = bytes()

    def read(self, __size: Optional[int] = None) -> bytes:
        if __size is None:
            __size = self._size

        if __size + self._position > self._size:
            __size = self._size - self._position

        self._clear_buffer()
        self._read_chunks(__size)

        self._position += __size
        return self._byte_array

    def tell(self) -> int:
        return self._position

    def seek(self, position: int, whence: int = None) -> int:
        # TODO HANSKEN-14170: fully implement and test seeking
        if whence:
            raise RuntimeError('whence not supported')

        self._position = position
        return self._position
