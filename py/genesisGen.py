import json
import codecs
from Crypto.Hash import keccak
import sys
import os
import ecdsa

nodes_path = sys.argv[1]
number_node =  sys.argv[2]
chain_id = int(sys.argv[3])
def exportGenesis(consortium,chainId):
	pubKeyList = readPubKeys()
	addressList = getAdresses(pubKeyList)
	res = {}
	if consortium == "poa" :
		res = cliqueGenesis(addressList,chainId)
	with open(nodes_path+"/genesis.json", "w") as outfile :
		json.dump(res, outfile)
	outfile.close()
	return
def cliqueGenesis(addresses,chainId):
	res = baseGenesis()
	res["alloc"]= {
		addresses[0][2:]: {
			"balance": "0x2000000000000000000000000000000000000000000000"
		},
		addresses[1][2:] : {
			"balance": "0x2000000000000000000000000000000000000000000000"
		}
	}
	concataddress = "0x0000000000000000000000000000000000000000000000000000000000000000"
	for address in addresses :		
		concataddress += address[2:]
	concataddress += "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
	res["extraData"] = concataddress
	res["config"] = {
		"chainId": chainId,
		"homesteadBlock": 0,
		"eip150Block": 0,
		"eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
		"eip155Block": 0,
		"eip158Block": 0,
		"byzantiumBlock": 0,
		"constantinopleBlock": 0,
		"petersburgBlock": 0,
		"istanbulBlock": 0,
		"clique": {
			"period": 10,
			"epoch": 30000
		}
		}
	res["nonce"] = "0x0"
	res["difficulty"] = "0x1"
	res["timestamp"] = "0x5d934f79"
	return res

def baseGenesis():
	return {
		"mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
		"coinbase": "0x0000000000000000000000000000000000000000",
		"parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
		"gasLimit": "0x47b760"
	}
def getAdresses(pubKeyList):
	res = []
	for pubKey in pubKeyList :
		res.append(public_to_address(pubKey.strip()))
	return res
def readPubKeys():
	res = []
	for i in range(1, int(number_node)+1):
		filename = nodes_path+"/node_"+str(i)+"/keys/pub.key"
		fileReader = open(filename, "r")
		currentLine = fileReader.readline()
		while currentLine != "" :
			res.append(currentLine.strip())
			currentLine = fileReader.readline()
		fileReader.close()
	return res

def public_to_address(public_key):
	public_key_bytes = codecs.decode(public_key, "hex")
	keccak_hash = keccak.new(digest_bits=256)
	keccak_hash.update(public_key_bytes)
	keccak_digest = keccak_hash.hexdigest()
	# Take last 20 bytes
	wallet_len = 40
	wallet = "0x" + keccak_digest[-wallet_len:]
	return wallet

if __name__ == "__main__":
    exportGenesis("poa", chain_id)
