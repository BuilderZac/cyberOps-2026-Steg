import CLI_parsing, crypto, image_io

#Parse all the command line arguments
args = CLI_parsing.parse_CLI()
print(args)

#unpack all the args
encode = args["encode"]
decode = args["decode"]
input_image_path = args["input_image_path"]
scheme = args["scheme"]
key = args["key"]
shares_directory = args["shares_directory"]
output_directory = args["output_directory"]


#TODO: Load the images with image_io and encrypt them with crypto
