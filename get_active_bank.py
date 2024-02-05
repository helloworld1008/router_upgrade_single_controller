###################################################################################
#     This function logs into the router and fetches the active and inactive      #
#     software bank                                                               #
###################################################################################

from fetch_ssh_output import fetch_ssh_output
from get_ne_type import get_ne_type
import os, sys, paramiko, shutil, re

def get_active_bank(ch):

	op_string = ""
	
	op_string = fetch_ssh_output("show system bank",3,ch)
	
	#print (type(op_string))
	
	#print ("")
	
	#print (op_string)
	
	if "Up-Partition" in op_string:
	
		return ("up")
		
	if "Down-Partition" in op_string:
	
		return ("down")





if __name__ == '__main__':

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.171.192",username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()

	op_string = fetch_ssh_output("",2,ch)
	
	op_string = ""

	print (get_active_bank(ch))


	ch.close()
	clnt.close()













