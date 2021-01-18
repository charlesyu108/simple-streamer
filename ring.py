class RingBuffer:
    """
    A simple ring-buffer.
    """

    def __init__(self, max_size=100):
        self.max_size = max_size

        self._buffer = [None] * max_size
        self._size = 0
        self._next_read_pos = 0
        self._next_write_pos = 0
    
    def add(self, value):
        if self.is_full():
            raise FullBufferException("The buffer is full.")
        self._buffer[self._next_write_pos] = value
        self._next_write_pos += 1
        if self._next_write_pos >= self.max_size:
            self._next_write_pos = 0
        self._size += 1

    
    def get(self):
        if self.is_empty():
            raise EmptyBufferException("The buffer is empty.")
        val = self._buffer[self._next_read_pos]
        self._next_read_pos += 1
        if self._next_read_pos >= self.max_size:
            self._next_read_pos = 0
        self._size -= 1
        return val

    def is_full(self):
        return self._size == self.max_size

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

##############################################
# Exceptions
##############################################

class FullBufferException(Exception):
    """
    The Buffer is full
    """

class EmptyBufferException(Exception):
    """
    The Buffer is empty
    """
