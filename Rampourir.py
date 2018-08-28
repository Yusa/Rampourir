#!/bin/python2
import os
import sys
import readline
import sqlite3
from tabulate import tabulate
import json

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')


reload(sys)
sys.setdefaultencoding('utf-8')


helpMsg = """Options:
SET PATH <path>			set the path to where the malwares are stored
SET DB	<path>			set the path to database the malwares are stored
SEARCH <hash> <hash> <hash>	to search files with hash
SHOW PATH			to show the current selected path for malwares to analyze
LIST				to list the files
CLEAR				to clear screen
EXIT				to exit
"""

defaultPath = None
defaultDb = None
searchPath = None
defaultConn = None

if os.path.exists("Malwares"):
	defaultPath = "Malwares"

if os.path.exists("veritabani.db"):
	defaultDb = "veritabani.db"
	defaultConn = sqlite3.connect(defaultDb)


print """
    ____                                         _     
   / __ \____ _____ ___  ____  ____  __  _______(_)____
  / /_/ / __ `/ __ `__ \/ __ \/ __ \/ / / / ___/ / ___/
 / _, _/ /_/ / / / / / / /_/ / /_/ / /_/ / /  / / /    
/_/ |_|\__,_/_/ /_/ /_/ .___/\____/\__,_/_/  /_/_/     
                     /_/                               
                                     """
print helpMsg

try:
	while True:
		cmd = str(raw_input("<CMD> "))
		command = cmd.split()

		#=========================================================================================================
		#Not to crash when enter pressed
		if len(command) == 0:
			continue
		#=========================================================================================================
		#SEARCH files
		if command[0].upper() == "SEARCH":
			if len(command) == 1:
				print "No hashes given"
				continue
			i = 1
			if defaultDb:
				while i < len(command):
					c = defaultConn.cursor()
					c.execute("""SELECT * FROM files WHERE md5sum = ? or sha256sum = ?""", (command[i],command[i],))
					result = c.fetchone()
					if result:
						print "\nSample exists for: {}\n".format(command[i])
						print tabulate([['MD5', result[0]], ['SHA256', result[1]], ['Filepath', result[2]], ['Is Detected', result[3]], ['Detected as', result[4]], ['Collection date', result[5]], ['SSDEEP Value', result[6]] ], headers=['Type', 'Value'], tablefmt='grid')
						if result[7]:
							print "\n"
							ssdeepres = result[7].replace("'", "\"")
							print tabulate(json.loads(ssdeepres).items(), headers=['Similar With', 'SSDEEP Similarity'], tablefmt='grid')
							print "\n"
					else:
						print "Sample doesn't exist with the given hash values: {}".format(command[i])
					i += 1		
			else:
				print "Set the database to view informations\n\tSET DB <FullPath>"

		#=========================================================================================================
		#SET variables
		elif command[0].upper() == "SET":
			if len(command) == 2:
				if command[1].upper() == "PATH":
					print "Please give the path to malwares\n\tSET PATH <FullPath>"
				elif command[1].upper() == "DB":
					print "Please give the path to database\n\tSET DB <FullPath>"
			elif len(command) == 3:
				if command[1].upper() == "PATH":
					if os.path.exists(command[2]):
						defaultPath = command[2]
					else:
						print "Path doesnt exist"
						print "Please give the path to malwares\n\tSET PATH <FullPath>"
				
				elif command[1].upper() == "DB":
					if os.path.exists(command[2]):
						defaultDb = command[2]
						defaultConn = sqlite3.connect(defaultDb)
					else:
						print "Path doesnt exist"
						print "Please give the path to database\n\tSET DB <FullPath>"

			else:
				print "Missing arguments\nexample:\tSET PATH\n\t\tSET DB"	
				print "Missing arguments"		

		#=========================================================================================================
		#SHOW variables
		elif command[0].upper() == "SHOW":
			if len(command) == 2:
				if command[1].upper() == "PATH":
					print "Path = {}".format(defaultPath)
				elif command[1].upper() == "DB":
					print "Database = {}".format(defaultDb)
				else:
					print "Wrong format, you can use as in example:\nexample:\tSHOW PATH"

			else:
				print "Missing arguments\nexample:\tSHOW PATH\n\t\tSHOW DB"	
				print "Missing arguments"	

		#=========================================================================================================
		#LIST files
		elif len(command) == 1 and command[0].upper() == "LIST":
			if defaultDb:
				c = defaultConn.cursor()
				c.execute("""SELECT md5sum FROM files""")
				myList = c.fetchall()
				for count, i in enumerate(myList):
					print "\t+----------------------------------+"
					print str(count + 1) + " :\t|",
					print i[0],
					print "|"

				print "\t+----------------------------------+\n"

				print "There are {} files...\n".format(len(myList))
			else:
				print "Please give the path to database\n\tSET PATH <FullPath>"

		#=========================================================================================================
		#CLEAR screen
		elif command[0].upper() == "CLEAR":
			if os.name == "nt":
				os.system('cls')
			else:
				os.system('clear')

		#=========================================================================================================
		#EXIT program
		elif command[0].upper() =="EXIT":
			print "\nBye\n"
			exit()

		else:
			print helpMsg


except KeyboardInterrupt:
	print "\nBye"