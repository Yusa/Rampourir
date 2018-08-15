import sqlite3
import os
import commonFunctions
import malshare
import malc0de
import vxvault
import corpus

_DEBUG = False


def destroy_db():
	if os.path.exists(commonFunctions._DB_NAME):
		os.remove(commonFunctions._DB_NAME)


def create_db():
	commonFunctions._CON = sqlite3.connect(commonFunctions._DB_NAME)
	cursor = commonFunctions._CON.cursor()
	cursor.execute('''CREATE TABLE files
				(md5sum text, sha256sum text, fname text, isDetected boolean, detection text, date date, ssdeep text, ssdeepSimilar text)''')

	cursor.execute('''CREATE TABLE timestamps
				(malshare date)''')


def clear_dir(topdir):
	for root, dirs, files in os.walk(topdir, topdown=False):
	    for name in files:
	        os.remove(os.path.join(root, name))
	    for name in dirs:
	        os.rmdir(os.path.join(root, name))


def main():
	#if in debug mode recreate database every run
	if _DEBUG:
		clear_dir(commonFunctions.SAVEPATH)
		destroy_db()
		create_db()
		if os.path.exists(malc0de.CHECKFILE):
			os.remove(malc0de.CHECKFILE)

	if os.path.exists(commonFunctions._DB_NAME):
		commonFunctions._CON = sqlite3.connect(commonFunctions._DB_NAME)
	else:
		create_db()

	#check if the directory where samples will be stored exists or not
	if not os.path.exists(commonFunctions.SAVEPATH):
		os.mkdir(commonFunctions.SAVEPATH)

	###################################################################
	print "\n\nMALSHARE STARTS HERE\n\n"
	malshare.main()	
	print "----"

	###################################################################
	print "\n\nMALC0DE STARTS HERE\n\n"
	malc0de.main()	
	print "----"

	###################################################################
	print "\n\VXVAULT STARTS HERE\n\n"
	vxvault.main()	
	print "----"

	###################################################################
	print "\n\CORPUS STARTS HERE\n\n"
	corpus.main()	
	print "----"

	###################################################################

if __name__ == "__main__":
	main()
