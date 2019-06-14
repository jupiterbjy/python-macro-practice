import time
import sys


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


def ScriptKill(delay):
	print('Script shutdown in', delay, 'seconds.')

	time.sleep(delay)
	sys.exit()


def FileAvailable(name, mode):
	if mode == 'open':
		try:
			with open(name, 'r', encoding='utf-8') as f:
				lines = f.readlines()

		except FileNotFoundError:
			print('file not found! Try again!')
			return [-1, -1]

		else:
			try:
				# Test if Sequence txt has at least 2 lines

				tmp = lines[1]
				del tmp

			except IndexError:
				print('File contains barely nothing!')
				print('Check if you chose correct file, or remove it!')
				ScriptKill(10)

			else:
				if '@2' in lines[1]:

					print('file Loaded:', name)
					print(lines[0], lines[1], sep='')

					lines[1] = '@2 Last Access : %s\n' % TStr()

					# Rewrite entire file to change a single line!
					# How efficient!

					with open(name, 'w+', encoding='utf-8') as f2:
						for i in lines:
							f2.write("%s" % i)

					return lines

				else:
					print('No creation Date or Last access date is found')
					print('Performing basic file integrity check')

					global file_integrity
					file_integrity = False

					num_lines = sum(1 for _ in f)

					for i in range(num_lines):
						if '#' in lines[i]:
							file_integrity = True
							break

					if file_integrity:
						return lines

					else:
						NameError('File integrity damaged!')
						ScriptKill(10)

	elif mode == 'generate':

		# Generate file with argument, not with no file exception
		# I find it more sensible with less mess!

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
