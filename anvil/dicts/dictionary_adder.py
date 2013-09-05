f = open('./negative-words.txt', 'r');
g = open('./negative.yml', 'a');
while f:
	w = f.readline();
	if not w: break;
	else:
		g.write(str(w.strip().encode('utf-8'))+ ": [negative]\n")
