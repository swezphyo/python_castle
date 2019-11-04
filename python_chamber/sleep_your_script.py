import time
#Ref: https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/ 
def sleeper():
    while True:
        # Get user input
        num = input('How long to wait: ')
 
        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            print('Please enter in a number.\n')
            continue
 
        # Run our time.sleep() command,
        # and show the before and after time
        print('Before: %s' % time.ctime())
        time.sleep(num)
        print('After: %s\n' % time.ctime())
 
 
def main():    
    try:
        sleeper()
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()

if __name__ == '__main__':
    main()