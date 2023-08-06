from iniparser2 import INI_TEMP

file="""
; no section here
brief=test parse
#nothing=yes
comment_me=yes # ok

[main]
; a random comment
data=400=500
string="Hello"
something="hi hi'hello"
comment_here=again? # haha

[[section]]
; another random comment
prop=nothing
#e=haha
"""

tmp = INI_TEMP()
data = tmp.parse(file)

print(data)