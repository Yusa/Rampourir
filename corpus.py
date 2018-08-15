import urllib2
import pandas as pd
import numpy as np
import os
import sqlite3
import commonFunctions
import sys
import requests
import datetime

_DATE = datetime.date.today()


def pandam():
	FNAME = os.path.join(commonFunctions._SCRIPT_PATH, "trackerHexEu.csv")
	saveFile = os.path.join(commonFunctions._SCRIPT_PATH, 'trackerHexEuURLS.stamp')

	response = urllib2.urlopen('http://tracker.h3x.eu/api/sites_1day.php')
	
	with open(FNAME,"wb") as f:
		f.write(response.read())
	data = pd.read_csv(FNAME)
	np.savetxt(saveFile, data.url, fmt="%s")
	os.remove(FNAME)
	return saveFile

def main():
	commonFunctions._CON = sqlite3.connect(commonFunctions.DBPATH)
	c = commonFunctions._CON.cursor()
	
	fname = pandam()
	with open(fname, "r") as f:
		lst = f.readlines()
		ln = len(lst)
		print "\n[*] {}/{} is in process. [*]".format(0,ln),
		sys.stdout.flush()
		for i,line in enumerate(lst):
			print '\r', "[*] {}/{} is in process. [*] ".format(i,ln),
			sys.stdout.flush()
			if commonFunctions.sampleDownloader(line.strip()):
				oldFile = os.path.join(commonFunctions.SAVEPATH, "temp")
				hashes = commonFunctions.hasher(oldFile)
				newFile = os.path.join(commonFunctions.SAVEPATH, str(hashes["md5"]))
				c.execute("""SELECT * FROM files WHERE md5sum=?""", (hashes["md5"],))
				if c.fetchone() == None:
					os.rename(oldFile, newFile)
	#				print hashes
					print "INSERTING"
					isDetected = False
					ScanResult = commonFunctions.yaraScan()
					if ScanResult != None:
						print ScanResult
						isDetected = True
					ssdeepResult = commonFunctions.checkSsdeep()

					c.execute("""INSERT INTO files values (?, ?, ?, ?, ?, ?, ?, ?)""", (hashes["md5"], hashes["sha256"], newFile, isDetected, ScanResult, _DATE, hashes["ssdeep"], None))
					commonFunctions._CON.commit()

	commonFunctions._CON.close()	

if __name__ == '__main__':
	main()