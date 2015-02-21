"""

"""
import socket,json
class ServerFiles:
	def __init__(self,HOST,PORT):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((HOST, PORT))
	def open(self,name,mode='r'):
		#open file on server and get a unique session id for it
		new = SFile(self,name,mode)
		self.sock.send("### "+name+" "+mode)
		new.ID = self.sock.recv(1024)
		return new
	def send(self,message,resp=True):
		"""Only ever called by SFile object belonging to it.
		It sends what ever message is there to it's server and returns the responce"""
		self.sock.send(message)
		tmp = self.sock.recv(1024)
		if(tmp!='@'):#rules out the '@' returns
			try:
				tmp = json.loads(tmp)
				return tmp
			except ValueError:
				print(tmp)
				raise(eval(tmp[11:tmp.index(' ')])) #NOT SECURE but it's the best I can do. json doesn't like errors
class SFile:
	"""This class is a helper for the server class and mimics what a normal file object does"""
	def __init__(self,server,name,mode):
		"""Should only ever be called from ServerFiles object"""
		self.server = server
		self.ID = None 
		self.name = name
		self.mode = mode
	"""
	Methods on a file to implement:
	read size
	readline size
	write string
	close
	flush
	fileno
	isatty
	seek offset whence
	"""
	def read(self,i=0):
		#only reads first tid-bit of data really, not the whole file. Will imporve
		return self.server.send(self.ID+" read"+(' '+str(i) if i else ''))
	def readline(self,i=0):
		return self.server.send(self.ID+" readline "+(str(i) if i else ''))
	def write(self,data):
		self.server.send(self.ID+" write "+data,False)
	def close(self):
		self.server.send(self.ID+" close",False)
	def flush(self):
		self.server.send(self.ID+" flush",False)
	def fileno(self):
		return int(self.server.send(self.ID+" fileno"))
	def isatty(self):
		return bool(self.server.send(self.ID+' isatty'))
	def seek(self, *other):
		self.server.send(self.ID+" seek "+' '.join(other),False)
	def load(self):
		self.server.send(self.ID+" load",False)
	def change(self,data,start,end=None):
		if end != None:
			ind = '['+str(start)+':'+str(end)+']'
		else:
			ind = str(start)
		self.server.send(self.ID+' change '+ind +' '+json.dumps(data))
	def save(self):
		self.server.send(self.ID+" save")
		
		
		
		
		
		
		
		
		
"""
import client as io,json
s = io.ServerFiles('localhost',50007)
test = s.open("test.txt","w+")
data = {1:2}
test.write(json.dumps(data))
test.load()
test.change(3,4)
test.save()


"""
		
		
		
		
		
