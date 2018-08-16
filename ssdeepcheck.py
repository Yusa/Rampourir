import sqlite3
import ssdeep
import commonFunctions
import os
import json

if os.path.exists(commonFunctions.DBPATH):
	connDB = sqlite3.connect(commonFunctions.DBPATH)
else:
	print "[!] Database doesn't exist\n[*] Run Allonsy.py to collect samples first."
	exit()


'''
	Match format = {
					'hash':'match-level', 
					'hash':'match-level',
					'hash':'match-level', 
					'hash':'match-level', 
				   }
'''


def ssdeepNewEntry(hash1, ssdeep1):
	'''
		function to use when new data is added to database
	'''
	cursor = connDB.cursor()
	cursor.execute("""SELECT * FROM files""")
	res = cursor.fetchone()
	while res:
		check_result = checker(res[6], ssdeep1)
		if int(check_result) > 90 and res[0] != hash1:
			updateOther(res[0], hash1, check_result)
			updateOther(hash1, res[0], check_result)
		res = cursor.fetchone()	


def updateOther(hash1, hash2, similarity):
	'''
		hash1 = hash of the sample whom value will be updated
		hash2 = hash of the sample in progress
	'''
	cursor = connDB.cursor()
	cursor.execute("""SELECT * FROM files WHERE md5sum=?""",(hash1,))
	target = cursor.fetchone()
	if target:
		currentSsdeep = target[7]
		if currentSsdeep == None:
			newSsdeep = {hash2.encode("ascii"):str(similarity).encode("ascii")}

			cursor.execute("""UPDATE files SET ssdeepSimilar=(?) WHERE md5sum=(?)""", (str(newSsdeep), hash1,))
		else:
			currentSsdeep = currentSsdeep.replace("'", "\"")
			currentSsasJson = json.loads(currentSsdeep)
			if not hash2 in currentSsasJson.keys():
				currentSsasJson[hash2.encode("ascii")] = str(similarity).encode('ascii')
			cursor.execute("""UPDATE files SET ssdeepSimilar=(?) WHERE md5sum=(?)""", (json.dumps(currentSsasJson), hash1,))
		connDB.commit()



def checker(hash1, hash2):
	'''
	given to hashes as string, returns the similarity percentage as integer
	'''
	return ssdeep.compare(hash1,hash2)



def main():
	cursor = connDB.cursor()
	cursor.execute("""SELECT * FROM files""")
	cursor2 = connDB.cursor()
	cursor2.execute("""SELECT * FROM files""")

	res = cursor.fetchone()
	cursor2.fetchone()
	i = 1
	while res:
		res2 = cursor2.fetchone()
		while res2:
			check_result = checker(res[6],res2[6])
			if int(check_result) > 90:
				updateOther(res[0], res2[0], check_result)
				updateOther(res2[0], res[0], check_result)
			#	print "{} - {} -> result: {}".format(res[0], res2[0], check_result)
			res2 = cursor2.fetchone()


		cursor2.execute("""SELECT * FROM files""")
		cursor2.fetchmany(i+1)
		res = cursor.fetchone()
		i += 1

if __name__ == "__main__":
	main()
