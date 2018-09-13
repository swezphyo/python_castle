from tornado.ioloop import IOLoop
from tornado import gen
from tornado.gen import Return
import time
 
@gen.coroutine
def coroutine_func(dura,srfn):
	print("This is Coroutine function %s" %srfn)
	yield gen.sleep(dura)
	print("Coroutine function %s is done " %srfn)
	return


def simple_func():
	print("This is the normal function")
	time.sleep(5)
	print('normal function is done')
	return

@gen.coroutine
def main():
	"""simple function works one after another. but coroutine_fun replies first and 
	then the one finished first reply the answer
	"""
	print("Start---Normal")
	[simple_func(),simple_func(),simple_func()]
	print("End----Normal")
	print("Start---Coroutine")
	yield[
		coroutine_func(6,1),
		coroutine_func(9,2),
		coroutine_func(2,3)
		]
	print("End---Coroutine")

if __name__ == "__main__":
	IOLoop().run_sync(main)