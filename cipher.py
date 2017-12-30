"""
	PeerCrypt

	Copyright (c) 2018, Madd Games.
	All rights reserved.
	
	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:
	
	* Redistributions of source code must retain the above copyright notice, this
	  list of conditions and the following disclaimer.
	
	* Redistributions in binary form must reproduce the above copyright notice,
	  this list of conditions and the following disclaimer in the documentation
	  and/or other materials provided with the distribution.
	
	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
	FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
	DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
	CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
	OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from rsa import *

"""
List of ciphers.

Each entry is a tuple describing a single cipher. The elements of the tuple, in order, are:

	0	id				A unique cipher ID used in key files as well as the protocol.
	1	name				Name of the cipher; a human-readable identifier for commands etc.
	2	keygen()			A function which takes no arguments and returns a description of a new key.
	3	keystr(key)			Returns a public key string used to identify the public part of the key, in such a way that
						it can be copied by a human and pasted somewhere.
	4	keystore(key, filename)		Save the given key description into a ".key" file.
	5	keyload(f)			Load a key description (and return it) from the given file pointer, whose position is right be
						beyond the cipher ID in the file.
	6	sign(m, key)			Return the signature for hashed message "m" using the given key.
	7	verify(m, sig, keystr)		Verify that the signautre "sig" is valid for message "m" with public key string "keystr" (as given
						by keystr() )
"""
cipherList = [
	(0x0001, 'RSA4096-DH2048-AES128', rsa4096_keygen, rsa4096_keystr, rsa4096_keystore, rsa4096_keyload, rsa4096_sign, rsa4096_verify)
]

def getCipherByName(name):
	for cipher in cipherList:
		if cipher[1] == name:
			return cipher
	raise Exception('cipher name not found')

def getCipherByID(id):
	for cipher in cipherList:
		if cipher[0] == id:
			return cipher
	raise Exception('cipher ID not found')
	
def loadKey(name):
	f = open(name, "rb")
	if f.read(4) != "KEY\0": 
		raise Exception('invalid key file')
	
	cidstr = f.read(2)
	if len(cidstr) != 2:
		raise Exception('invalid key file')
	
	cid = int(tools.bigEndianToLong(cidstr))
	ciph = getCipherByID(cid)
	key = ciph[5](f)
	f.close()
	return (ciph, key)
