import sys

def add_op(op, first, second):
	''' addition function'''
	res = first + second
	print(res)

def sub_op(op, first, second):
	'''Subtraction function'''
	res = first - second
	print(res)

def div_op(op, first, second):
	'''Divide function'''
	res = first / second
	print(res)

def mod_op(op, first, second):
	'''Modular function'''
	res = first % second
	print(res)

def mult_op(op, first, second):
	'''Multiplication function'''
	res = first * second
	print(res)

def main():
	print("Welcome from my calculator")
	try:
		a = int(input("Enter first number:"))
	except ValueError as e:
		print("Invalid! Enter integer value")
		sys.exit(1)

	try:
		b = int(input("Enter second number:"))
	except ValueError as e:
		print("Invalid! Enter integer value")
		sys.exit(1)

	raw_in = input("Choose operations that you want: (+,-,*,/,%)! ")
	if raw_in == '+':
		add_op(raw_in,a,b)
	elif raw_in == '-':
		sub_op(raw_in,a,b)
	elif raw_in == '/':
		div_op(raw_in,a,b)
	elif raw_in == '%':
		mod_op(raw_in,a,b)
	elif raw_in == '*':
		mult_op(raw_in,a,b)
	else:
		print("Please enter valid operations:")
	print("Thank You!")

if __name__ == '__main__':
    main()