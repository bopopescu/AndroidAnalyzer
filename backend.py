import sqlite3

#Set this to true to send debug data to std out rather than db.
debug = False

#the global database connection object.
conn = None

'''
Creats a SQLite db and tables.
Returns the cursor for the db.
'''
def getDB(path):
   #get SQLite connection
    global conn
    conn = sqlite3.connect(path)
    c = conn.cursor()

    createDB(c)
    return c
'''
Create SQLite database from schema
'''
def createDB(cursor):
    cursor.execute('''
	CREATE TABLE IF NOT EXISTS app (
		id INTEGER PRIMARY KEY UNIQUE,
		package TEXT,
		appname TEXT,
        shortFileNames INTEGER,
        longFileNames INTEGER
	);
	''')
    cursor.execute('''
	CREATE TABLE IF NOT EXISTS keys (
		id INTEGER PRIMARY KEY UNIQUE,
		appID INTEGER,
		varName TEXT,
		value TEXT,
		filename TEXT,
		FOREIGN KEY(appID) REFERENCES app(id)
	);
	''')
    cursor.execute('''
	CREATE TABLE IF NOT EXISTS http (
		id INTEGER PRIMARY KEY UNIQUE,
		appID INTEGER,
		type TEXT,
		filename TEXT,
		value TEXT,
                FOREIGN KEY(appID) REFERENCES app(id)
	);
	''')

'''
Saves key data to the SQLite database
'''
def saveKey(appID, filename, keyID, value, cursor):
    if debug:
        print keyID
        print value
        #print calcEntropy(value, range_printable)
    else:
        cursor.execute("INSERT INTO keys VALUES (?, ?, ?, ?, ?)",
            [None,  # let sqlite3 pick an ID for us
            appID, keyID, value, filename])

'''
Saves http data to the SQLite database
'''
def saveHTTP(appID, filename, connType, urlstr, cursor):
    if debug:
        print urlstr.strip()
    else:
        cursor.execute("INSERT INTO http VALUES (?, ?, ?, ?, ?)",
        [None,  # let sqlite3 pick an ID for us
        appID, connType, filename, urlstr])
'''
Saves app information to the SQLite database.
Returns the database ID.
'''
def saveApp(package, appName, cursor, shortFileNames, longFileNames):
    cursor.execute("INSERT INTO app VALUES (?, ?, ?, ?, ?)",
        [None,  # let sqlite3 pick an ID for us
        package, appName, shortFileNames, longFileNames])
    if cursor.lastrowid != None:
            return cursor.lastrowid
    else:
            return -1

'''
Updates app information with filename length counts
'''
def saveFileNameLengths(appID, cursor, shortFileNames, longFileNames):
    cursor.execute('''UPDATE app 
        SET shortFileNames = ?, longFileNames = ? 
        WHERE id = ?''',
        [shortFileNames, longFileNames, appID])

'''
Cleans up and commits any dirty database data.
'''
def close():
    global conn
    if conn != None:
        conn.commit()
    else:
        print " CONN= NONE!"
