# -*- coding:utf-8 -*-
#!/usr/bin/python3

import os           
import random

from ctypes import *

import time

from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.ecgroup import ECGroup
from charm.toolbox.eccurve import prime192v2
from charm.schemes.pkenc.pkenc_cs98 import CS98

# mg07a
from pre_mg07a_jet import PreGA

from fibre import ible

#************************M is the matrix order, kn of c file, should be preset********
m=64
#*************************************************************************************


group = PairingGroup('SS512', secparam=1024)
groupcs98 = ECGroup(prime192v2)

pkenc = CS98(groupcs98)
pre = PreGA(group, pkenc)

# PRE SETUP
(mk, params) = pre.setup()

k = 'k' * 16  # 128 bits
SymKey = k.encode('utf-8')


# Generate secret key for ID1
ID1 = "Harry_Potter@gmail.com"
ID2 = "Jet_Luo@gmail.com"


f_log = open("Record.log", "w")
localtime = time.asctime(time.localtime(time.time()))
# Trace File comments.
f_log.write("#Created @ ")
f_log.write(str(localtime))
f_log.write("\n#SymE\tKeyIBE\tKeyIBD\tSymD\tT_key\tAncor\n")



# Run counts
count = 50

while count >= 1:
	print('Run count:%d\n'%count)

	with open("XORtemp.txt") as ifile:
		a=ifile.read()
		n = len(a)//m     
		ss = [a[i:i + n] for i in range(0, len(a), n)]
		randa = random.randrange(0, m)
		sa = ss[randa]
		sma = sa.encode('utf-8')
		#print ('Anchor Share:', sa)

	

	sx=ible(pre, ID1, sma,SymKey, mk, params, f_log)   #The anchor share encryption and decryption operation

	if sx!=sma:raise "Anchor share decryption error"

	
	#File correctness comparison
	with open("Rmessage.txt") as rfile:
		with open("Smessage.txt") as sfile:
			r=rfile.read()
			s=sfile.read()
			if r!=s:
				raise Exception("Message recovery error")
			else: 
				print('Recovery Successed!')
	
	count -= 1



f_log.close()



