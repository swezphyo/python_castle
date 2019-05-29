"""Regression to check the NRC format in myanmar
"""
import re
#REF: https://stackoverflow.com/questions/7629643/how-do-i-validate-the-format-of-a-mac-address
inpstr = input("Enter a string to validate! ")
if re.match("[0-9]{2}[/]([A-Z][a-z]){3}[(][A-Z][)][0-9]{6}$", inpstr):
    print("true")
else:
    print("false")
