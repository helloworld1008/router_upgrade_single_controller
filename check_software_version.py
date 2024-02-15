#####################################################################################
#                                                                                   #
#     This function verifies that the new software image file is                    #
#     properly loaded in the master/slave bank of the MCP.                          #
#                                                                                   #
#####################################################################################


from fetch_ssh_output import fetch_ssh_output
import paramiko
import re


def check_software_version(ch):

	op_string = fetch_ssh_output("show system bank",3,ch)

	m = re.search(r"The master software version is : V[8-9]\.[0-9]\.[0-9][0-9][0-9][0-9][0-9].*", op_string)
	
	if m is not None:

		print ("The master software version is OK")

	else:

		print ("The master software version is not OK")


	s = re.search(r"The slave  software version is : V[8-9]\.[0-9]\.[0-9][0-9][0-9][0-9][0-9].*", op_string)	

	if s is not None:

		print ("The slave software version is OK")

	else:

		print ("The slave software version is not OK")

	if m is None or s is None:

		return False

	else:

		return True


if __name__ == '__main__':

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.171.12",username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()

	op_string = fetch_ssh_output("",2,ch)

	#op_string = fetch_ssh_output("show system bank",3,ch)

	#print (op_string)

	print (check_software_version(ch))

	print ("")

	ch.close()
	clnt.close()








