#####################################################################################
#                                                                                   #
#     This function sends the command to the router, waits for a specified time     # 
#     and returns the output in a string format                                     #
#                                                                                   #
#####################################################################################


import time
from output_cleaner import output_cleaner

def fetch_ssh_output(command,wait_time,ch):

	op_string = b''

	if command != "":

		ch.send(command + "\n")
	
	time.sleep(wait_time)

	while ch.recv_ready():

		op_string = op_string + ch.recv(1000)

	op_string = output_cleaner(op_string)

	return op_string


if __name__ == "__main__":

	pass
