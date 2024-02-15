#####################################################################################
#                                                                                   #
#     This function performs the pre-upgrade test in the router. If the test        #
#     succeeds, then the actual software upgrade is performed. Else, the upgrade    # 
#     process is aborted                                                            #
#                                                                                   #
#####################################################################################

from fetch_ssh_output import fetch_ssh_output
import paramiko, sys, time

def pre_upgrade_test(ch,prompt,new_emb_version):

	op_string = b''
	
	ch.send("request system software launch pre-upgrade-test version " + new_emb_version + "\n")
	
	time.sleep(3)
	
	while ch.recv_ready():

		op_string = op_string + ch.recv(1000)
		
	#print (op_string)
	
	while prompt not in str(op_string):
	
		time.sleep(10)
		
		op_string = b''
		
		while ch.recv_ready():

			op_string = op_string + ch.recv(1000)
			
	
	if "Pre-upgrade-test succeed" in str(op_string):
	
		time.sleep(3)
		
		op_string = b''
		ch.send("request system software launch version " + new_emb_version + "\n")
		time.sleep(3)
		
		while ch.recv_ready():

			op_string = op_string + ch.recv(1000)
			
		return (True,"pre-upgrade test succeeded")
		
	else:
	
		print ("")
		return (False,"pre-upgrade test failed")



if __name__ == '__main__':

	print ("")
	
	IP = "192.168.172.8"
	prompt = "admin@NE_B>"
	new_emb_version = "V9.2.00086"
	op_string = b''
	
	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect(IP,username="admin",password="admin1",timeout=3)

	ch = clnt.invoke_shell()
	
	time.sleep(5)
	
	while ch.recv_ready():

		op_string = op_string + ch.recv(1000)
		
	#time.sleep(3)
	
	print (op_string)
	
	print ("")
	print ("{}: Login successful".format(IP))
	
	pre_upgrade_test(ch,prompt,new_emb_version)
	
	ch.close()
	clnt.close()
