###################################################################################
#     This specific router platform returns a lot of special characters as part   #
#     of the binary string returned by the paramiko function.                     #
#                                                                                 #
#     This function removes the special characters which are not needed from the  # 
#     output and returns a cleaner output.                                        #
#                                                                                 #
###################################################################################

def output_cleaner(byte_string):

	byte_string_ascii_value_list = list(byte_string)

	target_ascii_value_list = [13,10,27,91,75]

	new_byte_string_ascii_value_list = []

	i = 0
	j = 0

	while i < len(byte_string_ascii_value_list):

		if byte_string_ascii_value_list[i:i+5] == target_ascii_value_list and j == 80:

			i = i + 5
			j = 0
			continue

		if byte_string_ascii_value_list[i:i+5] == target_ascii_value_list and j != 80:

			new_byte_string_ascii_value_list = new_byte_string_ascii_value_list + byte_string_ascii_value_list[i:i+5]
			i = i + 5
			j = 0
			continue

		new_byte_string_ascii_value_list.append(byte_string_ascii_value_list[i])

		i = i + 1
		j = j + 1   

	old_byte_string = ''
	new_byte_string = ''

	i = 0

	while i < len(new_byte_string_ascii_value_list):

		if new_byte_string_ascii_value_list[i:i+5] == target_ascii_value_list:

			del new_byte_string_ascii_value_list[i+2:i+5]

			i = 0

		else:

			i = i + 1


	for b in new_byte_string_ascii_value_list:

		new_byte_string = new_byte_string + chr(b)

	return new_byte_string


if __name__ == "__main__":

	pass
