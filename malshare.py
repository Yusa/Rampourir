from bs4 import BeautifulSoup
import requests
import pprint
import datetime
import commonFunctions
import sys
import os 
import json

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
_HASHFNAME = "sha256Malshare"

with open("configs", "r") as f:
	CONFS = json.loads(f.read())

_API_KEY = CONFS['MALSHARE-API']


def retrieve_hashes(url):
	"""
	Parameters
		url : url of the html file that will be downloaded

	Returns 1 if the file retrieved without problem
			0 if there is a problem
	"""
	try:
		response = requests.get(url, headers=_HEADERS)
#		soup = BeautifulSoup(response.text, 'html.parser')
		with open(_HASHFNAME, "w") as f:
			f.write(response.text)
		return 1
	except:
		print "[!] Error: malshare.py - retrieve_hashes function!"
		return 0


def main():
	_DATE = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
	_URL = "https://malshare.com/daily/{}/malshare_fileList.{}.sha256.txt".format(_DATE, _DATE)
	cursor = commonFunctions._CON.cursor()
	if retrieve_hashes(_URL):
		with open(_HASHFNAME, "r") as f:
			hashlist = f.readlines()
			for i,line in enumerate(hashlist):
				try:
					ln = len(hashlist)
					line = "https://malshare.com/api.php?api_key={}&action=getfile&hash={}".format(_API_KEY,line)
					print '\r', "[*] {}/{} is downloaded. [*] ".format(i,ln),
					sys.stdout.flush()
					if commonFunctions.sampleDownloader(line.strip()):
						oldFile = os.path.join(commonFunctions.SAVEPATH, "temp")
						hashes = commonFunctions.hasher(oldFile)
						newFile = os.path.join(commonFunctions.SAVEPATH, str(hashes["md5"]))
						os.rename(oldFile, newFile)
						cursor.execute("""SELECT * FROM files WHERE md5sum=?""", (hashes["md5"],))
						if cursor.fetchone() == None:
							#print hashes
							print "INSERTING"
							cursor.execute("""INSERT INTO files values (?, ?, ?, ?, ?, ?, ?, ?)""", (hashes["md5"], hashes["sha256"], newFile, False, None, _DATE, None, None))
							commonFunctions._CON.commit()


				except Exception as e:
					print e
					print "[!] Error: malshare.py - main function - for loop!"


if __name__=="__main__":
	main()