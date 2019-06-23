def arrange(sentence):
	res = sentence.split('')
	sorted_res = sorted(res, key=len)
	output = " ".join(str(x) for x in sorted_res)
	return output