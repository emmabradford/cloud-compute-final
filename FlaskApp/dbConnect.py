import MySQLdb

dev conncetion():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "root",
                           db = "aws")
    c = conn.cursor()

    return c, conn
