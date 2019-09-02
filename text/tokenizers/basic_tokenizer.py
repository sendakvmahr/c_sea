if __name__ == "__main__" :
	import token
	
else:
	import text.token
	token = text.token

class Basic_Tokenizer():
	def __init__(self):
		pass
	def tokenize(self, to_parse):
		remove = "[]()+=~`@#%^*()_-+=\{[]\}|\\'\'<>,"
		for c in remove:
			to_parse = to_parse.replace(c, "")
		# for everything in reomve: remove it 
		tokens = to_parse.split(" ")
		punctuation = '!$&:;?.'
		result = []
		# for everything in punctuation, if it's there, remove it, append the punctuation as a token
		for t in tokens:
			result += self.punc_split(t, punctuation)
		return [token.Token(t) for t in result]
	
	def punc_split(self, text, punctuation):
		result = []
		current = ""
		text = text.lower()
		for c in text:
			if c in punctuation:
				result.append(current)
				result.append(c)
				current = ""
			else:
				current += c
		if current != "":
			result.append(current)
		return result



if __name__ == "__main__":
	c = Basic_Tokenizer()
	tests = [
		"Here I am, looking for a thing to say.",
		"Thursday at 4AM - look for a plane.",
		"How many people are here?",
		"My battery is low and it is getting dark."
	]

	for test in tests:
		tokens = c.tokenize(test)
		t = [n.text for n in tokens]
		print(t)
	print("done")