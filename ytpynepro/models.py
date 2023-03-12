import  pynecone as pc


class User(pc.Model,table=True):
	name:str
	age:int