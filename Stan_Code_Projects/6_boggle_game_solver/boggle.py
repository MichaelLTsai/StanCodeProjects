"""
File: boggle.py
Name: 蔡霖
----------------------------------------

"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


def main():
	"""
	"""
	while True:
		row_1 = input("1 row of letters: ").lower()  # ["f", "y", "c", "l"]
		if len(row_1) > 7:
			print("Illegal Input")
			break
		row_1 = row_1.split()
		row_2 = input("2 row of letters: ").lower()  # ["i", "o", "m", "g"]
		if len(row_2) > 7:
			print("Illegal Input")
			break
		row_2 = row_2.split()
		row_3 = input("3 row of letters: ").lower()  # ["o", "r", "i", "l"]
		if len(row_3) > 7:
			print("Illegal Input")
			break
		row_3 = row_3.split()
		row_4 = input("4 row of letters: ").lower()  # ["h", "j", "h", "u"]
		if len(row_4) > 7:
			print("Illegal Input")
			break
		row_4 = row_4.split()
		start = time.time()
		row_ttl = [row_1, row_2, row_3, row_4]
		dict_list = read_dictionary(row_1 + row_2 + row_3 + row_4)
		counter = []
		for row in range(0, 4):
			for ch in range(0, 4):
				find_anagrams(row_ttl, dict_list, [], "", row, ch, counter)
		print(f"There are {len(counter)} words in total")
		end = time.time()
		print('----------------------------------')
		print(f'The speed of your boggle algorithm: {end - start} seconds.')
		break


def read_dictionary(ttl):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	lst = []
	with open(FILE, "r") as f:
		for line in f:
			if len(line.strip()) < 4:
				continue
			for i in range(len(line.strip())):
				if line.strip()[i] not in ttl:
					break
				elif i == len(line.strip())-1:
					lst.append(line.strip())
	return lst


def has_prefix(sub_s, dict_list):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:param dict_list: (list) A list that contain a sorted dictionary
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for word in dict_list:
		if word.startswith(sub_s):
			return True
	return False


def find_anagrams(row_ttl, dict_list, used_list, sub_s, row_num, ch_num, counter):
	"""
	:param row_ttl: (list) A list contain 4 items which each item represent a row.
	:param dict_list: (list) A list that contain a sorted dictionary
	:param used_list: (list) A list the record the used (row_num, ch_num)
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:param row_num: (int) Current row number
	:param ch_num: (int) Current ch number in each row
	:param counter (list) A list contain all the answer.
	"""
	# Base Case
	if row_num < 0 or row_num > 3 or ch_num < 0 or ch_num > 3:
		pass
	elif (row_num, ch_num) in used_list:
		pass
	else:
		# Chose
		sub_s += row_ttl[row_num][ch_num]
		used_list.append((row_num, ch_num))
		if has_prefix(sub_s, dict_list):
			# Explore
			for i in range(-1, 2):
				for j in range(-1, 2):
					if i == 0 and j == 0:
						pass
					else:
						find_anagrams(row_ttl, dict_list, used_list, sub_s, row_num + i, ch_num + j, counter)
		if sub_s in dict_list and sub_s not in counter:
			counter.append(sub_s)
			print("Found:", sub_s)
		# Un-Chose
		sub_s = sub_s[:-1]
		used_list.pop()
		# why not: used_list = used_list[:-1]


if __name__ == '__main__':
	main()
