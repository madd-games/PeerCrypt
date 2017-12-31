Format of .key files
====================

A `.key` file is used to store cryptographic keys. They store both the public and the private part of the key, and so the file itself must be kept secret. However, the public key (which can be extracted with the `peercrypt-printpub` command) can be published freely and allows other to verify signatures made with the key (but not to forge them).

The file has the following structure, with all fields in big endian (network byte order).

|Key File                                                                               |
|---------------------------------------------------------------------------------------|
|Magic number (32 bits). The string `KEY\0`. Used simply to identify this as a key file.|
|16-bit [cipher ID](cipher.md). Defines the format of the rest of the file.             |
|*Cipher-specific data*                                                                 |
