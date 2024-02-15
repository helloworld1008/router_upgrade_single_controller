#####################################################################################
#                                                                                   #
#     This function verifies that the new software image file is locally present    #
#     on the external server. If not, then the program is aborted.                  #
#                                                                                   #
#####################################################################################

from fetch_ssh_output import fetch_ssh_output
from get_ne_type import get_ne_type
import os, sys, paramiko, shutil, re

def check_local_emb_file(ch, platform):

	pattern = re.compile(platform + "_Emb_[0-9]{7}\.bin")

	file_found_flag = 0

	for t1,t2,t3 in os.walk("."):
	
		for f in t3:
		
			res = None
			
			res = pattern.match(f)
			
			if res is not None:
			
				emb_file_name = f
				
				file_found_flag = 1
				
				break

	if file_found_flag == 1:
	
		shutil.copyfile(emb_file_name,platform + "_Emb.bin")
	
		return ("Emb file found",emb_file_name)
		
	if file_found_flag == 0:
	
		return ("Emb file not found","")





if __name__ == '__main__':

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.172.8",username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()

	op_string = fetch_ssh_output("",2,ch)

	platform = get_ne_type(ch)

	print (check_local_emb_file(ch, platform))

	

	ch.close()
	clnt.close()













