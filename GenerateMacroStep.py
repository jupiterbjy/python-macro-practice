import time

import KillProcess


def TStr():
	now = time.gmtime(time.time())
	string_a = [now.tm_year, now.tm_mon, now.tm_mday]
	string_b = [now.tm_hour, now.tm_min, now.tm_sec]
	string_c = string_a + string_b
	out = '{}.{}.{} {}:{}:{}'.format(*string_c)

	# TimeString. Did this mess to reduce horizontal length!
	# Asterisk almost looks like pointer, wow.
	# Actually just unpacking string, how boring.

	return out


def FileAvailable(name, mode):

	# TODO: finish actual file generation step

	if mode == 'open':
		try:
			with open(name, 'r', encoding='utf-8') as f:
				lines = f.readlines()

		except FileNotFoundError:
			print('file not found! Try again!')
			return -1

		else:

			try:
				if '@2' in lines[1]:

					print('file Loaded:', name)
					print('\n', lines[0], lines[1], sep='')

					lines[1] = '@2 Last Access : %s\n' % TStr()

					# Rewrite entire file to change a single line!
					# How efficient!

					with open(name, 'w+', encoding='utf-8') as f2:
						for i in lines:
							f2.write("%s" % i)

					return lines

				else:
					raise IndexError

			except IndexError:
				print('File has Wrong Format!')

				KillProcess.PressKill()
    
    
	# Todo: finish this doomed code
    
	elif mode == 'generate':

		# Generate file with argument, not with no file exception
		# I find it more sensible with less mess!

		# INCOMPLETE, I have no time!!!

		print('Generating Macro Sequence!')
		print('Leaving name black will name it as macro1.txt!')

		file_name = input('File Name: ')
		if file_name == '':
			file_name = 'macro1.txt'

		# <Today's Grammar Class>
		# Created in 3 hours / Created on the 13th of July
		# Created at 2013-07-13 14:35 / Created on 2013-07-13

		with open(file_name, 'w+', encoding='utf-8') as f:
			f.write('@1 Created at  : {}\n'.format(TStr()))
			f.write('@2 Last Access : {}\n'.format(TStr()))
			f.write('# Macro Data Starts\n\n')


'''
def GenerateFile():
	
	f_lines = FileAvailable(input())
	
	while True:
		print("Entry for @", macro_s_point, sep='')
		temp = [input()]
	
	f_lines[macro_s_point] = 
'''
