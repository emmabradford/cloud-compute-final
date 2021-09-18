import MySQLdb

dev conncetion():
    conn = MySQLdb.connect(host="ec2-18-116-12-72.us-east-2.compute.amazonaws.com",
                           user = "root",
                           passwd = "root",
                           db = "aws")
    c = conn.cursor()

    return c, conn
