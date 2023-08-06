try:
    from cryptography.fernet import Fernet
except ModuleNotFoundError:
    raise ModuleNotFoundError("Missing libraries! Use: pip3 install -r requirements.txt")

__all__ = ["Encryption"]


class Encryption(object):
    def __init__(self):
        """The Encryption class is used to encrypt and decrypt the data."""
        self._key = Fernet.generate_key()
        self._key_for_each = {}

    def encrypt_data(self, data: bytes) -> bytes:
        """encrypt data and update the dictionary(_key_for_each).
        :param data takes bytes
        """
        try:
            data = Fernet(self._key).encrypt(data)
            self._key_for_each.update({data: self._key})
            return data
        except Exception as e:
            raise Exception(e)

    def decrypt_data(self, data: bytes) -> bytes:
        """decrypt data and returns the new data. this method uses the self._key_for_each,
        which will find the data that was saved in the dictionary. It will take its key and finally decrypt it.
        :param data takes bytes
        """
        try:
            return Fernet(self._key_for_each.get(data)).decrypt(data)
        except Exception as e:
            raise Exception(e)

    def next_and_destroy(self):
        """Destroy the first element in the dictionary data."""
        key = None
        for a in self._key_for_each.keys():
            key = a
            break
        self._key_for_each.pop(key)

    def clear_session(self):
        """It will start a new session of encryption, which will prevent saving new data and old data that
        won't be used in future.
        """
        self._key = Fernet.generate_key()
        self._key_for_each.clear()