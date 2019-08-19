#!/usr/bin/env python

import os
import ecdsa
import hashlib
import base58
import requests
import time
from smtplib import SMTP_SSL as SMTP
import logging
import blockcypher


wif = ""



logging.basicConfig(filename='BTC_PrivateKeys_'+time.strftime("%Y-%m-%d-%H-%M")+'.csv', \
level=logging.INFO, format='%(message)s', datefmt='%Y-%m-%d,%H:%M:%S')
logging.getLogger("requests").setLevel(logging.WARNING)
logging.info ('"Timestamp", "WifKey", "PublicAddress"')



def ping_address(publicAddress):
	global pk
	global wif
	global publicKey

	"""
	sends Request to a Block Explorer	
	Use blockcypher Python package to fetch unlimited balances...
	"""
	
	balance = blockcypher.get_total_balance(publicAddress)
	print balance

	# "WifKey", "HexKey", "PublicAddress", "PublicKey", "Balance"
	#Comment out this line if you wish to NOT record blank keys
	logging.info (''+ time.strftime("%m-%d-%y %H:%M:%S") +','+ wif +','+publicAddress)

	if float(balance) > 0.00000000:
		logging.info (''+ time.strftime("%m-%d-%y %H:%M:%S") +','+ wif +','+publicAddress+' ,balance '+balance)
		
		print "Congratulations...alert the world cause you just made some sort of history friend!"


def wif_conversion(pk):
	global wif
	padding = '80' + pk
	# print padding

	hashedVal = hashlib.sha256(padding.decode('hex')).hexdigest()
	checksum = hashlib.sha256(hashedVal.decode('hex')).hexdigest()[:8]
	# print hashedVal
	# print padding+checksum

	payload = padding + checksum
	wif = base58.b58encode(payload.decode('hex'))
	print wif
	

while True:

	pk = os.urandom(32).encode("hex")
	wif_conversion(pk)

	sk = ecdsa.SigningKey.from_string(pk.decode("hex"), curve = ecdsa.SECP256k1)
	vk = sk.verifying_key
	publicKey = ("\04" + vk.to_string())
	ripemd160 = hashlib.new('ripemd160')
	ripemd160.update(hashlib.sha256(publicKey).digest())
	networkAppend = '\00' + ripemd160.digest()
	checksum = hashlib.sha256(hashlib.sha256(networkAppend).digest()).digest()[:4]
	binary_address = networkAppend + checksum
	publicAddress = base58.b58encode(binary_address)
	print publicAddress
	while True:
		try:
			ping_address(publicAddress)	
		except ValueError:
			print "Aaaannnnd we got Timed Out"
			print pk
			print publicAddress
			time.sleep(3)
			continue
		except KeyError:
			print "we may be denied or something, keep the script moving"
			time.sleep(10)			
		break

# msg = "I own your Private Key for %s" %(publicAddress)
# signed_msg = sk.sign(msg)
# encoded_msg = signed_msg.encode("hex")
