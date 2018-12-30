import time, sys

i = 0

def tell_joke(prompt, punchline):
	print(prompt)
	time.sleep(2)
	print(punchline)

def read_user_input():
	inst = input()
	if inst == "next":
		return True
	elif inst == "quit":
		return False
	else:
		print("I don't understand")
		read_user_input()

def read_jokes(file):
	jokes = open(file, 'r')
	return jokes.readlines()

def deliver_joke():
	global i
	args = read_jokes("jokes.csv")[i].split(",")
	tell_joke(args[0], args[1])
	i += 1
	if read_user_input():
		deliver_joke()
	sys.exit()

if __name__ == "__main__":
	deliver_joke()