import re

string = '''
a = 10; b = 20
a= 10
10 = a
a = ?
a = 1.1
a = 1,1
a = q
a  =  1,2

'''

string2 = '''
Gegeben sind die Seitenlängen a =10, b=  20. Finde die Seitenlänge c
'''

print(string2)

new_string = re.sub(' *= *', ' = ', string2)

print(new_string)