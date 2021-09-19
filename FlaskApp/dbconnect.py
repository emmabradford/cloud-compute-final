import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "ubuntu",
                           db = "aws")
    c = conn.cursor()

    return c, conn
