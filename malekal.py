from pyquery import PyQuery
import requests
import sqlite3
import commonFunctions
import argparse
import datetime
import sys, os

parser = argparse.ArgumentParser(description='Malekal downloader tool.')
parser.add_argument('--hashes', dest='downHashes', action='store_true',
					help='To download samples need to download hashes first. It will take a while')
parser.add_argument('--samples', dest='downSamples', action='store_true',
					help='Use it if hashes were already downloaded')

args = parser.parse_args()


_DOWN_URL = "http://malwaredb.malekal.com/files.php?file="
_HASHFILE = "malekalmd5.stamp"
_DATE = datetime.date.today()


commonFunctions._CON = sqlite3.connect(commonFunctions._DB_NAME)
cursor = commonFunctions._CON.cursor()			


def download_hashes():
	arr = []
	try:
		for index in range(829) :
			print '\r', "[*] page {}/829 is downloaded. [*] ".format(index),
			sys.stdout.flush()

			x = requests.get("http://malwaredb.malekal.com/index.php?page={}".format(index), headers=commonFunctions._HEADERS)
			pq = PyQuery(x.text)
			table = pq.find("table")
			for tr in table.find("tr").items():
				for td in tr.find("td").items():
					if all(i in str(td) for i in ("MD5", "SHA1", "SHA256")):
						arr.append(td.text().split()[1])

			with open(_HASHFILE, "a") as f:
				for i in arr:
					f.write(i + "\n")
			arr = []

	except KeyboardInterrupt:
		exit()
	except Exception as e:
		print e
		pass
		

def downloadSamples():
	with open(_HASHFILE, "r") as f:
		hashlist = f.readlines()
		for i,line in enumerate(hashlist):
			try:
				ln = len(hashlist)
				line = "{}{}".format(_DOWN_URL,line.strip())
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
				print "[!] Error: malekal.py - main function - for loop!"




def main():
	if args.downHashes:
		download_hashes()
	elif args.downSamples:
		downloadSamples()
	else:
		exit()



if __name__ == "__main__":
	main()