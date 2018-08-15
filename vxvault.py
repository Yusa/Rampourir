from bs4 import BeautifulSoup
import requests
import datetime
import commonFunctions
import sys
import os
import sqlite3


_DOWN_URL = "http://vxvault.net/URL_List.php"
_DATE = datetime.date.today()


def getUrls():
	result = str(requests.get(_DOWN_URL, headers=commonFunctions._HEADERS).text).split("\n")
	urls = []
	for line in result:
		if "http" in line:
			urls.append(line.strip())
	return urls



def main():
	commonFunctions._CON = sqlite3.connect(commonFunctions.DBPATH)
	c = commonFunctions._CON.cursor()
	
	result = getUrls()
	if result:
		print "\n[*] Download is starting...[*]",
		sys.stdout.flush()
		for i, res in enumerate(result):
			print '\r', "[*] {}/{} is in process. [*] ".format(i,len(result)),
			sys.stdout.flush()
			if  commonFunctions.sampleDownloader(res.strip()):
				oldfile = os.path.join(commonFunctions.SAVEPATH, "temp")
				hashes = commonFunctions.hasher(oldfile)
				newFile = os.path.join(commonFunctions.SAVEPATH, str(hashes["md5"]))
				c.execute("""SELECT * FROM files WHERE md5sum=?""", (hashes["md5"],))
				if c.fetchone() == None:
					os.rename(oldfile, newFile)
	#				print hashes
					print "INSERTING"
					isDetected = False
					ScanResult = commonFunctions.yaraScan(newFile)
					if ScanResult != None:
						print ScanResult
						isDetected = True
					ssdeepResult = commonFunctions.checkSsdeep()

					c.execute("""INSERT INTO files values (?, ?, ?, ?, ?, ?, ?, ?)""", (hashes["md5"], hashes["sha256"], newFile, isDetected, ScanResult, _DATE, hashes["ssdeep"], None))
					commonFunctions._CON.commit()






if __name__ == "__main__":
	main()