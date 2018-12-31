import time, sys
import requests

# Ensure jokes are printed sequentially.
i = 0


def print_joke(prompt, punchline):
	print("\n" + prompt)
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
		return read_user_input()

# Returns a list where each element is a joke.
def read_jokes(file):
	jokes = open(file, "r")
	return jokes.readlines()


# Retrieves posts from reddit.com/r/dadjokes and writes them, formatted, to a .csv file.
def get_dad_jokes():
	r = requests.get('https://www.reddit.com/r/dadjokes.json', headers = {'User-agent': 'Jokebot'})
	# Check if we're successful in requesting the data.
	if r.status_code == requests.codes.ok:
		json = r.json()["data"]["children"]
		
		# Filters jokes by content and writes them to dadjokes.csv in simplified format.
		filter_nsfw = [x for x in json if x["data"]["over_18"] == False]
		filter_nonqs = [x for x in filter_nsfw if x["data"]["title"].split(" ", 1)[0] in ("Why", "What", "How", "What's")]
		with open("dadjokes.csv", "w") as f:
			for post in filter_nonqs:
				f.write(post["data"]["title"] + "," + post["data"]["selftext"] + "\n")
	else:
		print("Failed to retrieve JSON")
		print("Status Code: " + str(r.status_code))
		sys.exit()


# Parse .csv file, output joke, receive next instruction.
def deliver_joke(file = "dadjokes.csv"):
	global i
	args = read_jokes(file)[i].split(",", 1)
	print_joke(args[0], args[1])
	i += 1
	# Exit when no more jokes to tell
	if i >= len(read_jokes(file)): 
		sys.exit()

	if read_user_input():
		deliver_joke(file)
	else:
		sys.exit()


if __name__ == "__main__":
	get_dad_jokes()
	deliver_joke(*sys.argv[1:])
