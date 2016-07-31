import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",user = "root", passwd = "nepal", db="MajorProject")
    
    c= conn.cursor()
    
    return c, conn
    

