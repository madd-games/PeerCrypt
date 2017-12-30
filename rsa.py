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

import math
import random
import tools

def generatePrime(size):
	n = 0
	nIsPrime = False
	while not nIsPrime:
		while True:
			while True:
				n = random.getrandbits(size)
				smallPrimes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 
				139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 
				311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 
				491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 
				683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 
				887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
				prime = True
				for prime in smallPrimes:
					if n % prime == 0:
						prime = False
						break
				if prime:
					break
					
			
			if pow(2, n-1, n) == 1:			#Fermat test
				break
		
		r, s = 0, n - 1
		while s % 2 == 0:
			r += 1
			s //= 2
		
		nIsPrime = True					#Miller-Rabin test
		for k in range(1, 20):
			a = random.randrange(2, n - 1)
			x = pow(a, s, n)
			if x == 1 or x == n - 1:
				continue
			for _ in xrange(r - 1):
				x = pow(x, 2, n)
				if x == n - 1:
					break
			else:
				nIsPrime = False
				break
	return n
	
def generateKey(size):
	p = generatePrime(size/2)
	q = generatePrime(size/2)
	n = p*q
	
	e = 65537
	
	def egcd(a, b):
		if a == 0:
			return (b, 0, 1)
		else:
			g, y, x = egcd(b % a, a)
			return (g, x - (b // a) * y, y)
			
	k = (p-1) * (q-1)
	
	def modinv(a, m):
		g, x, y = egcd(a, m)
		if g != 1:
			raise Exception('modular inverse does not exist')
		else:
			return x % m
		
	d = modinv(e, k)
	
	
	return (n, d)
	
def rsa4096_keygen():
	return generateKey(4096)
	
def rsa4096_keystore(key, name):
	f = open(name, "wb")
	f.write("KEY\0\0\1")
	f.write(tools.longToBigEndian(key[0], 512))
	f.write(tools.longToBigEndian(key[1], 512))
	f.close()
	

def rsa4096_keystr(key):
	n=key[0]
	alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._"
	s = ""
	while n != 0:
		d = n%64
		n = n/64
		s = alphabet[d] + s
	return "RSA4096/" + s

def rsa4096_keyload(f):
	nstr = f.read(512)
	dstr = f.read(512)
	
	if (len(nstr) != 512) or (len(dstr) != 512):
		raise Exception('RSA4096 key corrupted')

	end = f.read(1)
	if end != "":
		raise Exception('RSA4096 key corrupted')
	
	n = tools.bigEndianToLong(nstr)
	d = tools.bigEndianToLong(dstr)
	return (n, d)

def rsa4096_sign(m, key):
	n, d = key
	return pow(m, d, n)

def rsa4096_verify(m, sig, keystr):
	if not keystr.startswith("RSA4096/"):
		return False
	s = keystr.split("/", 1)[1]
	alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._"
	n = 0
	for c in s:
		if c not in alphabet:
			return False
		n = n * 64 + alphabet.find(c)
	return pow(sig, 65537, n) == m

if __name__ == "__main__":
    print generateKey(4096)
