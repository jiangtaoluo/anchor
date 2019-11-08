# -*- coding:utf-8 -*-
#!/usr/bin/python3
#set the num in the ss_xor_encrypt.cc and ss_xor_decrypt.cc be 1.
#steps:
#     1)  python t3.py
#     2)  ./processall
#And this code can test the whole step operation time
#This code has a out of memory peoblem ,so the algorithm efficient test is better operated in t.py.
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


# (public_key, secret_key) = pkenc.keygen()

# Generate secret key for ID1
ID1 = "Harry_Potter@gmail.com"
ID2 = "Jet_Luo@gmail.com"

#************Call the shell script and compile the cc file first,generat the so file**************#
n=os.system('process.sh') 
#*************************************************************************************************#


f_log = open("Record.log", "w")
localtime = time.asctime(time.localtime(time.time()))
# Trace File comments.
f_log.write("#Created @ ")
f_log.write(str(localtime))
f_log.write("\n#SymE\tKeyIBE\tKeyIBD\tSymD\tT_key\tAncor\n")



# Run counts
count = 10

while count >= 1:
	print('Run count:%d\n'%count)

	
	enc = cdll.LoadLibrary("encrypt.so")
	dec=cdll.LoadLibrary("decrypt.so")
	
	#Time starts from the XOR calculation
	t1=time.time()
	
	enc.main()
	
	t2=time.time()   #End of XOR operation

	del enc
	

	with open("XORtemp.txt") as ifile:
		a=ifile.read()
		n = len(a)//m     
		ss = [a[i:i + n] for i in range(0, len(a), n)]
		randa = random.randrange(0, m)
		sa = ss[randa]
		sma = sa.encode('utf-8')
		#print ('Anchor Share:', sa)

	

	t_IBSS1=(t2-t1)*1000
	print('XOR encryption operation time：',t_IBSS1)

	sx=ible(pre, ID1, sma,SymKey, mk, params, f_log)  #The anchor share encryption and decryption operation

	if sx!=sma:raise "Anchor share decryption error"

	
	#Message recovery
	t3=time.time()
	
	dec.main()

	
	#File correctness comparison
	with open("Rmessage.txt") as rfile:
		with open("Smessage.txt") as sfile:
			r=rfile.read()
			s=sfile.read()
			if r!=s:
				raise Exception("Message recovery error")
			else: 
				print('Recovery Successed!')
	
	
	t4=time.time()
	del dec
	t_IBSS2=(t4-t3)*1000
	print('XOR decryption and file comparison operation time：',t_IBSS2)
	t_IBSS=t_IBSS1+t_IBSS2
	print('Total XOR encryption and decryption time：',t_IBSS)

	log = '{0:.4f}'.format(t_IBSS) + "\n"

	f_log.write(log)
	
	count -= 1



f_log.close()



