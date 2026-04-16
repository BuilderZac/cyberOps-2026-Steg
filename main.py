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


#List of allowed file extensions
image_extensions = {".png", ".jpg", ".jpeg", ".bmp"}



#TODO:encrypt/decrypt images for aes

#Create an instance of crypto
c = crypto.crypto()

#Create a list to store image files
image_files = []

if (encode): #If the encode flag is set, load the image at input_image_path and add it to the list
    image_files.append(image_io.load_image(input_image_path)) #Convert the input image to a PIL Image
    if (scheme == "xor"):
        #Encode with XOR using the key

        c.setKey(key) #Set the key for encoding
        c.basicEncode(image_files[0]) #Break the input image into R, G, B images
        c.keyBuffer() #Apply an XOR cipher to the images using the key that was just set

        #Save the encoded images
        encoded_images = c.returnBuffer()
        image_io.save_image(encoded_images[0], "share_r.png", output_directory) #Save the red share
        image_io.save_image(encoded_images[1], "share_g.png", output_directory) #Save the green share
        image_io.save_image(encoded_images[2], "share_b.png", output_directory) #Save the blue share



    elif (scheme == "aes"):
        ###IMPORTANT NOTE: For now, decoding for aes will only work with pngs, and both encoding/decoding can only view files in the current directory###
        img = image_io.load_image(input_image_path)
        c.setKey(key) #Set the key for encoding
        c.encrypt_and_save_channels(img, "aes_share_")


else: #otherwise load and decode shares based on scheme

    if (scheme == "xor"):

        #Load R, G, B shares

        try:
            r = g = b = None
            for entry in os.scandir(shares_directory):
                if entry.is_file():

                    name, ext = os.path.splitext(entry.name)
                    name = name.lower()

                    if ext.lower() in image_extensions:
                        if "share_r" in name:
                            r = image_io.load_share(entry.path)
                        elif "share_g" in name:
                            g = image_io.load_share(entry.path)
                        elif "share_b" in name:
                            b = image_io.load_share(entry.path)

            if r is None or g is None or b is None:
                print("Error: Missing one or more RGB shares")
                sys.exit()

        except PermissionError:
            print(f"Error: Unable to access {shares_directory}")
            sys.exit()
        except FileNotFoundError:
            print("Error: Directory does not exist")
            sys.exit()


        c.bufferImport([r,g,b]) #Add the shares to the buffer

        c.setKey(key) #Set the key for decoding
        c.dekeyBuffer() #Undo the XOR cipher for each image in the buffer
        c.basicDecode() #Remerge the R,G,B shares in the buffer to get the original image

        #Save the decoded image
        if output_directory is not None: #If the output directory exists and already contains a decodedImage, add a number to the end of the filename
            if os.path.isfile(os.path.join(output_directory, "decodedImage.png")):
                i = 1
                while os.path.isfile(os.path.join(output_directory, f"decodedImage{i}.png")):
                    i += 1

                filename = f"decodedImage{i}.png"
                print(f"set filename to {filename}")

        else:
            filename = "decodedImage.png"

        image_io.save_image(c.returnBuffer()[0], filename, output_directory)

    elif (scheme == "aes"):
        #Decode from aes_shares
        c.load_and_decrypt_channels(key, "aes_share_")
        #Save the decoded image
        image_io.save_image(c.returnBuffer()[0], "aes_decoded", output_directory)
