from PIL import Image
from crypto import crypto
import numpy as np


def images_equal(img1, img2):
    return np.array_equal(np.array(img1), np.array(img2))


def main():
    original = Image.open("./testImage.jpg")
    key = crypto.generateKey()
    print("Generated key:", key)

    c = crypto()
    c.setKey(key)
    c.encrypt_and_save_channels(original)
    print("Saved R.png, G.png, B.png.")

    c2 = crypto()
    c2.load_and_decrypt_channels(key)
    out = c2.returnBuffer()[0]
    if images_equal(original, out):
        print("Test PASSED: Reconstructed image matches original.")
    else:
        print("Test FAILED: Images do not match.")


if __name__ == "__main__":
    main()
