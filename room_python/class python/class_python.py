class Dog:
	def __init__(self, name, age):
		self.name = name
		self.age = age

dog1 = Dog('mike',34)
print("{} is {} now.".format(dog1.name,dog1.age))
#print(dog1)