import sys, os

'''List of flags: See show_help method'''

allowed_schemes = ["aes", "xor", "feistel"]

def show_help():
    print("Options:")
    print("-h display help and flag options")
    print("-e <image file>: ENCODE: take an input image and split it into shares")
    print("-d: DECODE: (must be used with --inDir) take a path to a directory containing each image share and combine them to output the decoded image")
    print(f"--scheme [{'/'.join(allowed_schemes)}]: used to select the encoding scheme. Note: aes requires a 32-byte key")
    print("-i: INFO: when used with -e, provides information about the selected encoding method.")
    print("--keyStr [keyStr]: expects a string literal to use when encoding/decoding with the xor scheme.")
    print("--keyFile [key.txt]: alternative to --keyStr, expects a txt file containing the key string to use when encoding/decoding with the xor scheme.")
    print("  |->Note: if no key is provided, a random 32 byte key will be generated.")
    print("--outDir <dir>: Directory to output the encoded shares or the decoded image.")
    print("--inDir <dir>: Directory to read encoded shares from.")
    print("-----------------------------------------------------")
    print("Example Usage:")
    print("encoding:")
    print("python3 main.py -e image.png --scheme xor --keyFile key.txt --outDir ~/myShares -i")
    print("decoding:")
    print("python3 main.py -d --inDir ~/myShares --scheme aes --outDir ~/myImage")


def parse_CLI():
    encode = False
    decode = False
    input_image_path = None
    scheme = None
    key = None
    shares_directory = None
    output_directory = None
    info = False

    if ((len(sys.argv) == 1) or sys.argv[1] == "-h"): #If the help flag was set or no arguments were given, display the help menu
        show_help()
        sys.exit()

    else:
        i = 1
        while i < len(sys.argv):
            #Parse each token in the command line
            token = sys.argv[i]
            try:

                match token:
                    case "-e":
                        if(decode or encode): #Make sure that only one of encode/decode is used
                            print("Only one Encode/Decode flag should be set. Use -h to display help.")
                            sys.exit()
                        encode = True
                        i += 1
                        input_image_path = sys.argv[i] #Read the image to encode
                        if not os.path.isfile(input_image_path):
                            print(f"Error: unable to locate file {input_image_path}.") #Make sure the input file exists
                            sys.exit()
                        ##Note: Checking for valid file type happens in image-io.py
                        i += 1 #advance the token index

                    case "-d":
                        if(decode or encode): #Make sure that only one of encode/decode is used
                            print("Only one Encode/Decode flag should be set. Use -h to display help.")
                            sys.exit()
                        decode = True
                        i += 1 #advance the token index

                    case "--scheme":
                        if scheme is not None: #Ensure that only one scheme is selected
                            print("Error: only one scheme should be specified. Use -h to display help.")
                            sys.exit()
                        i += 1
                        scheme = sys.argv[i].lower() #Read the scheme
                        if (scheme not in allowed_schemes): #Make sure the scheme is a known scheme
                            print(f"Unknown scheme: {scheme}. Scheme options are: {'/'.join(allowed_schemes)}. Use -h to display help.")
                            sys.exit()
                        i += 1 #advance the token index

                    case "--keyStr":
                        if key is not None: #Ensure that only one key is provided
                            print("Only one key should be provided. Use -h to display help.")
                            sys.exit()

                        i += 1
                        key = sys.argv[i] #Read the key. Note: key will be encoded as bytes in crypto.py
                        i += 1 #advance the token index

                    case "--keyFile":
                        if key is not None: #Ensure that only one key is provided
                            print("Only one key should be provided. Use -h to display help.")
                            sys.exit()

                        i += 1
                        key_path = sys.argv[i] #Read the filepath for the key
                        if not os.path.isfile(key_path):
                            print(f"Error: --keyFile specified, but unable to find file {key_path}. Use -h to display help.")
                            sys.exit()
                        if not os.access(key_path, os.R_OK):
                            print(f"Error: User does not have permission to read the keyFile {key_path}")
                            sys.exit()

                        try:
                            with open(key_path, 'r') as f:
                                key = f.read() #Read the key. Note: key will be encoded as bytes in crypto.py
                        except Exception:
                            print(f"Error: unable to read file {key_path}")
                            sys.exit()

                        i += 1 #advance the token index


                    case "--outDir":
                        i += 1
                        output_directory = sys.argv[i] #Read the output directory path
                        ##Note: If the directory does not exist, it will be created as part of image-io.py
                        if os.path.exists(output_directory):
                            if os.path.isfile(output_directory):
                                print(f"Error: --outDir must be a directory. Use -h to display help.")
                                sys.exit()
                            if not os.access(output_directory, os.W_OK):
                                print(f"Error: User does not have permission to write to the directory {output_directory}")
                                sys.exit()
                        i += 1 #advance the token index



                    case "--inDir":
                        i += 1
                        shares_directory = sys.argv[i] #Read the input directory path
                        i += 1 #advance the token index
                        #Ensure that the in directory exists:
                        if not os.path.isdir(shares_directory):
                            print(f"Error: {shares_directory} is not a directory")
                            sys.exit()
                        try:
                            files = os.listdir(shares_directory)
                        except PermissionError:
                            print("Error: cannot access directory")
                            sys.exit()

                    case "-i":
                        if (info != False):
                            print("Multiple instances of the -i flag are redundant. Additional instances have been ignored")
                        info = True
                        i += 1 #advance the token index

                    case _:
                        print(f"Unknown option: {token}. Use python3 main.py -h to display help.")
                        sys.exit()

            except IndexError:
                print(f"Error:argument expected after {sys.argv[i-1]} but found none. Use -h to display help.")
                sys.exit()

        #After reading all the tokens, check that the following conditions are met:
        if ((encode is None) and (decode is None)):
            print("Error: either -e or -d must be specified. Use -h to display help.")
            sys.exit()

        if encode:
            #checks for no input image, scheme, key, or if a non-32-byte key was mistakenly provided for aes scheme
            if input_image_path is None:
                print("Error: an input image is required for encoding. Use -h to display help.")
                sys.exit()
            if scheme is None:
                print("Error: a scheme ({'/'.join(allowed_schemes)}) is required for encoding. Use -h to display help.")
                sys.exit()
            if (key is None):
                pass #This is handled in main.py

        if decode:
                #checks for no scheme, key, input directory, or if a key was mistakenly provided for aes scheme
                if scheme is None:
                    print("Error: a scheme ({'/'.join(allowed_schemes)}) is required for decoding. Use -h to display help.")
                    sys.exit()
                if key is None:
                    print("Error: a key must be specified when decoding. Use -h to display help.")
                    sys.exit()
                if shares_directory is None or not any(os.scandir(shares_directory)): #Check if no input directory was provided, or the directory is empty
                    print("Error: an input directory (containing image shares) must be specified when decoding. Use -h to display help.")

        return {
            "encode": encode,
            "decode": decode,
            "input_image_path": input_image_path,
            "scheme": scheme,
            "key": key,
            "shares_directory": shares_directory,
            "output_directory": output_directory,
            "info": info
        }
