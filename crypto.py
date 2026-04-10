from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import hashlib


class crypto:
    """
    Adds all crypto methods. Uses an internal buffer for most operations.
    I = Complete
    WIP = WIP
    NT = Needs Testing
    B = Bugged
    NA = Not Avalible

    Attributes:
        key (string): the current saved key
        buffer (Image[]): the current images ready for output

    Methods:
        __init__: creates the object (NT)
        basicEncode: take a PIL Image & breaks it to RGB in the buffer (NT)
        bufferImport: adds a list of images to the buffer (NT)
        basicDecode: remerges everything in buffer (NT)
        setKey: sets a text key for the cipher to use (NT)
        keyBuffer: applies cipher to the buffered images using key (WIP)
        dekeyBuffer: undoes the cipher with the key (WIP)
        returnBuffer: returns the buffer as a list of PIL Images (NT)
        clearBuffer: Emptys out the buffer (NT)
    """

    def __init__(self, key: str = ""):
        """
        Initiates the crypto system.

        Args:
            key (string): can be passed a starting key
        """
        self.key = key
        self.buffer = []

    def basicEncode(self, source: Image):
        """
        Takes a single image to split it apart and puts it in the outputBuffer

        Args:
            source (Image): The original image
        """
        r, g, b = source.split()
        self.buffer.append(r)
        self.buffer.append(g)
        self.buffer.append(b)

    def bufferImport(self, imageList):
        """
        Force adds images to the buffer. Can be a list of 1 image.

        Args:
            imageList (Image[]): list of images to add
        """
        for i in imageList:
            self.buffer.append(i)

    def basicDecode(self):
        """
        Remerges the first three images in the buffer as R,G,B.
        """
        if len(self.buffer) < 3:
            raise ValueError("Buffer does not contain three channels.")
        r, g, b = self.buffer[:3]
        merged = Image.merge("RGB", (r, g, b))
        self.buffer = [merged]

    @staticmethod
    def generateKey():
        """
        Generates a random 32-byte key, returns it as a hex string suitable for setKey().
        """
        key_bytes = os.urandom(32)
        return key_bytes.hex()

    def setKey(self, key):
        """
        Sets a new key overwriting a old or none existent one.
        Args:
            key (string or bytes): the new key to use. If hex string, it's converted to bytes.
        """
        if isinstance(key, str):
            # Accept hex or utf-8 string for compatibility
            try:
                # Try to parse as hex string
                self.key = bytes.fromhex(key)
            except ValueError:
                self.key = key.encode('utf-8')
        else:
            self.key = key

    def keyBuffer(self):
        """
        Applies a simple XOR cipher using the set key to the images in the buffer.
        The method works in-place and assumes color images (mode "RGB") for simplicity.
        """
        if not self.key:
            raise ValueError(
                "No key set. Use setKey() to set a key before ciphering.")

        key_bytes = self.key if isinstance(
            self.key, bytes) else self.key.encode('utf-8')
        key_len = len(key_bytes)
        temBuffer = []

        for img in self.buffer:
            size = img.size
            mode = img.mode
            imageData = img.tobytes()
            ciphered = bytearray(len(imageData))

            for idx, byte in enumerate(imageData):
                ciphered[idx] = byte ^ key_bytes[idx % key_len]

            reconstructed = Image.frombytes(mode, size, bytes(ciphered))
            temBuffer.append(reconstructed)
        self.buffer = temBuffer

    def dekeyBuffer(self):
        """
        Undoes the XOR cipher using the set key to the images in the buffer.
        This is identical to keyBuffer since XOR is symmetric.
        """
        if not self.key:
            raise ValueError(
                "No key set. Use setKey() to set a key before deciphering.")

        key_bytes = self.key if isinstance(
            self.key, bytes) else self.key.encode('utf-8')
        key_len = len(key_bytes)
        temBuffer = []

        for img in self.buffer:
            size = img.size
            mode = img.mode
            imageData = img.tobytes()
            deciphered = bytearray(len(imageData))

            for idx, byte in enumerate(imageData):
                deciphered[idx] = byte ^ key_bytes[idx % key_len]

            reconstructed = Image.frombytes(mode, size, bytes(deciphered))
            temBuffer.append(reconstructed)
        self.buffer = temBuffer

    def aesEncryptBuffer(self):
        """
        Encrypts each image in the buffer using AES-CTR.
        The nonce is prepended to the ciphertext for each channel.
        """
        if not self.key or len(self.key) != 32:
            raise ValueError("AES-CTR requires a 32-byte key.")

        temBuffer = []

        for img in self.buffer:
            size = img.size
            mode = img.mode
            data = img.tobytes()
            nonce = os.urandom(16)
            cipher = Cipher(algorithms.AES(self.key), modes.CTR(
                nonce), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            temBuffer.append((nonce + ciphertext, size, mode))
        self.buffer = temBuffer

    def aesDecryptBuffer(self):
        """
        Decrypts each image in the buffer using AES-CTR.
        Assumes each entry is a (nonce+ciphertext, size, mode) tuple.
        """
        if not self.key or len(self.key) != 32:
            raise ValueError("AES-CTR requires a 32-byte key.")

        temBuffer = []

        for item in self.buffer:
            data, size, mode = item
            nonce = data[:16]
            ciphertext = data[16:]
            cipher = Cipher(algorithms.AES(self.key), modes.CTR(
                nonce), backend=default_backend())
            decryptor = cipher.decryptor()
            plain = decryptor.update(ciphertext) + decryptor.finalize()
            img = Image.frombytes(mode, size, plain)
            temBuffer.append(img)
        self.buffer = temBuffer

    def returnBuffer(self):
        """
        Returns a list of all images in the buffer.
        If buffer holds encrypted (nonce+ciphertext, size, mode) tuples,
        returns noise images suitable for saving or visualization.
        """
        result = []
        if len(self.buffer) == 0:
            return result
        # Check if the first buffer item is a tuple from AES encryption
        if isinstance(self.buffer[0], tuple):
            for data, size, mode in self.buffer:
                # Extract ciphertext (skip nonce)
                ciphertext = data[16:]
                # Form a "noise" image from ciphertext bytes
                noise_img = Image.frombytes(mode, size, ciphertext)
                result.append(noise_img)
        else:
            result = list(self.buffer)
        return result

    def clearBuffer(self):
        """
        Clears the buffer back to an empty list.
        """
        self.buffer = []

    @staticmethod
    def derive_nonce(key):
        """Deterministically derive a 16-byte nonce from a 32-byte key."""
        key_bytes = key if isinstance(key, bytes) else bytes.fromhex(key)
        return hashlib.sha256(key_bytes).digest()[:16]

    def encrypt_and_save_channels(self, image, out_prefix=""):
        """Split image to R/G/B, encrypt each with AES-CTR (shared nonce), save as PNGs."""
        self.basicEncode(image)
        nonce = self.derive_nonce(self.key)
        channel_names = ['R', 'G', 'B']
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        for idx, img in enumerate(self.buffer):
            size = img.size
            mode = img.mode
            data = img.tobytes()
            cipher = Cipher(algorithms.AES(self.key), modes.CTR(
                nonce), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            noise_img = Image.frombytes(mode, size, ciphertext)
            noise_img.save(f"{out_prefix}{channel_names[idx]}.png")
        self.clearBuffer()

    def load_and_decrypt_channels(self, key, in_prefix=""):
        """Load R/G/B PNGs, decrypt with AES-CTR (shared nonce), reconstruct image in buffer."""
        channel_names = ['R', 'G', 'B']
        self.setKey(key)
        nonce = self.derive_nonce(self.key)
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        decrypted_buffer = []
        for name in channel_names:
            noise_img = Image.open(f"{in_prefix}{name}.png")
            ciphertext = noise_img.tobytes()
            mode = noise_img.mode
            size = noise_img.size
            cipher = Cipher(algorithms.AES(self.key), modes.CTR(
                nonce), backend=default_backend())
            decryptor = cipher.decryptor()
            plain = decryptor.update(ciphertext) + decryptor.finalize()
            img = Image.frombytes(mode, size, plain)
            decrypted_buffer.append(img)
        self.buffer = decrypted_buffer
        self.basicDecode()
