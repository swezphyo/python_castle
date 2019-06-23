def substrings(s):

    # Declare local variable for the length of s.
    l = len(s)

    # Here I chose range over xrange for python version compatibility.
    for end in range(l, 0, -1):
        for i in range(l-end+1):
            yield s[i: i+end]

# Define palindrome.
def palindrome(s):
    return s == s[::-1]

# Main function.
def Question2(a):
    for l in substrings(a):
        if palindrome(l):
            return l

# Simple test case.
print Question2("stresseddesserts")
# stresseddesserts