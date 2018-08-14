import sqlite3
import os
import commonFunctions
import malshare

_DEBUG = True


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




if __name__ == "__main__":
	main()
