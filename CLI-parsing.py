import sys, os

#sys.argv is the list of all command line arguments
#sys.argv[0] is the name of the program

'''List of flags:
    -h display help and flag options
    -e <image file>: ENCODE: take an input image and split it into shares
    -d: DECODE: (must be used with --inDir) take a path to a directory containing each image share and combine them to output the decoded image
    --scheme [rsa/key]: used to select the encoding scheme, rsa or key
    --keyStr/keyFile [key str] or [key.txt]: expects either a string literal or txt file containing the key string to use when encoding/decoding
    --outDir <dir>: Directory to output the encoded shares
    --inDir <dir>: Directory to read encoded shares from
'''


def show_help():
    print("Options:")
    print("-h display help and flag options")
    print("-e <image file>: ENCODE: take an input image and split it into shares")
    print("-d: DECODE: (must be used with --inDir) take a path to a directory containing each image share and combine them to output the decoded image")
    print("--scheme [rsa/key]: used to select the encoding scheme, rsa or key")
    print("--keyStr [keyStr]: expects a string literal to use when encoding/decoding with the key scheme")
    print("--keyFile [key.txt]: alternative to --keyStr, expects a txt file containing the key string to use when encoding/decoding with the key scheme")
    print("--outDir <dir>: Directory to output the encoded shares")
    print("--inDir <dir>: Directory to read encoded shares from")
    print("-----------------------------------------------------")
    print("Example Usage:")
    print("encoding:")
    print("python3 main.py -e image.png --scheme key --keyFile key.txt --outDir ~/myShares")
    print("decoding:")
    print("python3 main.py -d --inDir ~/myShares --scheme key --keyFile key.txt")


'''
reads flags from the command line and returns the follwing:
    "encode": encode,
    "decode": decode,
    "input_image_path": input_image_path,
    "scheme": scheme,
    "key": key,
    "shares_directory": shares_directory,
    "output_directory": output_directory
'''
def parse_CLI():
    encode = False
    decode = False
    input_image_path = None
    scheme = None
    key = None
    shares_directory = None
    output_directory = None
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
                        scheme = sys.argv[i].lower() #Read the scheme (and convert to lowercase)
                        if ((scheme != "rsa") and (scheme != "key")): #Make sure the scheme is either rgb or key
                            print(f"Unknown scheme: {scheme}. Scheme options are rsa or key. Use -h to display help.")
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

                        with open(key_path, 'r') as f:
                            key = f.read() #Read the key. Note: key will be encoded as bytes in crypto.py

                        i += 1 #advance the token index


                    case "--outDir":
                        i += 1
                        output_directory = sys.argv[i] #Read the output directory path
                        ##Note: If the directory does not exist, it will be created as part of image-io.py
                        i += 1 #advance the token index

                    case "--inDir":
                        i += 1
                        shares_directory = sys.argv[i] #Read the input directory path
                        i += 1 #advance the token index
                        #Ensure that the in directory exists:
                        if not os.path.isdir(shares_directory):
                            print(f"Error: Unable to find input directory: {shares_directory}.")
                            sys.exit()

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
            #checks for no input image, scheme, key, or if a key was mistakenly provided for rsa scheme
            if input_image_path is None:
                print("Error: an input image is required for encoding. Use -h to display help.")
                sys.exit()
            if scheme is None:
                print("Error: a scheme (rsa or key) is required for encoding. Use -h to display help.")
                sys.exit()
            if scheme == "rsa" and key is not None:
                print("Error: no key should be provided when encoding with the rsa scheme. Use -h to display help.")
                sys.exit()
            if scheme == "key" and key is None:
                print("Error: a key must be specified when encoding with the key scheme. Use -h to display help.")
                sys.exit()

        if decode:
                #checks for no scheme, key, input directory, or if a key was mistakenly provided for rsa scheme
                if scheme is None:
                    print("Error: a scheme (rsa or key) is required for decoding. Use -h to display help.")
                    sys.exit()
                if scheme == "rsa" and key is not None:
                    print("Error: no key should be provided when decoding with the rsa scheme. Use -h to display help.")
                    sys.exit()
                if scheme == "key" and key is None:
                    print("Error: a key must be specified when decoding with the key scheme. Use -h to display help.")
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
            "output_directory": output_directory
        }

parse_CLI()
