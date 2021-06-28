# vigenere-cipher
Encrypts, decrypts, and attempts to figure out the key for vigenere cipher

## Encryption
- Enter 'ENCRYPTION' when prompted
- Enter plaintext to encrypt
- Enter key to encrypt with
- Encrypted text is output

## Decryption (with a key)
- Enter 'DECRYPTION' when prompted
- Enter ciphertext to decrypt
- Input 'Y' to indicate that the key is known
- Input the key
- Decrypted text is output

## Decryption (without a key) - the program will attempt to find the key
- Enter 'DECRYPTION' when prompted
- Enter ciphertext to decrypt
- Input 'N' to indicate that the key is not known
- Input a maximum key length to check for. This must be greater than 0 but less than the length of the ciphertext. Note that a larger maximum key will be slower.
- The most likely key length to the least likely key length is output
- Input a key length to use
- Keys will be output, ordered by the most likely key to the least likely key
- Input a key to use. Inputting '1' will automatically select the most likely key.
- Decrypted text is output
