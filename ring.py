class RingBuffer:
    """
    A simple ring-buffer that overwrites itself when full.
    """

    def __init__(self, max_size=1000):
        self.max_size = max_size
        self._buffer = [None] * max_size
        self._size = 0
        self._next_read_pos = 0
        self._next_write_pos = 0
    
    def add(self, value):
        self._buffer[self._next_write_pos] = value
        self._next_write_pos += 1
        if self._next_write_pos >= self.max_size:
            self._next_write_pos = 0
        self._size += 1 if not self.is_full() else 0

    
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

##############################################
# Exceptions
##############################################

class EmptyBufferException(Exception):
    """
    The Buffer is empty
    """
