import socket
import sys
import os
import zipfile
from Crypto import Random
from Crypto.Cipher import AES
import glob  
import shutil


#------------ encryption function start ---------------------------
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)
#------------ encryption function end ---------------------------


print("\n################## Starting client file #################\n")









path = "./pic/"		#path to picture folder to be send





#-----------------------------------zip started ----------------------------------------
print("zipping.....")

src = "C:/Users/slax/Desktop/com_realtime_zipadded/client_server/client/pic"  
#dst = "C:\Users\slax\Desktop\com_realtime_2\client_server\client\pic"



def zipFile(src):   
    if not (os.path.exists(src)):  # Check if folder exists 
        return False  
  
    ListOfP = glob.glob(src + '*.jpg') # Get a list of Pictures  
    for p in ListOfP:  
        newZipFN = p[:-3] + 'zip'   # Create an output zip file name from Pictures 
        if (os.path.exists(newZipFN)):  # Check if output zipfile exists, delete it  
            os.remove(newZipFN)  
            if (os.path.exists(newZipFN)):  
                return False  
   
        zipobj = zipfile.ZipFile(newZipFN,'w')  # Create zip file object 
        for infile in glob.glob( p.lower().replace(".jpg",".*")): 
            if infile.lower() != newZipFN.lower() :  
                zipobj.write(infile,os.path.basename(infile),zipfile.ZIP_DEFLATED)  # Avoid zipping the zip file!   
        zipobj.close()  
    return True  



# delete zip files in zip folder
def delete():
    fileList = os.listdir(dst)
    for fileName in fileList:
            os.remove(dst+"/"+fileName)



zipFile(src)



#-----------------------------------zip end ----------------------------------------





#--------------------------------- encryption start --------------------------------- 


#key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18' #key for encrypting and decrypting
key='aaaabbbbccccdddd'

					
fileNames = os.listdir( path )			#get all fille names in path directry

for file in fileNames:					#encrypt and delete orginal file

	if(file[-3:]!="enc"):
		
		print(file[-3:])

		completePath=path+file 				#get the file path and file name
		print("Encrypting: ",file)
		encrypt_file(completePath, key)		#encrypting file

		print("Deleting: ",file)
		os.remove(completePath)				#delete orginal file
		print('')

#--------------------------------- encryption end --------------------------------- 












#--------------------------------- sending files to server start --------------------------------- 

host = socket.gethostname()						# Get local machine name
# host="169.254.16.104"
port = 12345									# Reserve a port for your service.
print("Client host name ",host," port ",port,'\n')


fileNames = os.listdir( path )					#get all fille names in path directry

for file in fileNames:
	completePath=path+file 						#get the file path and file name	
	
	s = socket.socket()							#create socket
	s.connect((host,port))						#bind socket and port

	print("Sending ",file)

	f=open (completePath, "rb") 				#sending file to server
	l = f.read(1024)
	while (l):
	    s.send(l)
	    l = f.read(1024)
	f.close()
	s.close()

print("\nSending complete\n")

#--------------------------------- sending files to server end --------------------------------- 






#-------------------------------- deleting encrypted files start --------------------------------


print("deleting send files\n")
fileNames = os.listdir( path )			#get all fille names in path directry
for file in fileNames:					

	completePath=path+file 				#get the file path and file name
	print("Deleting: ",file)
	os.remove(completePath)				#delete orginal file


#-------------------------------- deleting encrypted files end --------------------------------





print("\n################## Ending client file #################")


