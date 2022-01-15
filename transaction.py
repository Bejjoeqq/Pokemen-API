import sqlite3
from crypt import encrypt

rnge = [[175,175],[180,200],[201,250],[251,300],[301,350],[351,400],[401,450],[451,500],[501,600],[601,700],[701,800],[801,1500]]

def select(q):
    connection = sqlite3.connect('herodb.db')
    cursor = connection.cursor()

    cursor.execute(q)
    result =  cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def setLogin(user,paswd):
	encrypted = encrypt(paswd)
	query = f"SELECT account_id,email,password FROM account WHERE email='{user}' AND password='{encrypted}'"
	result = select(query)
	return result

def getUsers(accid):
	query = f"SELECT a.user_id,a.name,b.namex,(a.power+b.powerx),(a.hp+b.hpx),(a.atk+b.atkx),(a.def+b.defx),(a.satk+b.satkx),(a.sdef+b.sdefx),(a.speed+b.speedx),a.floor,a.exp_user,a.exp_poke,a.poke_idx,a.diamond,a.pokecoin,a.pokeball,a.stardust,a.account_id FROM user a LEFT JOIN pokex b ON a.poke_idx = b.poke_idx WHERE a.account_id = {accid}"
	result = select(query)
	return result

def getNChat():
	query = "SELECT c.name,a.message FROM chat a LEFT JOIN account b ON a.account_id=b.account_id LEFT JOIN user c ON b.account_id=c.account_id ORDER BY chat_id DESC LIMIT 100"
	temp = select(query)
	result = list()
	for x in temp:
		result.append(
				{
					"name" : x[0],
					"message" : x[1]
				}
			)
	return result

def setNChat(user,msg):
	connection = sqlite3.connect('herodb.db')
	query = "INSERT INTO chat(message,account_id) VALUES(?,?);"
	cursor = connection.cursor()

	cursor.execute(query,[msg,user])
	connection.commit()

	cursor.close()
	connection.close()

def getLeader():
	query = "SELECT a.name,(a.power+b.powerx),a.exp_user FROM user a LEFT JOIN pokex b ON a.poke_idx = b.poke_idx ORDER BY a.exp_user DESC LIMIT 10;"
	temp = select(query)
	result = list()
	for x in temp:
		result.append(
				{
					"name" : x[0],
					"power" : x[1],
					"exp" : x[2]
				}
			)
	return result

def setRegis(user,name):
	try:
		connection = sqlite3.connect('herodb.db')
		query = "INSERT INTO user(name,power,hp,atk,def,satk,sdef,speed,floor,exp_user,exp_poke,account_id,poke_idx,diamond,pokecoin,pokeball,stardust) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
		cursor = connection.cursor()

		cursor.execute(query,[name,0,0,0,0,0,0,0,0,0,0,user,1,0,0,0,100])
		connection.commit()

		cursor.close()
		connection.close()

		query = f"SELECT user_id FROM user WHERE account_id = {user}"
		result = select(query)[0][0]
		insertState(user)
		return True
	except:
		return False

def minStardust():
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	query = "SELECT user_id,stardust FROM user"
	userCollection = select(query)

	for x in userCollection:
		if x[1]<100:
			crud_query = f"UPDATE user set stardust = stardust + 1 WHERE user_id = {x[0]}"
			cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def setNStardust(user,n):
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	crud_query = f"UPDATE user set stardust = stardust + {n} WHERE user_id = {user}"
	cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def setNPokecoin(user,n):
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	crud_query = f"UPDATE user set pokecoin = pokecoin + {n} WHERE user_id = {user}"
	cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def setNPokeball(user,n):
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	crud_query = f"UPDATE user set pokeball = pokeball + {n} WHERE user_id = {user}"
	cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def setNDiamond(user,n):
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	crud_query = f"UPDATE user set diamond = diamond + {n} WHERE user_id = {user}"
	cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def setNExp(user,n):
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	crud_query = f"UPDATE user set exp_user = exp_user + {n} WHERE user_id = {user}"
	cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def setNAtt(user,hp,attk,deff,satk,sdef,speed):
	connection = sqlite3.connect('herodb.db')
	cursor = connection.cursor()

	crud_query = f"UPDATE user set power = power + {hp+attk+deff+satk+sdef+speed}, hp = hp + {hp}, atk = atk + {attk}, def = def + {deff}, satk = satk + {satk}, sdef = sdef + {sdef}, speed = speed + {speed} WHERE user_id = {user}"
	cursor.execute(crud_query)

	connection.commit()
	cursor.close()
	connection.close()

def getNEnemy(user,floor):    
	query = f"SELECT a.name,a.hp,a.atk,a.def,a.satk,a.sdef,a.speed,a.power,a.poke_id,a.img FROM poke a LEFT JOIN state b on a.poke_id = b.poke_id WHERE a.power >= {rnge[int(floor)][0]} AND a.power <= {rnge[int(floor)][1]} AND b.user_id = {user} AND b.status IS NULL;"
	temp = select(query)
	result = list()
	for x in temp:
		result.append(
				{
					"name" : x[0],
					"hp" : x[1],
					"atk" : x[2],
					"def" : x[3],
					"satk" : x[4],
					"sdef" : x[5],
					"speed" : x[6],
					"power" : x[7],
					"poke_id" : x[8],
					"img" : x[9]
				}
			)
	return result

def getAllEnemy(args):
	query = f"SELECT name,hp,atk,def,satk,sdef,speed,power,poke_id,img FROM poke;"  
	if args:
		whereMatch = ""
		for x in args:
			whereMatch += f"{x[0]}='{x[1]}' and "  
		whereMatch = whereMatch[:-5]
		query = f"SELECT name,hp,atk,def,satk,sdef,speed,power,poke_id,img FROM poke where {whereMatch} COLLATE NOCASE;"
		
	temp = select(query)
	result = list()
	for x in temp:
		result.append(
				{
					"poke_id" : x[8],
					"name" : x[0],
					"hp" : x[1],
					"atk" : x[2],
					"def" : x[3],
					"satk" : x[4],
					"sdef" : x[5],
					"speed" : x[6],
					"power" : x[7],
					"img" : x[9]
				}
			)
	return result

def defeatEnemy(user):    
    query = f"SELECT a.poke_id FROM poke a LEFT JOIN state b on a.poke_id = b.poke_id WHERE a.power >= {rnge[int(floor)][0]} AND a.power <= {rnge[int(floor)][1]} AND b.user_id = {user} AND b.status IS NOT NULL;"
    enemy = select(query2)
    return enemy

def setNFloor(user):
    connection = sqlite3.connect('herodb.db')
    cursor = connection.cursor()

    crud_query = f"Update user set floor = floor + 1 WHERE user_id = {user};"
    cursor.execute(crud_query)

    connection.commit()
    cursor.close()
    connection.close()

def insertState(user):
	connection = sqlite3.connect('herodb.db')
	crud_query = "INSERT INTO state(poke_id,user_id) VALUES(?,?);"
	cursor = connection.cursor()

	for x in range(1,1046):
		cursor.execute(crud_query,[x,user])

	connection.commit()
	cursor.close()
	connection.close()

def updateWin(user,poke):
    connection = sqlite3.connect('herodb.db')
    cursor = connection.cursor()

    crud_query = f"Update state set status = 1 WHERE poke_id = {poke} AND user_id = {user};"
    cursor.execute(crud_query)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
	result = ""
	print(result)