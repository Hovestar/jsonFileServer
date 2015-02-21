# So it'll have an option to add files, which is a (*str) arg
# Everything will be opened as an array of files
# Client and server operations, handles across http
# Serverside needs to access requested files in r+
import Queue,socket,thread,sys,json,traceback

#serverside
"""
- Get requests from client
 - validate credintials
 - open file / maybe create file?
 - allow reading access and or writing access
 - shallow wrapper around the normal file io!!


-BUILD
	-Listener that puts orders on a queue for the server to handle
	-Systematic sytax for sending packets

So the server needs a listener that pushes jobs onto a queue
It also needs a "doer" that takes jobs from the queue and performs actions upon it
The listener is pretty simple let me make that now.

"""
que = Queue.Queue()

currID = 0
files = {}
data = {}

def listener(conn):
	"""This will listen to a specific connections and put it's jobs on the queue"""
	done = False
	while(not done):
		try:
			data = conn.recv(1024)
			if not data: pass
			elif(data == 'q'):
				done = True
				conn.q
				#Kill connection
			else: toQueue(data,conn)
		except:
			pass

def toQueue(data,conn):
	"""
	puts the job and connection in a tuple in the Queue
	Implement later
	Takes messages from client and makes them a job for the server"""
	que.put_nowait((data,conn))

def doer():
	global currID
	"""
	Pulls item from top of queue and performs action on it then 
	sends the needed responce to the connection that requested it.
	"""
	"""
	Methods on a file:
	read size
	readline size
	write string
	close
	flush
	fileno
	isatty
	seek offset whence
		
	DIDNT IMPLEMENT:
	tell
	truncate size
	readlines
	xreadlines
	writelines []
	iter
	next
	closed
	encoding
	mode
	name
	newlines
	softspace
	"""
	while 1:
		try:
			job,conn = que.get()
			job = job.split(" ")
			ID = job[0]
			job = job[1:]
			if(ID=="###"):
				#TODO Check if it's not overwrinting anything important
				files[str(currID)]=open(*job)
				conn.send(str(currID))
				currID +=1
				""""""
			elif(job[0] == 'load'):
				files[ID].seek(0)
				tmp = files[ID].read()
				data[ID] = json.loads(tmp)
				conn.send('@')
			elif(job[0] == 'change'):
				try:
					data[ID]
				except:
					files[ID].seek(0)
					tmp = files[ID].read()
					data[ID] = json.loads(tmp)
				if(isinstance(data[ID],list) or isinstance(data[ID],str)):
					if(job[1][0] == '['):# it's giving me a splice object no step
						start,end = job[1:-1].split(':')
						data[ID][int(start):int(end)] = json.loads(' '.join(job[2:]))
					else:#just an index
						data[ID][int(job[1])] = json.loads(job[2])
				else: #I assume this is only going to be used on a dictionary or list No error handling
					data[ID][json.loads(job[1])] = json.loads(' '.join(job[2:]))
				conn.send('@')
			elif(job[0] == 'save'):
				name = files[ID].name
				files[ID].close()
				files[ID] = open(name,'w+')
				files[ID].write(json.dumps(data[ID]))
				conn.send('@')
			elif(job[0] == "read"):
				if(len(job)<=1):
					conn.send(files[ID].read())
				else:
					conn.send(files[ID].read(int(job[1])))
			elif(job[0] == "readline"):
				if(len(job==0)):
					conn.send(files[ID].readline())
				else:
					conn.send(files[ID].readline(int(job[0])))
			elif(job[0] == "write"):
				files[ID].write(' '.join(job[1:]))
				conn.send('@')
			elif(job[0] == "close"):
				files[ID].close()
				conn.send('@')
			elif(job[0] == 'flush'):
				files[ID].flush()
				conn.send('@')
			elif(job[0] == 'fileno'):
				conn.send(str(files[ID].fileno()))
			elif(job[0] == 'isatty'):
				conn.send(str(files[ID].isatty()))
			elif(job[0] == 'seek'):
				files[ID].seek(*job[1:])
				conn.send('@')
		except Exception as e:
			err = str(type(e))
			err = err[7:-2]
			conn.send(err+' \n'+traceback.format_exc())
		
		
def main():
	HOST = "localhost" #Empty for local host
	PORT = int(sys.argv[1]) #Random port specified in 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	thread.start_new(doer,())
	s.listen(1)
	while 1:
		conn,addr = s.accept()
		thread.start_new(listener,(conn,))

main()

