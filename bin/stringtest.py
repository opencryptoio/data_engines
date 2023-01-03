s = "This is (the) Text"

import re
 
# initializing string
test_str = "geeks for geeks is best"
 
 
# Extract substrings between brackets
# Using regex
res = re.search(r'\(.*?\)', test_str)
 
# printing result
print("The element between brackets : " + str(res))
print(test_str[res.regs[0][0]+1:res.regs[0][1]-1])


