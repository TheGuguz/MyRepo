"""

'''Python Arithmetic Operators'''
x + y               # sum of x and y
x - y               # difference of x and y
x * y               # product of x and y
x / y               # quotient of x and y
x ** y              # x to the power y
x // y              # floored quotient of x and y
x % y               # remainder of x / y
-x                  # x negated
+x                  # x unchanged


'''Python Assignment Operators'''
=       # x = 5       x = 5
+=      # x += 3      x = x + 3
-=      # x -= 3      x = x - 3
*=      # x *= 3      x = x * 3
/=      # x /= 3      x = x / 3
%=      # x %= 3      x = x % 3
//=     # x //= 3     x = x // 3
**=     # x **= 3     x = x ** 3
&=      # x &= 3      x = x & 3
|=      # x |= 3      x = x | 3
^=      # x ^= 3      x = x ^ 3
>>=     # x >>= 3     x = x >> 3
<<=     # x <<= 3     x = x << 3


'''Python Comparison Operators'''
# Equal:            3 == 2
# Not Equal:        3 != 2
# Greater Than:     3 > 2
# Less Than:        3 < 2
# Greater or Equal: 3 >= 2
# Less or Equal:    3 <= 2


'''Python Logical Operators'''
and     # Returns True if both statements are true                    x < 5 and  x < 10
or      # Returns True if one of the statements is true               x < 5 or x < 4
not     # Reverse the result, returns False if the result is true     not(x < 5 and x < 10)

'''Python Identity Operators'''
is          # Returns True if both variables are the same object          x is y
is not      # Returns True if both variables are not the same object      x is not y


'''Python Membership Operators'''
in          # Returns True if a sequence with the specified value is present in the object          x in y	Try it »
not in      # Returns True if a sequence with the specified value is not present in the object      x not in y


'''Python Bitwise Operators'''
x | y       # bitwise or of x and y
x ^ y       # bitwise exclusive or of x and y
x & y       # bitwise and of x and y
x << n      # x shifted left by n bits
x >> n      # x shifted right by n bits
~x          # the bits of x inverted


'''Misc'''

# Abs()
abs(x)              # absolute value or magnitude of x
# Round()
round(x[, n])       # x rounded to n digits, rounding half to even. If n is omitted, it defaults to 0.


int(x)              # x converted to integer
float(x)            # x converted to floating point
complex(re, im)     # a complex number with real part re, imaginary part im. im defaults to zero.
c.conjugate()       # conjugate of the complex number c
divmod(x, y)        # the pair (x // y, x % y)
pow(x, y)           # x to the power y


math.trunc(x)       # x truncated to Integral
math.floor(x)       # the greatest Integral <= x
math.ceil(x)        # the least Integral >= x







# Casting: string -> int


# Mutable
# list_1 = ['History', 'Math', 'Physics', 'CompSci']
# list_2 = list_1

# print(list_1)
# print(list_2)

# list_1[0] = 'Art'

# print(list_1)
# print(list_2)


# Immutable
# tuple_1 = ('History', 'Math', 'Physics', 'CompSci')
# tuple_2 = tuple_1

# print(tuple_1)
# print(tuple_2)

# tuple_1[0] = 'Art'

# print(tuple_1)
# print(tuple_2)

# Sets
# cs_courses = {'History', 'Math', 'Physics', 'CompSci'}

# print(cs_courses)


# Empty Lists
# empty_list = []
# empty_list = list()

# Empty Tuples
# empty_tuple = ()
# empty_tuple = tuple()

# Empty Sets
# empty_set = {} # This isn't right! It's a dict
# empty_set = set()




# Comparisons:
# Equal:            ==
# Not Equal:        !=
# Greater Than:     >
# Less Than:        <
# Greater or Equal: >=
# Less or Equal:    <=
# Object Identity:  is


# False Values:
#     # False
#     # None
#     # Zero of any numeric type
#     # Any empty sequence. For example, '', (), [].
#     # Any empty mapping. For example, {}.

# condition = False

# if condition:
#     print('Evaluated to True')
# else:
#     print('Evaluated to False')


# i = 0
# print("jump in the loop!")
# while i <= 5:
#     print(i)
#     i+= 1
# print("out of the loop!")


# Number of days per month. First value placeholder for indexing purposes.
# month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# def is_leap(year):
#     '''Return True for leap years, False for non-leap years.'''

#     return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# def days_in_month(year, month):
#     '''Return number of days in that month in that year.'''

#     if not 1 <= month <= 12:
#         return 'Invalid Month'

#     if month == 2 and is_leap(year):
#         return 29

#     return month_days[month]


#     # list[start:end:step]
# print (my_list[::-1])


# sample_url = 'http://coreyms.com'
# print (sample_url)

# Reverse the url
# print (sample_url[::-1])

# # Get the top level domain
# print (sample_url[-4:])

# # Print the url without the http://
# print (sample_url[7:])

# # Print the url without the http:// or the top level domain
# print (sample_url[7:-4]) 


nums = [1,2,3,4,5,6,7,8,9,10]

# I want 'n' for each 'n' in nums
my_list = []
for n in nums:
  my_list.append(n)
print (my_list)

print ([n for n in nums])

# I want 'n*n' for each 'n' in nums
# my_list = []
# for n in nums:
#   my_list.append(n*n)
# print my_list

# Using a map + lambda
# my_list = map(lambda n: n*n, nums)
# print my_list

# I want 'n' for each 'n' in nums if 'n' is even
# my_list = []
# for n in nums:
#   if n%2 == 0:
#     my_list.append(n)
# print my_list

# Using a filter + lambda
# my_list = filter(lambda n: n%2 == 0, nums)
# print my_list

# I want a (letter, num) pair for each letter in 'abcd' and each number in '0123'
# my_list = []
# for letter in 'abcd':
#   for num in range(4):
#     my_list.append((letter,num))
# print my_list

# Dictionary Comprehensions
names = ['Bruce', 'Clark', 'Peter', 'Logan', 'Wade']
heros = ['Batman', 'Superman', 'Spiderman', 'Wolverine', 'Deadpool']
# print zip(names, heros)

# I want a dict{'name': 'hero'} for each name,hero in zip(names, heros)
# my_dict = {}
# for name, hero in zip(names, heros):
#     my_dict[name] = hero
# print my_dict



# If name not equal to Peter

# Set Comprehensions
# nums = [1,1,2,1,3,4,3,4,5,5,6,7,8,7,9,9]
# my_set = set()
# for n in nums:
#     my_set.add(n)
# print my_set


# Generator Expressions
# I want to yield 'n*n' for each 'n' in nums
nums = [1,2,3,4,5,6,7,8,9,10]

# def gen_func(nums):
#     for n in nums:
#         yield n*n

# my_gen = gen_func(nums)

# for i in my_gen:
#     print i

"""