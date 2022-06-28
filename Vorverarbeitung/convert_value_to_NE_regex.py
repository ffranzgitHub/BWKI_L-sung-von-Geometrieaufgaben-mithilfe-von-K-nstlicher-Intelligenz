import re


def convert(match_obj):
    
    string = '<'+match_obj.group(1)+'=' + match_obj.group(2)+'>'

    print('converted string: '+ string)
    return string


string1= ''' a = 10; b  =  20'''
string2= ''' a = 10; b  =  20; 10=c; 200= a'''
string3= ''' a = 10;
b = 20
c = 30  d=40
alpa = 4,5 betha =  5,5

asdflöjj.a = ?. 10,10  =  10,10
'''


new_string3 = re.sub('(\d+,\d+|\w+|\?+) *= *(\?+|\d+,\d+|\w+)', convert, string3)


print(string3)
print(new_string3)