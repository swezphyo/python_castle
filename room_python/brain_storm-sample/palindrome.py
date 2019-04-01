class Palindrome:
  @staticmethod
  def is_palindrome(word):
    #Please write your code here.
    rev = word[::-1]
    print(rev)
    if (word == rev.lower()):
      return True
    return False
    
#word = 'Deleveled'
word = input("Enter palindrone word: ")
print(Palindrome.is_palindrome(word))