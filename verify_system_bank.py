###################################################################################
#     This function logs into the router and verifies that the software is        #
#     properly loaded in the master/slave bank                                    #
###################################################################################

from fetch_ssh_output import fetch_ssh_output
from get_ne_type import get_ne_type
import os, sys, paramiko, shutil, re, time

def verify_system_bank(ch,partition,new_emb_file):

	op_string = ""
	
	op_string = fetch_ssh_output("show system bank | grep " + partition,3,ch)
	
	target_line = ""
	
	for line in op_string.split("\n"):
	
		if "software version" in line:
		
			target_line = line
			
			break
			
	
	if partition == "slave":
	
		search_res = re.search(r"^.*?The slave  software version is : (V[7-9]\.[0-9]\.[0-9]{5}).*$",target_line)
		
		if search_res == None:
		
			return (False,"The slave partition is blank")
			
		
		emb_version_in_ne = search_res[1]
		
		if emb_version_in_ne.replace("V","").replace(".","") == new_emb_file.split("_")[2].split(".")[0]:
		
			return (True,"New emb loaded successfully in slave bank",emb_version_in_ne)
			
		else:
		
			return (False,"New emb not loaded in slave bank","")
		
		
	if partition == "master":
	
		search_res = re.search(r"^.*?The master software version is : (V[7-9]\.[0-9]\.[0-9]{5}).*$",target_line)
		
		if search_res == None:
		
			return (False,"The master partition is blank")
		
		
		emb_version_in_ne = search_res[1]
		
		if emb_version_in_ne.replace("V","").replace(".","") == new_emb_file.split("_")[2].split(".")[0]:
		
			return (True,"New emb loaded successfully in master bank")
			
		else:
		
			return (False,"New emb not loaded in master bank")
			
	
if __name__ == '__main__':

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.171.159",username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()

	op_string = fetch_ssh_output("",2,ch)
	
	print ("")
	print (op_string)
	
	new_emb_file = "NPT1100_Emb_9020380.bin"
	
	res = verify_system_bank(ch,"master",new_emb_file)
	
	if res[0] == True:
	
		print ("192.168.171.159: {}".format(res[1]))
		
	else:
	
		print ("192.168.171.159: {}".format(res[1]))
		print ("Exiting")
	
	ch.close()
	clnt.close()
	
	print ("")
	print ("connection closed")