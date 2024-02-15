#####################################################################################
#                                                                                   #
#     This function deletes the old software image file from the required (master/  #
#     slave) bank of the router                                                     # 
#                                                                                   #
#####################################################################################


from get_ne_type import get_ne_type
from fetch_ssh_output import fetch_ssh_output
from check_local_emb_file import check_local_emb_file
from get_active_bank import get_active_bank
import paramiko, sys

def delete_emb(ch,bank,platform):

	op_string = ""
	
	emb_file_path = "/sdboot/" + bank
	
	op_string = fetch_ssh_output("start shell",2,ch)
	
	#print (op_string)
	
	op_string = ""
	
	op_string = fetch_ssh_output("su",2,ch)
	
	#print (op_string)
	
	
	op_string = ""
	
	op_string = fetch_ssh_output("cd " + emb_file_path,2,ch)
	
	#print (op_string)
	
	
	op_string = ""
	
	op_string = fetch_ssh_output("pwd",2,ch)
	
	#print (op_string)
	
	if emb_file_path not in op_string:
	
		return False
		
		
	op_string = ""
	
	op_string = fetch_ssh_output("rm " + platform + "_Emb.bin*",5,ch)
	
	#print (op_string)
	
	
	op_string = ""
	
	op_string = fetch_ssh_output("ls -l " + platform + "_Emb.bin",3,ch)
	
	#print (op_string)
	
	if "No such file or directory" in op_string:
	
		op_string = ""
		op_string = fetch_ssh_output("exit",3,ch)
		
		op_string = ""
		op_string = fetch_ssh_output("exit",3,ch)
	
		return True
		
	else:
	
		op_string = ""
		op_string = fetch_ssh_output("exit",3,ch)
		
		op_string = ""
		op_string = fetch_ssh_output("exit",3,ch)
		
		return False
	
	
	
	
	
	

if __name__ == '__main__':

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.170.247",username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()

	op_string = fetch_ssh_output("",2,ch)
	
	print (op_string)
	
	if delete_emb(ch,"down","NPT1200i") is True:
	
		print ("Emb file deleted successfully")
		
	else:
	
		print ("Unable to locate or delete emb file")
	
	

	
	ch.close()
	clnt.close()
	
	
	
