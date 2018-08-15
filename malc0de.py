#!/bin/python2
import feedparser
import requests
import re
import os
import sqlite3
import commonFunctions
import progressbar
import sys
import datetime

CHECKFILE = os.path.join(commonFunctions._SCRIPT_PATH, "lastURLmalc0d.stamp") 
_DATE = datetime.date.today()


def process_xml_list_desc(response):
	feed = feedparser.parse(response)
	urls = set()
	isFirst = True

	if not os.path.exists(CHECKFILE):
		open(CHECKFILE,"wb").close()

	with open(CHECKFILE,"r") as f:
		checkerCurrent = f.read().strip()

	checkerUpdate = ""
	for entry in feed.entries:
		desc = entry.description
		url = desc.split(' ')[1].rstrip(',')
		if url == '':
			continue
		if url == '-':
			url = desc.split(' ')[4].rstrip(',')
		url = re.sub('&amp;', '&', url)
		if not re.match('http', url):
			url = 'http://' + url

		if isFirst:
			isFirst = False
			checkerUpdate = url

		if url.strip() == checkerCurrent:
			break #break if the link is downloaded in earlier run
		urls.add(url)


	with open(CHECKFILE,"wb") as f:
		f.write(checkerUpdate.strip())

	return urls

def malc0de():
	try:
		req = requests.get("http://malc0de.com/rss/", headers=commonFunctions._HEADERS)
		print "Status code of request malc0de.com/rss/: {}".format(req.status_code)
		if req.status_code == 200:
			return process_xml_list_desc(req.content)
		else:
			return None
	except requests.exceptions.ConnectionError as e:
		print e


def main():
	commonFunctions._CON = sqlite3.connect(commonFunctions.DBPATH)
	c = commonFunctions._CON.cursor()
	
	result = malc0de()
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



if __name__ == '__main__':
	main()
