import sys

#sys.argv is the list of all command line arguments
#sys.argv[0] is the name of the program

'''List of flags:
    -h display help and flag options
    -e [image]: take an input image and split it into shares
    -d [image]: input path to a directory containing each image share and combine them to output the decoded image
    --scheme [rgb/key]: used to select the encoding scheme, rgb or key
    --key [key str] or [key.txt]: expects either a string literal or txt file containing the key string to use when encoding/decoding
    --outDir [dir]: Directory to output the encoded shares
    --inDir [dir]: Directory to read encoded shares from

Example Usage:
    Python3 main.py -e image.png --scheme rgb --key keyString.txt --outDir ~/myShares

    Python3 main.py -d --inDir ~/myShares --scheme rgb --key keyString.txt

'''


def show_help():
    print("Options:")
    print("-h display help and flag options")
    print("-e [image]: take an input image and split it into shares")
    print("-d [image]: input path to a directory containing each image share and combine them to output the decoded image")
    print("--scheme [rgb/key]: used to select the encoding scheme, rgb or key")
    print("--key [keyStr] or [key.txt]: expects either a string literal or txt file containing the key string to use when encoding/decoding")
    print("--outDir [dir]: Directory to output the encoded shares")
    print("--inDir [dir]: Directory to read encoded shares from")



if (sys.argv[1] == "-h"):
    show_help()
    quit()

elif (len(sys.argv) < 8): #If there are fewer than 8 arguments it cannot possibly be correct
    print("Improper usage, try main.py -h for help")

#TODO: Parse each flag
