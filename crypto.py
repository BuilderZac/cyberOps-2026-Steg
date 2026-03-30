from PIL import Image


class crypto:
    """
    Adds all crypto methods. Uses an internal buffer for most operations.

    Attributes:
        key (string): the current saved key
        buffer (Image[]): the current images ready for output
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

    def basicDecode(self):
        """
        Tries to remerge all images in the buffer.
        """

    def setKey(self, key):
        """
        Sets a new key overwriting a old or none existent one.

        Args:
            key (string): the new key to use
        """
        self.key = key

    def keyOutput(self):
        """
        Applies a cipher using the set key to the images in the buffer.
        """

    def dekeyOutput(self):
        """
        Undoes the symmetric cipher using the set key to the images in the buffer.
        """

    def returnOutput(self):
        """
        Returns a list of all images in the buffer.
        """
        return self.buffer
