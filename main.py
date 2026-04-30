import CLI_parsing, crypto, image_io, os, sys

#Parse all the command line arguments
args = CLI_parsing.parse_CLI()

#unpack all the args
encode = args["encode"]
decode = args["decode"]
input_image_path = args["input_image_path"]
scheme = args["scheme"]
key = args["key"]
shares_directory = args["shares_directory"]
output_directory = args["output_directory"]
info = args["info"]

#List of allowed file extensions
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}

def fail_lodaing():
    print()
    print('''
| Command Line Input Parsing.......OK
| Loading Image(s).................ERROR
| Encoding/Decoding................
| Saving Image(s)..................
''')
    sys.exit()

def fail_crypto():
    print()
    print('''
| Command Line Input Parsing.......OK
| Loading Image(s).................OK
| Encoding/Decoding................ERROR
| Saving Image(s)..................
''')
    sys.exit()

def fail_saving():
    print()
    print('''
| Command Line Input Parsing.......OK
| Loading Image(s).................OK
| Encoding/Decoding................OK
| Saving Image(s)..................ERROR
''')
    sys.exit()




def load_RGB_shares():
    '''
    Check the shares_directory to find the red green and blue shares. Returns a list containing each share. Will break if there are multiple images with the same "share_r/g/b" substring
    '''

    #Load R, G, B shares

    try:
        r = g = b = None
        for entry in os.scandir(shares_directory):
            if entry.is_file():

                name, ext = os.path.splitext(entry.name)
                name = name.lower()

                if ext.lower() in IMAGE_EXTENSIONS:
                    if "share_r" in name:
                        r = image_io.load_share(entry.path)
                    elif "share_g" in name:
                        g = image_io.load_share(entry.path)
                    elif "share_b" in name:
                        b = image_io.load_share(entry.path)

        if r is None or g is None or b is None:
            print("Error: Missing one or more RGB shares")
            fail_loading()

    except Exception as e:
        print(e)
        fail_loading()

    return [r,g,b]


#Create an instance of crypto
c = crypto.crypto(info=info)
if key is not None:
    c.setKey(key) #Set the key for encoding/decoding
elif key is None:
    print("No key provided. A random 32-byte key will be generated. Please save it in a safe location as it is necessary to decode the shares.")
    key = c.generateKey()
    try:
        c.setKey(key)
        print(f"Generated key: {key}")
    except Exception as e:
        print(e)
        fail_crypto()

#Create a list to store image files
image_files = []

if (encode): #If the encode flag is set, load the image at input_image_path and add it to the list

    image_files.append(image_io.load_image(input_image_path)) #Convert the input image to a PIL Image

    if (scheme == "xor"):
        #Encode with XOR using the key

        try:
            c.basicEncode(image_files[0]) #Break the input image into R, G, B images (and store them in the buffer)
            c.keyBuffer() #Apply an XOR cipher to the images using the key that was just set

        except Exception as e:
            print(e)
            fail_crypto()

        #Save the encoded images
        try:
            encoded_images = c.returnBuffer()
            image_io.save_image(encoded_images[0], "share_r.png", output_directory) #Save the red share
            image_io.save_image(encoded_images[1], "share_g.png", output_directory) #Save the green share
            image_io.save_image(encoded_images[2], "share_b.png", output_directory) #Save the blue share
        except Exception as e:
            print(e)
            fail_saving()


    elif (scheme == "aes"): #encode the image with AES
        #Check key validity
        try:
            if (len(c.key) != 32):
                print("The provided key does not meet AES requirements. A random key has been generated for AES encryption. Please store it in a safe place as it is necessary to decrypt the shares")
                key = c.generateKey()
                print(f"Generated key: {key}")
                c.setKey(key)

            c.basicEncode(image_files[0]) #Break the input image into R,G,B images (and store them in the buffer)
            c.aesEncryptBuffer() #Apply AES-CTR to the images in the buffer (and store the result in the buffer)

        except Exception as e:
            print(e)
            fail_crypto()

        #Save the encoded images
        try:
            encoded_images = c.returnBuffer()
            image_io.save_image(encoded_images[0], "share_r.png", output_directory) #Save the red share
            image_io.save_image(encoded_images[1], "share_g.png", output_directory) #Save the green share
            image_io.save_image(encoded_images[2], "share_b.png", output_directory) #Save the blue share

        except Exception as e:
            print(e)
            fail_saving()


    elif (scheme == "feistel"): #encode the image with feistel
        try:
            c.basicEncode(image_files[0]) #Break the input image into R,G,B images (and store them in the buffer)
            c.feistelEncode() #Apply feistel cipher to each image in the buffer
        except Exception as e:
            print(e)
            fail_crypto()

        #Save the encoded images
        try:
            encoded_images = c.returnBuffer()
            image_io.save_image(encoded_images[0], "share_r.png", output_directory) #Save the red share
            image_io.save_image(encoded_images[1], "share_g.png", output_directory) #Save the green share
            image_io.save_image(encoded_images[2], "share_b.png", output_directory) #Save the blue share

        except Exception as e:
            print(e)
            fail_saving()

else: #otherwise load and decode shares based on scheme

    if (scheme == "xor"):

        share_list = load_RGB_shares() #Load each share in the share directory
        c.bufferImport(share_list) #Add the shares to the buffer

        try:
            c.setKey(key) #Set the key for decoding
            c.dekeyBuffer() #Undo the XOR cipher for each image in the buffer
            c.basicDecode() #Remerge the R,G,B shares in the buffer to get the original image

        except Exception as e:
            print(e)
            fail_crypto()

        #Save the decoded image
        filename = "decodedImage.png"

        try:
            if output_directory is not None: #If the output directory exists and already contains a decodedImage, add a number to the end of the filename
                if os.path.isfile(os.path.join(output_directory, "decodedImage.png")):
                    i = 1
                    while os.path.isfile(os.path.join(output_directory, f"decodedImage{i}.png")):
                        i += 1

                    filename = f"decodedImage{i}.png"
                    print(f"set filename to {filename}")


            image_io.save_image(c.returnBuffer()[0], filename, output_directory)

        except Exception as e:
            print(e)
            fail_saving()

    elif (scheme == "aes"):

        shares_list = load_RGB_shares() #Load each share in the share directory
        c.bufferImport(shares_list) #Add the shares to the buffer

        try:
            c.aesDecryptBuffer() #Undo the aes encryption
            c.basicDecode() #Merge r,g,b shares back into one image
        except Exception as e:
            print(e)
            fail_crypto()

        #Save the decoded image
        filename = "decodedImage.png"

        try:
            if output_directory is not None: #If the output directory exists and already contains a decodedImage, add a number to the end of the filename
                if os.path.isfile(os.path.join(output_directory, "decodedImage.png")):
                    i = 1
                    while os.path.isfile(os.path.join(output_directory, f"decodedImage{i}.png")):
                        i += 1

                    filename = f"decodedImage{i}.png"
                    print(f"set filename to {filename}")

            image_io.save_image(c.returnBuffer()[0], filename, output_directory)

        except Exception as e:
            print(e)
            fail_saving()

    elif (scheme == "feistel"):

        shares_list = load_RGB_shares() #Load each share in the share directory
        c.bufferImport(shares_list) #Add the shares to the buffer

        try:
            c.feistelDecode() #Undo the feistel cipher
            c.basicDecode() #Merge r,g,b shares back into one image

        except Exception as e:
            print(e)
            fail_crypto()

        #Save the decoded image
        filename = "decodedImage.png"

        try:
            if output_directory is not None: #If the output directory exists and already contains a decodedImage, add a number to the end of the filename
                if os.path.isfile(os.path.join(output_directory, "decodedImage.png")):
                    i = 1
                    while os.path.isfile(os.path.join(output_directory, f"decodedImage{i}.png")):
                        i += 1

                    filename = f"decodedImage{i}.png"
                    print(f"set filename to {filename}")

            image_io.save_image(c.returnBuffer()[0], filename, output_directory)

        except Exception as e:
            print(e)
            fail_saving()


#Finally print out a graph showing each portion of the data flow
print('''
| Command Line Input Parsing.......OK
| Loading Image(s).................OK
| Encoding/Decoding................OK
| Saving Image(s)..................OK
''')
