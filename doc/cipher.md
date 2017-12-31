Ciphers General Overview
========================

PeerCrypt is a framework which can potentially support all sorts of different ciphers. Certain things are expected from each cipher, and the cipher implementation must handle this.

Cipher components
-----------------

A cipher has 3 components: a *signature scheme*, a *key exchange*, and *bulk encryption*:

### Signature scheme

The signature scheme defines a public and private key, both of which are stored in a [key file](keyfile.md). The private key (and hence the whole key file) must be kept secret, while the public key can be distributed. To allow for the distribution of the public key, a *public key string format* is defined: `scheme/key`, where `scheme` names the signature scheme, and `key` is some scheme-specific data which describes the public key. See documentation of specific ciphers for details on their specific formats.

Given the private key and a message *m*, the signature scheme can produce a value *s* which is specific to the message and the key. Someone who has the public key can take the value of *m*, *s*, and the public key, and verify, without knowing the private key itself, that *s* must have been correctly produced by the owner of the private key, hence acting as a "signature" of that person for the specific message.

### Key exchange

Each cipher also describes a method by which two connecting hosts can established a shared secret key without an interceptor being able to discover it.

### Bulk encryption

Bulk encryption uses a shared secret key to encrypt and decrypt message for a particular connection.

Cipher IDs and names
--------------------

Each cipher has a name and a 16-bit ID, used to identify it in key files, or for the user to be able to specify one on the command line. The value `0x0000` is reserved to mean "no cipher specified" where necessary. IDs starting from `0xF000` are for private and experimental use. The rest are defined here. The IDs and names are listed below:

|ID      |Name                                                  |
|--------|------------------------------------------------------|
|`0x0001`|[RSA4096-DH2048-AES128](rsa4096-dh2048-aes128.md)     |
