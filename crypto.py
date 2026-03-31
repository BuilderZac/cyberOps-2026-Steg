from PIL import Image
from numpy import array


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
    key = ""
    buffer = []

    def __init__(self, key: str = None):
        """
        Initiates the crypto system.

        Args:
            key (string): can be passed a starting key
        """
        self.key = key

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
        Tries to remerge all images in the buffer.
        """
        means = [array(i).mean() for i in self.buffer]
        r = g = b = None
        for i, m in enumerate(means):
            if m > 0:
                if r is None:
                    r = self.buffer[i]
                elif g is None:
                    g = self.buffer[i]
                elif b is None:
                    b = self.buffer[i]

        if None in (r, g, b):
            raise ValueError(
                "Could not identify all three channels in buffer.")

        merged = Image.merge("RGB", (r, g, b))
        self.buffer = [merged]

    def setKey(self, key):
        """
        Sets a new key overwriting a old or none existent one.

        Args:
            key (string): the new key to use
        """
        self.key = key

    def keyBuffer(self):
        """
        Applies a cipher using the set key to the images in the buffer.
        """
        temBuffer = []
        size = 0
        for i in self.buffer:
            size = i.size
            imageData = i.tobytes()

            # cipher here

            reconstructed = Image.frombytes("RGB", size, imageData)
            temBuffer.append(reconstructed)
        self.buffer = temBuffer

    def dekeyBuffer(self):
        """
        Undoes the symmetric cipher using the set key to the images in the buffer.
        """
        temBuffer = []
        size = 0
        for i in self.buffer:
            size = i.size
            imageData = i.tobytes()

            # cipher here

            reconstructed = Image.frombytes("RGB", size, imageData)
            temBuffer.append(reconstructed)
        self.buffer = temBuffer

    def returnBuffer(self):
        """
        Returns a list of all images in the buffer.
        """
        return self.buffer

    def clearBuffer(self):
        """
        Clears the buffer back to an empty list.
        """
        self.buffer = []
