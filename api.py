from flask import Flask,jsonify
from flask_restful import Api, Resource
from transaction import setLogin,getNChat,getUsers,getLeader,setNChat,setRegis,setNStardust,setNPokecoin,setNPokeball,setNDiamond,setNFloor,getNEnemy,updateWin,setNExp,setNAtt

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

class getVersion(Resource):
	def get(self):
		data = {"result":"V1.1"}
		return jsonify(**data)

class getAccount(Resource):
	def get(self,user,paswd):
		accid = setLogin(user,paswd)
		if len(accid)==1:
			user = getUsers(accid[0][0])
			if len(user)==1:
				user = user[0]
				data = {
					"result" : len(accid),
					"user_id" : user[0],
					"name" : user[1],
					"poke_name" : user[2],
					"power" : user[3],
					"hp" : user[4],
					"atk" : user[5],
					"def" : user[6],
					"satk" : user[7],
					"sdef" : user[8],
					"speed" : user[9],
					"floor" : user[10],
					"exp_user" : user[11],
					"exp_poke" : user[12],
					"poke_idx" : user[13],
					"diamond" : user[14],
					"pokecoin" : user[15],
					"pokeball" : user[16],
					"stardust" : user[17],
					"account_id" : user[18]
				}
			else:
				data = {
					"result" : len(accid),
					"user_id" : 0,
					"name" : "",
					"poke_name" : "",
					"power" : 0,
					"hp" : 0,
					"atk" : 0,
					"def" : 0,
					"satk" : 0,
					"sdef" : 0,
					"speed" : 0,
					"floor" : 0,
					"exp_user" : 0,
					"exp_poke" : 0,
					"poke_idx" : 0,
					"diamond" : 0,
					"pokecoin" : 0,
					"pokeball" : 0,
					"stardust" : 0,
					"account_id" : accid[0][0]
				}
		else:
			data = {"result" : len(accid)}

		return jsonify(**data)

class getUpdate(Resource):
	def get(self,user):
		user = getUsers(user)[0]
		data = {
			"result" : 1,
			"user_id" : user[0],
			"name" : user[1],
			"poke_name" : user[2],
			"power" : user[3],
			"hp" : user[4],
			"atk" : user[5],
			"def" : user[6],
			"satk" : user[7],
			"sdef" : user[8],
			"speed" : user[9],
			"floor" : user[10],
			"exp_user" : user[11],
			"exp_poke" : user[12],
			"poke_idx" : user[13],
			"diamond" : user[14],
			"pokecoin" : user[15],
			"pokeball" : user[16],
			"stardust" : user[17],
			"account_id" : user[18],
		}
		return jsonify(**data)

class getChat(Resource):
	def get(self):
		result = getNChat()
		data = {"result":result}
		return jsonify(**data)

class setChat(Resource):
	def get(self,user,msg):
		setNChat(user,msg)
		data = {"result":1}
		return jsonify(**data)

class setStardust(Resource):
	def get(self,user,n):
		setNStardust(user,n)
		data = {"result":1}
		return jsonify(**data)

class setPokecoin(Resource):
	def get(self,user,n):
		setNPokecoin(user,n)
		data = {"result":1}
		return jsonify(**data)

class setPokeball(Resource):
	def get(self,user,n):
		setNPokeball(user,n)
		data = {"result":1}
		return jsonify(**data)

class setDiamond(Resource):
	def get(self,user,n):
		setNDiamond(user,n)
		data = {"result":1}
		return jsonify(**data)

class setExp(Resource):
	def get(self,user,n):
		setNExp(user,n)
		data = {"result":1}
		return jsonify(**data)

class setAtt(Resource):
	def get(self,user,hp,attk,deff,satk,sdef,speed):
		setNAtt(user,hp,attk,deff,satk,sdef,speed)
		data = {"result":1}
		return jsonify(**data)

class setFloor(Resource):
	def get(self,user):
		setNFloor(user)
		data = {"result":1}
		return jsonify(**data)

class getRank(Resource):
	def get(self):
		result = getLeader()
		data = {"result":result}
		return jsonify(**data)

class getEnemy(Resource):
	def get(self,user,floor):
		result = getNEnemy(user,floor)
		data = {"result":result}
		return jsonify(**data)

class setUsername(Resource):
	def get(self,user,name):
		result = setRegis(user,name)
		data = {"result":result}
		return jsonify(**data)

class setWin(Resource):
	def get(self,user,poke):
		updateWin(user,poke)
		data = {"result":1}
		return jsonify(**data)



api.add_resource(getAccount,"/poke/getAccount/<string:user>&<string:paswd>")
api.add_resource(getChat,"/poke/getChat")
api.add_resource(getVersion,"/poke/getVersion")
api.add_resource(getRank,"/poke/getRank")
api.add_resource(setUsername,"/poke/setUsername/<string:user>&<string:name>")
api.add_resource(setChat,"/poke/setChat/<string:user>&<string:msg>")
api.add_resource(getUpdate,"/poke/getUpdate/<string:user>")
api.add_resource(setStardust,"/poke/setStardust/<string:user>&<string:n>")
api.add_resource(setPokecoin,"/poke/setPokecoin/<string:user>&<string:n>")
api.add_resource(setPokeball,"/poke/setPokeball/<string:user>&<string:n>")
api.add_resource(setDiamond,"/poke/setDiamond/<string:user>&<string:n>")
api.add_resource(setExp,"/poke/setExp/<string:user>&<string:n>")
api.add_resource(setFloor,"/poke/setFloor/<string:user>")
api.add_resource(getEnemy,"/poke/getEnemy/<string:user>&<string:floor>")
api.add_resource(setWin,"/poke/setWin/<string:user>&<string:poke>")
api.add_resource(setAtt,"/poke/setAtt/<string:user>&<string:hp>&<string:attk>&<string:deff>&<string:satk>&<string:sdef>&<string:speed>")

if __name__ == '__main__':
	app.run()