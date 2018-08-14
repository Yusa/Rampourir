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



def main():
	if _DEBUG:
		destroy_db()
		create_db()
	if not os.path.exists(commonFunctions.SAVEPATH):
		os.mkdir(commonFunctions.SAVEPATH)




if __name__ == "__main__":
	main()
	print "\n\nMALSHARE STARTS HERE\n\n"
	malshare.main()
	
	print "----"
