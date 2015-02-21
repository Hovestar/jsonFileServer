Thank you for looking at my server based file io class

SETUP:
use the command: python server.py ##PORT NUM##
where ##PORT NUM### is what port you would like to accept files

On the machine that you want to access from you are free to access the 
client.py librart by starting with import client

the main concern to the user is the client.ServerFiles class that helps
create SFile objects.

Example 1: open a file in write mode and write to it

import client
s = client.ServerFiles(HOSTNAME,PORT)
f = s.open("test","w")
f.write("Hello, World!")
f.close()

Example 2: read a file
s = client.ServerFiles(HOSTNAME,PORT)
f = s.open("test","r")
print(f.read())
>>> Contents of file

Example 3:  Edit data structure
import client as io,json
s = client.ServerFiles('localhost',50007)
test = s.open("test.txt","w+")
data = {1:2}
test.write(json.dumps(data))
test.load()
test.change('value','key')
test.save()


TODO:
read will only return 1024 bytes, extend it to readwhole file
implement these file functions, utilities:
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

Add security and stop users from leaving directory and replacing files.

