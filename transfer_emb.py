#####################################################################################
#                                                                                   #
#     This function transfers the software image file to the required (master/      #
#     slave) bank of the router                                                     # 
#                                                                                   #
#####################################################################################


from scp import SCPClient
import paramiko

def transfer_emb(sshclient,platform,bank):

	scp_obj = SCPClient(sshclient.get_transport())

	scp_obj.put(platform + "_Emb.bin",remote_path="/sdboot/" + bank)

	scp_obj.close()
	
	

if __name__ == "__main__":

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect("192.168.172.8",username="admin",password="admin1",timeout=3)
	ch = clnt.invoke_shell()

	print ("")
	print ("Transferring emb file to NE")
	transfer_emb(clnt,"NPT1100","down")
	
	print ("")
	print ("File transferred successfully")
	
	ch.close()
	clnt.close()
	
	
	
