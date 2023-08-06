from time import sleep

from .ext.Encryption import *
from .errors import *

__all__ = ["Queue"]


class Queue(object):
    def __init__(self, size: int):
        """Queue is a class that was made to secure your data better. It works by
        taking data that is been taken with a bytes structure and setting the data in the
        put function. It enters the Encryption class and there it starts the encryption.
        :param size: define a size for the queue list.
        """
        self._size = size
        self._queue = []
        self._encrypt_session = Encryption()

    def put(self, *args: bytes) -> None:
        """add to the _queue list data and encrypts.
        :param args takes bytes and encrypts it for safety
        """
        add_total = len(self._queue) + len(args)
        if add_total <= self._size:
            for arg in args:
                arg = self._encrypt_session.encrypt_data(arg)
                self._queue.append(arg)
        else:
            raise ErrorRequestedHigherThanExpected(f"Expected {self._size} elements but instead got {add_total}")

    def get_queue_decrypted(self) -> list:
        """Get the data you have stored after decryption."""
        temp = []
        for task in self._queue:
            temp.append(self._encrypt_session.decrypt_data(task))
        return temp

    def get_queue_encrypted(self) -> list:
        """Get the data you have stored before decryption."""
        return self._queue

    def next_and_destroy(self, timeout: float = None):
        """Destroy the first element in the list data.
        :param timeout The time that the function will wait. After the timeout it will start acting.
        """
        if timeout is not None:
            sleep(timeout)
        self._queue.pop(0)
        self._encrypt_session.next_and_destroy()

    def new_encryption(self, queue_index: int):
        """This function will create a new encryption for a specific element.
        :param queue_index: type here the index of the list that you want to encrypt.
        """
        try:
            temp_queue = self._queue[queue_index]
            decrypted_temp = self._encrypt_session.decrypt_data(temp_queue)
            temp_queue = self._encrypt_session.encrypt_data(decrypted_temp)
            self._queue.pop(queue_index)
            self._queue.insert(queue_index, temp_queue)
        except IndexError:
            raise IndexError("The index that you placed isn't valid.")

    def change_queue_length(self, length: int):
        """Change the length of the queue list holder to allow more data."""
        if length >= 0:
            self._size = length
        else:
            raise ErrorQueueSizeNotValid("Invalid size expected a equal or greater length than 0")

    def clear_session(self):
        """clear all data and when using again it will start a new session."""
        self._encrypt_session.clear_session()
        self._queue.clear()
