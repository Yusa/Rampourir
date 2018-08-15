#!/bin/python2
import requests
import hashlib
import os
import progressbar
import ssdeep

_DB_NAME = "veritabani.db"
_CON = None


_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}

_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

SAVEPATH = os.path.join(_SCRIPT_PATH, "Malwares")

DBPATH = os.path.join(_SCRIPT_PATH, _DB_NAME)

if not os.path.exists(SAVEPATH):
	os.mkdir(SAVEPATH)


def sampleDownloader(url):
	try:
		req = requests.get(url.strip(), stream=True, headers=_HEADERS, timeout=5)
		#print "Sample download status code: {}".format(req.status_code)
		if req.status_code == 200:
		    with open(os.path.join(SAVEPATH,"temp"), 'wb') as f:
		        for chunk in req.iter_content(chunk_size=1024):
		            if chunk: # filter out keep-alive new chunks
		                f.write(chunk)
		 #       print "Succesfully sample downloaded"
		        return True
	#except requests.exceptions.ConnectionError as e:
	#	print e
	except KeyboardInterrupt:
		exit()
	except Exception as e:
		print "Host refused connection = {}".format(url)
		return False
	return False


def hasher(fname):
    #HASH md5
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    hmd5 = hash_md5.hexdigest()

    #HASH sha256
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    hsha256 = hash_sha256.hexdigest()
    
    #HASH ssdeep
    hssdeep = ssdeep.hash_from_file(fname)

    #return value
    return {"md5": hmd5, "sha256": hsha256, "ssdeep":hssdeep}



#NOT COMPLETE FUNCTIONS
def yaraScan():
	return None

def checkSsdeep():
	# it will check every file in database for similarity,
	# result of comparison with above 90% will be returned as json. 
	return None