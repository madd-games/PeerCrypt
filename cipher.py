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