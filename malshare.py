from bs4 import BeautifulSoup
import requests
import pprint
import datetime
import commonFunctions
import sys
import os 
import json

_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
_HASHFNAME = "sha256Malshare.stamp"

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

def checkDate(date):
	cursor = commonFunctions._CON.cursor()
	cursor.execute("""SELECT * FROM timestamps""")
	data = cursor.fetchone()
	yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
	if data == None:
		return 1
	elif data[0] == None or datetime.datetime.strptime(data[0].strip(),"%Y-%m-%d") < datetime.datetime.strptime(yesterday.strip(),"%Y-%m-%d"):
		return 2
	return 0

def main():
	# at every run it checks date and starts download then.
	_DATE = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
	chdRes = checkDate(_DATE)
	_URL = "https://malshare.com/daily/{}/malshare_fileList.{}.sha256.txt".format(_DATE, _DATE)
	if chdRes == 1:
		cursor = commonFunctions._CON.cursor()
		cursor.execute("""INSERT INTO timestamps values (?)""", (_DATE,))
		commonFunctions._CON.commit()
	
	elif chdRes == 2:
		cursor = commonFunctions._CON.cursor()
		cursor.execute("""UPDATE timestamps SET malshare = (?)""", (_DATE,))
		commonFunctions._CON.commit()

	else:
		return

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
						cursor.execute("""SELECT * FROM files WHERE md5sum=?""", (hashes["md5"],))
						if cursor.fetchone() == None:
							os.rename(oldFile, newFile)
							#print hashes
							print "INSERTING"
							isDetected = False
							ScanResult = commonFunctions.yaraScan()
							if ScanResult != None:
								print "detected"
								isDetected = True

							cursor.execute("""INSERT INTO files values (?, ?, ?, ?, ?, ?, ?, ?)""", (hashes["md5"], hashes["sha256"], newFile, isDetected, ScanResult, _DATE, hashes["ssdeep"], None))
							commonFunctions._CON.commit()
						else:
							os.remove(oldFile)

				except Exception as e:
					print e
					print "[!] Error: malshare.py - main function - for loop!"


if __name__=="__main__":
	main()