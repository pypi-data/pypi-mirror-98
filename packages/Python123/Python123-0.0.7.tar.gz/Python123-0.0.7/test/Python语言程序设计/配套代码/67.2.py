"""
>>> zd={1:2,3:4,5:6}
>>> zd.popitem()
(5, 6)
>>> zd.popitem()
(3, 4)
>>> zd.popitem()
(1, 2)
>>> zd.popitem()
Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    zd.popitem()
KeyError: 'popitem(): dictionary is empty'
>>>
"""
