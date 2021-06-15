from bs4 import BeautifulSoup as bs
import urllib3,csv
import sqlite3

def insertpoke():
	http = urllib3.PoolManager()
	url = 'https://pokemondb.net/pokedex/all'
	response = http.request('GET', url).data.decode('utf-8')

	connection = sqlite3.connect('herodb.db')
	crud_query = "INSERT INTO poke (name,power,hp,atk,def,satk,sdef,speed,img) VALUES(?,?,?,?,?,?,?,?,?);"
	cursor = connection.cursor()

	soup = bs(response,features="html.parser")
	imgg = soup.find_all("span","infocard-cell-img")
	tr = soup.find("table", class_ ="data-table").find("tbody").find_all("tr")
	data=[]
	z = 0
	for x in tr:
		td = x.find_all("td")
		temp=[]
		for y in range(len(td)):
			temp.append(td[y].get_text().replace("\n",""))
		temp.append(imgg[z].span["data-src"])
		data.append(temp)
		z+=1

	for x in data:
		del x[0]
		del x[1]
		cursor.execute(crud_query,x)

	connection.commit()
	cursor.close()
	connection.close()

def insertstate(idpoke):
	connection = sqlite3.connect('herodb.db')
	crud_query = "INSERT INTO state(poke_id,user_id) VALUES(?,?);"
	cursor = connection.cursor()

	for x in range(1,1046):
		cursor.execute(crud_query,[x,idpoke])

	connection.commit()
	cursor.close()
	connection.close()
if __name__ == '__main__':
	insertstate(2)
	print("Select the function fisrt")