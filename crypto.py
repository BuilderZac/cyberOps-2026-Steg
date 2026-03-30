class crypto:
    """
    Adds all crypto methods. Uses an internal buffer for most operations.

    Attributes:
        key (string): the current saved key
        outputBuffer (): the current images ready for output
    """
    key = ""

    def __init__(self, key: str = None):
        """
        Initiates the crypto system.

        Args:
            key (string): can be passed a starting key
        """
        self.key = key

    def basicEncode(source):
        """
        Takes a single image to split it apart and puts it in the outputBuffer

        Args:
            source (): The original image
        """

    def bufferImport(imageList):
        """
        Force adds images to the buffer. Can be a list of 1 image.

        Args:
            imageList (): list of images to add
        """

    def basicDecode():
        """
        Tries to remerge all images in the buffer.
        """

    def setKey(key):
        """
        Sets a new key overwriting a old or none existent one.

        Args:
            key (string): the new key to use
        """

    def keyOutput():
        """
        Applies a cipher using the set key to the images in the buffer.
        """

    def dekeyOutput():
        """
        Undoes the symmetric cipher using the set key to the images in the buffer.
        """

    def returnOutput():
        """
        Returns a list of all images in the buffer.
        """
