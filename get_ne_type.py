###################################################################################
#     This function logs into the router and fetches the router platform type     #
###################################################################################

from fetch_ssh_output import fetch_ssh_output
import paramiko
import re

def get_ne_type(ch):

	op_string = ""
	op_string = fetch_ssh_output("show version",2,ch)


	p = re.search(r"Ne Type            : (NPT-1[0-9][0-9][0-9]i{,1}B{,1}).*", op_string)

	if p is not None:

		platform = p.group(1)
		platform = platform.replace("-","",1)
		platform = platform.replace("B","",1)
		
		return (platform)

	else:

		return None


if __name__ == '__main__':

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.170.247",username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()

	op_string = fetch_ssh_output("",2,ch)

	
	print (get_ne_type(ch))

	print ("")

	ch.close()
	clnt.close()
