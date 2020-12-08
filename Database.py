import sqlite3
import datetime, pytz

SQL_STATEMENT = """CREATE TABLE Reminder (
	Id INTEGER PRIMARY KEY AUTOINCREMENT,
	Mentions VARCHAR(30),
	Messages VARCHAR(50),
	Day datetime(50)
	);"""


def connect(i):
	global con, cur
	con = sqlite3.connect("Database/"+str(i)+".db")
	cur = con.cursor()
	try:
		cur.execute(SQL_STATEMENT)
	except:
		return


def insert(i,j,k):
	cur.execute("INSERT INTO Reminder (Mentions, Messages, Day) VALUES (?,?,?);", (i,j,k))
	con.commit()
	con.close()


def search():
	#pytz.timezone("Asia/Kuala_Lumpur")
	dt=datetime.datetime.now().astimezone(pytz.timezone("Asia/Kuala_Lumpur")) + datetime.timedelta(minutes=10)
	cur.execute("SELECT Id, Mentions, Messages FROM Reminder WHERE Day < ?;",(dt.strftime("%c"),))
	return cur.fetchall()


def remove(i):
	cur.execute("DELETE FROM Reminder WHERE Id=?", (i,))


def close():
	con.commit()
	con.close()

#t=datetime.datetime(year=2022,month=11,day=4,hour=21,minute=45)>datetime.datetime.now()
#connect('happy')
#insert("as","sb","er","ty")

#insert("sgfg","wer",datetime.datetime.now())
#close()
#print(datetime.datetime.now(pytz.timezone("Asia/Kuala_Lumpur")))
