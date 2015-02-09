#Create mysql connection
import MySQLdb

db = MySQLdb.connect(host="", # your host, usually localhost
                     user="user", # your username
                      passwd="", # your password
                      db="sensors") # name of the data base
cur = db.cursor() 
cur.execute("""Insert into sensors.tree values (%s,sysdate())""", ('on')) 
