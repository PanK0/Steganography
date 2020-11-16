# For image processing
import sys
import math
from PIL import Image

MAX_BIT_LEN = 1024

'''
Given the pixel array of an image and the plaintext
Returns the encrypted pixel array following the scheme:
Take the binary representation of the plaintext.
Change the values of the pixels to odd for 1s and to even for 0s.
In in the range (0, width) it is stored the binary repr of the plaintext length
So that in a message it will be possible to store max(2^(width*3), width*height-width)
bits.
'''
def Encrypt_PixelArray(pixel_array, plaintext, image_size) :
	width = image_size[0]
	height = image_size[1]
	binary_plaintext = ''.join(format(ord(i), '08b') for i in plaintext)

	b_len = len(binary_plaintext)		# We BLen
	msg_len = format(b_len, 'b')		# tells in binary the length of plaintext in bits
	tot_bytes = 3 * width
	assert len(msg_len) < tot_bytes
	rgb = 3

	# Front padding to the length information
	for i in range(0, tot_bytes - len(msg_len)) :
		msg_len = '0' + msg_len

	assert len(msg_len) <= tot_bytes

	# Put the length of the message in the first row of the picture
	#print ('Before:', pixel_array[width-len(plaintext)-1: width])
	#print ('Binary:', msg_len, ' Len: ', len(msg_len))			
	for i in range(len(msg_len)) :
		odd = pixel_array[i//rgb][i%rgb] % 2
		if (msg_len[i] == '0' and odd) :
			pixel_array[i//rgb] = list(pixel_array[i//rgb])
			pixel_array[i//rgb][i%rgb] -= 1
			pixel_array[i//rgb] = tuple(pixel_array[i//rgb])
		elif (msg_len[i] == '1' and not odd) :
			pixel_array[i//rgb] = list(pixel_array[i//rgb])
			pixel_array[i//rgb][i%rgb] +=1
			pixel_array[i//rgb] = tuple(pixel_array[i//rgb])
	#print ('After:', pixel_array[width-len(plaintext)-1: width])

	# Put the message from the second row
	#print ('Before:', pixel_array[width : width + b_len//rgb +1])
	#print ('Binary:', binary_plaintext, ' Len: ', b_len)
	for i in range(b_len) :
		odd = pixel_array[width + (i//rgb)][i%rgb] % 2
		if (binary_plaintext[i] == '0' and odd) :
			pixel_array[width + (i//rgb)] = list(pixel_array[width + (i//rgb)])
			pixel_array[width + (i//rgb)][i%rgb] -= 1
			pixel_array[width + (i//rgb)] = tuple(pixel_array[width + (i//rgb)])
		elif (binary_plaintext[i] == '1' and not odd) :
			pixel_array[width + (i//rgb)] = list(pixel_array[width + (i//rgb)])
			pixel_array[width + (i//rgb)][i%rgb] +=1
			pixel_array[width + (i//rgb)] = tuple(pixel_array[width + (i//rgb)])
	#print('After:', pixel_array[width : width + b_len//rgb +1])


'''
Given the pixel array and the size of the image, returns the plaintext message
'''
def Decrypt_PixelArray(pixel_array, image_size) :
	width, height = image_size
	msg_len_encr = pixel_array[:width]
	rgb = 3

	#print (pixel_array[:width])
	# Compute the length of the message in bits
	msg_len = ''
	for px in msg_len_encr :
		for j in range(rgb) :
			msg_len += str(px[j]%2)
	b_len = int(msg_len, 2)
	
	# Getting the binary representation of the text
	binary_text = ''
	for i in range(b_len) :
		binary_text += str(pixel_array[width + (i//rgb)][i%rgb] % 2)

	# Giving the result
	text = ''
	for i in range((b_len//8)) :
		char = int(binary_text[i*8 : (i+1)*8], 2)
		text += chr(char)

	return text

'''
Given an opened image and an array of pixels
Overwrites the image's pixels with the new in the array
Pixel (x, y) is at position pixel_array[width*y + x]
'''
def Modify_Picture(image, pixel_array) :
	width, height = image.size
	for x in range(width) :
		for y in range(height)	:
			image.putpixel( (x, y), pixel_array[width*y +x])


'''
Encrypts the data in plaintext putting them into a copy of image_file,
saving the copy as 'encr_' + image_file
'''
def Encrypt(image_file, plaintext) :

	# Open the image given as input and create a copy
	image = Image.open(image_file, 'r')
	encr_image = image.copy()

	# Getting information about the image
	# Pixel (x, y) is at position pixel_values[width*y + x]
	width, height = image.size
	if (len(plaintext) > ((width * height) -width)) :
		print ("Plaintext too long: operation aborted.")
		print ("Please choose a plaintext shorter than", ((width * height) -width), " chars")
		return -1
	pixel_values = list(image.getdata())

	# Change the values in the pixel array to encrypted ones
	Encrypt_PixelArray(pixel_values, plaintext, image.size)
	
	'''
	print ("\nEncryption, modified pixel values. First 20 pixels and last 10 pixels of the first line")
	print (pixel_values[0 : 20])
	print (pixel_values[width-10 : width])
	'''

	# Transform the encr_image with the new values
	Modify_Picture(encr_image, pixel_values)

	# Save the new imager
	encr_image.save('encr_' + image_file)

	# Close the images
	image.close()
	encr_image.close()


'''
Decrypts the data in the image and returns the plaintext
'''
def Decrypt(image_file) :

	# Open the image with the encrypted text
	image = Image.open(image_file, 'r')


	# Getting information about the image
	width, height = image.size
	pixel_values = list(image.getdata())

	# Decrypt
	text = Decrypt_PixelArray(pixel_values, image.size)

	# Close
	image.close()

	return text


'''
Checks wether the input image is a .png file to give a warning
'''
def check_png(image_name) :
	if ( str(image_name.split(".")[1]).lower() != 'png') :
		print ("Warning! Non .png file detected as input.")
		print ("Decryption may not properly work.")

'''
Main function
'''
def main() :
	argv = sys.argv
	plaintext = ''

	if ('-encr' in argv) :
		# Get and check image
		image_file = argv[argv.index('-encr') +1]
		check_png(image_file)

		# Get the plaintext
		if ('-in' in argv) :
			try :
				plaintext_file = open(argv[argv.index('-in') +1], 'r')
			except :
				print ("No file found with name", argv[argv.index('-in') +1])
				return -1
			plaintext = plaintext_file.read()
		elif ('-text' in argv) :
			plaintext = argv[argv.index('-text') +1]
		else :
			print ("Give some text to encrypt. Type -help for instructions")
			return -1

		# Put the text i
		ret = Encrypt(image_file, plaintext)
		try :
			plaintext_file.close()
		except :
			return -1
		if (ret == -1) :
			return -1
		print ("Encryption done")

	elif ('-decr' in argv) :
		image_file = argv[argv.index('-decr') +1]
		check_png(image_file)

		# Write the text on output
		if ('-out' in argv) :
			plaintext_file_name = argv[argv.index('-out') +1]
			try :
				plaintext_file = open(plaintext_file_name, 'w')
			except :
				print ("No file found with name", plaintext_file_name)
				return -1
			text = Decrypt(image_file)
			plaintext_file.write(text)
			plaintext_file.close()
			print ("Decryption done")
		else :
			print ("Decrypted message: ")
			text = Decrypt(image_file)
			print (text)

		

	elif ('-help' in argv) :
		print ("\n******* ENCRYPTION")
		print ("SYNOPSIS")
		print ("The picture to modify should be a .png picture to avoid data loss.")
		print ("script -encr image.png (-in input.txt | -text 'message to encrypt') ")
		print ("e.g. ~$ python script.py -encr my_fav_picture.png -in input_plaintext.txt")
		print ("e.g. ~$ python script.py -encr my_fav_picture.png -text I\\ want\\ to\\ encrypt\\ this\\")

		print ("\n******* DECRYPTION")
		print ("SYNOPSIS")
		print ("If no output file is specified, the plaintext will be printed as output on the terminal")
		print ("script -decr encr_image.png [-out output.txt]")
		print ("e.g. ~$ python script.py -decr encripted_image.png -out output_file.txt")
		print ("e.g. ~$ python script.py -decr encripted_image.png")

	else : ('Specify image file')

if __name__ == '__main__' :
	main()
