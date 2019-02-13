def add_op(op, first, second):
	res = first + second
	print(res)

def sub_op(op, first, second):
	res = first - second
	print(res)

def div_op(op, first, second):
	res = first / second
	print(res)

def mod_op(op, first, second):
	res = first % second
	print(res)

def mult_op(op, first, second):
	res = first * second
	print(res)

def main():
	print("Welcome from my calculator")
	a = int(input("Enter first number:"))
	b = int(input("Enter second number:"))
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