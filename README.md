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

# Notes
In order to work, the script needs to process .png pictures.

As is it possible to read [here](https://stackoverflow.com/questions/11603528/pil-changes-pixel-value-when-saving):
> JPG doesn't promise to store precisely the pixels you intended. It compresses your data to make the file smaller, and the compression is based on human perception. The idea is to create an array of pixels that appear the same to a human, even though they are different pixels.
>
>So the pixel you are writing is in the output, but the adjacent pixels have been altered to be able to store the entire image in less space. This is called "lossy compression" because data is lost.
>
>Other image formats don't have this property. PNG is a lossless compressed format, meaning precisely the same pixels will results after decompressing a compressed PNG. If you save your image as a PNG, you will have the result you want.
