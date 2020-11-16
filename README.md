# Steganography
A little python script to write data into pictures.

It would be better to first encrypt data with an encryption algorithm such as AES or RSA before to write them into the picture.

Anyway, don't use this script if you want to securely exchange data.

# How To Run
For help info:
```
python steganography.py -help
```
To Encrypt:
```
python steganography.py -encr image.png (-in input.txt | -text 'message to encrypt')
```

To Decrypt: 
```
python steganography.py -decr encr_image.png [-out output.txt]
```
