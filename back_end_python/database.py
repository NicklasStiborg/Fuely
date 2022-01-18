import sqlite3

#queries
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS fuels (id INTEGER PRIMARY KEY, date DATE, provider_name TEXT, price_95 FLOAT, price_d FLOAT);"
INSERT_DATA = "INSERT INTO fuels (date, provider_name, price_95, price_d) VALUES (?, ?, ?, ?);"
GET_ALL = "SELECT * FROM fuels;"
GET_PROVIDER = "SELECT * FROM fuels WHERE name = ?;"
GET_BEST_PRICE_95 = "SELECT * FROM fuels ORDER BY price_95 LIMIT 1;"
GET_BEST_PRICE_D = "SELECT * FROM fuels ORDER BY price_d LIMIT 1;"
GET_NEWEST_PRICES = "SELECT * FROM fuels ORDER BY date DESC LIMIT 6;"

def connect():
    return sqlite3.connect("data.db", check_same_thread=False)

def createTables(connection):
    with connection:
        connection.execute(CREATE_TABLE)

def addData(connection, date, provider_name, price_95, price_d):
    with connection:
        connection.execute(INSERT_DATA, (date, provider_name, price_95, price_d))

def getAll(connection):
    with connection:
        return connection.execute(GET_ALL).fetchall()

def getProvider(connection, name):
    with connection:
        return connection.execute(GET_PROVIDER, (name,)).fetchall()

def bestPrice95(connection):
    with connection:
        return connection.execute(GET_BEST_PRICE_95).fetchone()

def bestPriceD(connection):
    with connection:
        return connection.execute(GET_BEST_PRICE_D).fetchone()

def newestPrice(connection):
    with connection:
        return connection.execute(GET_NEWEST_PRICES).fetchall()
