import sys
from bitstring import BitArray
fileName = sys.argv[1]
f_in = open(fileName, 'rb')
f = f_in.read()
utf = ""
f_out = open("utf8encoder_out.txt" , 'wb')
for i in xrange(0,len(f),2):
	#print "character: "+f[i]+f[i+1]
	#print ord(f[i])
	#print ord(f[i+1])
	#print hex(ord(f[i]))
	#print hex(ord(f[i+1]))
	#print ord(f[i])+ord(f[i+1])
	hexv1 = hex(ord(f[i]))[2:]
	hexv2 = hex(ord(f[i+1]))[2:]
	if(len(hexv1)<2):
		for i in range(0,2-len(hexv1)):
			hexv1='0'+hexv1
	if(len(hexv2)<2):
		for i in range(0,2-len(hexv2)):
			hexv2='0'+hexv2
	
	#print "hex value:"+"0x"+hex(ord(f[i]))[2:][::-1]
	#if(len(hex(ord(f[i]))[2:])<=2):
	#hexv = "0x"+hex(ord(f[i]))[2:]+hex(ord(f[i+1]))[2:]
	hexv = '0x'+hexv1+hexv2
	#else:
	#	hexv = "0x"+hex(ord(f[i]))[2:][::-1]
	#print "Hex-value: "+hexv
	if(int(hexv,16) <= 0x7F):
		#print "one octet"
		#print "Converted to utf"
		bitstr = bin(int(hexv,16))[2:]
		length = len(bitstr)
		for l in range(0,7-length):
			bitstr = '0' + bitstr
		#print BitArray('0b'+'0'+bitstr)
		f_out.write(BitArray('0b'+'0'+bitstr).tobytes())
		utf = utf + '0'+bin(ord(f[i]))[2:]
	elif(int(hexv,16) >= 0x80 and int(hexv,16) <= 0x7FF):
		#print "two octets"
		bitstr = bin(int(hexv,16))[2:]
		length = len(bitstr)
		#print "length is"+str(length)
		#first fill second octet
		secondoctet = bitstr[length-6:length]
		if(len(secondoctet)<6):
			for l in range(0,6-len(secondoctet)):
				secondoctet = '0'+secondoctet
		secondoctet = '10'+secondoctet
		if(length>6):
			firstoctet = bitstr[0:length-6]
			if(len(firstoctet)<5):
				for l in range(0, 5-len(firstoctet)):
					firstoctet = '0'+firstoctet
			firstoctet = '110'+firstoctet
		else:
			firstoctet = '11000000'
		completeoctet = firstoctet+secondoctet
		#print BitArray('0b'+completeoctet)
		f_out.write(BitArray('0b'+completeoctet).tobytes())
			
	else:
		#print "three octets"
		bitstr = bin(int(hexv,16))[2:]
		#print bitstr
		length = len(bitstr)
		#print "length is"+str(length)
		thirdoctet = bitstr[length-6:length]
		if(len(thirdoctet)<6):
			for l in range(0,6-len(thirdoctet)):
				thirdoctet = '0'+thirdoctet
		thirdoctet = '10'+thirdoctet
		if(length<=6):
			#completeoctet = "1110000010000000"+thirdoctet
			firstoctet = '11100000'
			secondoctet = '10000000'
		else:
			secondoctet = bitstr[length-12:length-6]
			if(len(secondoctet)<6):
				for l in range(0,6-len(secondoctet)):
					secondoctet = '0'+secondoctet
			secondoctet = '10'+secondoctet
			if(length>12):
				firstoctet = bitstr[0:length-12] 
				if(len(firstoctet)<4):
					for l in range(0, 4-len(firstoctet)):
						firstoctet = '0'+firstoctet
				firstoctet = '1110'+firstoctet
			else:
				firstoctet = '11100000'
		completeoctet = firstoctet+secondoctet+thirdoctet
		#print '0b'+completeoctet
		#print BitArray('0b'+completeoctet)
		f_out.write(BitArray('0b'+completeoctet).tobytes())
	
		
#print "-----------------" 
#print utf

#f_out = open("output.txt" , 'w')
#f_out.write(utf)
f_in.close()
f_out.close()

# print ord('A')
# print hex(ord('A'))
#	print bin(65)
# print bin(int('0x41',16))
# print chr(65)

#print repr(f)
#print f.encode('hex')
#print type(f)
#print f[:10]