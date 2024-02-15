#####################################################################################
#                                                                                   #
#     This function upgrades the software version of the router                     #
#                                                                                   #
#####################################################################################

from get_ne_type import get_ne_type
from fetch_ssh_output import fetch_ssh_output
from check_local_emb_file import check_local_emb_file
from get_active_bank import get_active_bank
from transfer_emb import transfer_emb
from delete_emb import delete_emb
from verify_system_bank import verify_system_bank
from pre_upgrade_test import pre_upgrade_test
import paramiko, sys, re

def router_upgrade(IP,username,password):

	########## LOGIN TO NE ##########

	clnt = paramiko.client.SSHClient()
	clnt.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

	clnt.connect(IP,username=username,password=password,timeout=3)

	ch = clnt.invoke_shell()


	########## GET NE PROMPT ##########
	
	op_string = ""
	op_string = fetch_ssh_output("",2,ch)
	
	#print ("")
	#print (op_string)
	

	for line in op_string.split("\n"):
	
		if "admin" in line:
		
			target_line = line
			
			break
	
	res = re.search(r"^.*?(admin@.*?>).*$",target_line)
	
	if res is not None:
	
		prompt = res.group(1)
		
	else:
	
		print ("")
		print ("{}: Unable to get NE prompt".format(IP))
		print ("{}: Exiting program".format(IP))
		
		sys.exit(0)
		
		
	
	print ("")
	print ("{}: Login successful".format(IP))
	

	########## FETCH PLATFORM TYPE ##########

	platform = get_ne_type(ch)

	print ("")
	print ("{}: Platform {} detected".format(IP,platform))

		
	########## CHECK FOR EMB FILE LOCALLY ##########
	
	result_check_local_emb_file = check_local_emb_file(ch, platform)
	
	if result_check_local_emb_file[0] == "Emb file found":
	
		print ("")
		print ("{}: Emb file found => {}".format(IP,result_check_local_emb_file[1]))
		
		new_emb_file = result_check_local_emb_file[1]
		
	
	if result_check_local_emb_file[0] == "Emb file not found":
	
		print ("")
		print ("{}: Emb file not found".format(IP))
		
		print ("")
		print ("{}: Exiting program".format(IP))

		ch.close()
		clnt.close()
		
		print ("")
		print ("{}: Connection closed".format(IP))
		
		sys.exit(0)


	########## GET ACTIVE BANK ##########

	if get_active_bank(ch) == "up":
	
		print ("")
		print ("{}: Active bank is UP".format(IP))
		
		inactive_bank = "down"
		
	if get_active_bank(ch) == "down":
	
		print ("")
		print ("{}: Active bank is DOWN".format(IP))
		
		inactive_bank = "up"
		
		
	########## DELETE EMB FROM INACTIVE BANK ##########		
		
	if delete_emb(ch,inactive_bank,platform) is True:
	
		print ("")
		print ("{}: Emb file deleted from inactive bank".format(IP))
		
	else:
		print ("")
		print ("{}: Unable to locate or delete emb file".format(IP))
		
		ch.close()
		clnt.close()
		
		print ("")
		print ("{}: Connection closed".format(IP))
		
		print ("")
		print ("{}: Exiting program".format(IP))
		
		sys.exit(0)

	
	########## TRANSFER EMB TO INACTIVE BANK ##########

	transfer_emb(clnt,platform,inactive_bank)
		
	print ("")
	print ("{}: Emb file transferred to inactive bank".format(IP))
	
	
	
	
	########## VERIFY EMB IN SLAVE BANK ##########

	verification_result = verify_system_bank(ch,"slave",new_emb_file)
	
	if verification_result[0] is True:
	
		new_emb_version = verification_result[2]
		
		print ("")
		print ("{}: {} {}".format(IP,verification_result[1],verification_result[2]))
		
	else:
	
		print ("")
		print ("{}: {}".format(IP,verification_result[1]))
		
		sys.exit(0)
		
		
	########## PERFORM PRE-UPGRADE TEST ##########	
				
	pre_upgr_test_result = pre_upgrade_test(ch,prompt,new_emb_version)
	
	if pre_upgr_test_result[0] is True:
	
		print ("")
		print ("{}: {}".format(IP,pre_upgr_test_result[1]))
		
		print ("")
		print ("{}: Activation given".format(IP))
		
	else:
	
		print ("{}: {}".format(IP,pre_upgr_test_result[1]))
		
		ch.close()
		clnt.close()
		
		print ("{}: Connection closed".format(IP))
		
		sys.exit(0)
		
	
	ch.close()
	clnt.close()
	
	print ("")
	print ("{}: Connection closed".format(IP))
	


if __name__ == '__main__':

	downgrade_ne("192.168.172.8","admin","admin1")

	
