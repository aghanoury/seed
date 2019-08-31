import numpy as np
"""this module solves the problems layed out in exersize 1 and 2 """
# read text file
with open('datafile.txt','r') as f:
    b = eval(f.read())

# brute force approach to finding the most frequent number
max_val = 0
most_frequent = None
for i in b:
    if b.count(i) > max_val:
        max_val = b.count(i)
        most_frequent = i

# find all of the even numbers
even_numbers = []
for i in set(b):
    if i % 2 == 0:
        even_numbers.append(i)

# print results
print("Maximum from list:", max(b))
print("Minimum from list:", min(b))
print("Index where '38' is located:", b.index(38))
print("The most frequently occuring:",most_frequent)
print("A sorted list:", np.sort(b, axis=0)) 
print("Even Numbers:", even_numbers)


# this module solves the problems layed out in exersize 2
# a crude attempt at a state machine


"""Begin excersize 2"""
print("\nBeginging assignment 2")
string = input("Enter a string to find 'abcd': ")
# in python, we can search if the string contains 'abcd' 
# using the string.find('abcd'), shown below as well

# if string.find('abcd') != -1: print("found sequence 'abcd' (python-style)") # this returns the
# else: print("did not find sequence 'abcd' (python-style)") 

# but lets also do it the proper state machine style
state = 0
for i in string:
    if i == 'a': # regardles of current state, if we find 'a' go to state 1
        state = 1
    elif i == 'b' and state == 1:
        state = 2
    elif i == 'c' and state == 2:
        state = 3
    elif i == 'd' and state == 3:
        state = 0
        print("Found sequence 'abcd' (state machine)")
        exit(0)
    else:
        state = 0
# if we get to this point, we did not find it
print('did not find sequence (state machine)')

