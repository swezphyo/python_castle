"""
program for reversing numbers in binary. For instance, the binary representation of 13 is 1101, and reversing it gives 1011, which corresponds to number 11.
"""
def main():
	_input = int(input("Enter an integer between 1 and 1000000000 "))

	binary = bin(_input)
	#print(binary)
	reversed_bin = binary[::-1]
	#print(reversed_bin)

	#decimal number from reversed binary number
	decimal = (int(reversed_bin[:-2],2))
	#print(decimal)


if __name__ == '__main__':
	main()
	sys.exit(0)

