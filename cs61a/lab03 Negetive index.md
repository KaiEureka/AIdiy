#cs61a #python语法 

## Negetive index
Python的List和Tuple都是0-indexed的, 当越界访问时还会自动报错. 但神奇的是, Python却允许我们访问负下标, -1表示最后一个元素, -2是倒数第二个元素, -len是第一个元素, 访问比-len更小的下标时则会报错, 也就是说有效下标访问范围是`-len ~ len - 1` 神奇的规定 
for example, 
```python
>>> s = [1, 2, 3]
>>> s[0]
1
>>> s[-1]
3
>>> s[-3]
1
>>> s[-4]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
>>> s[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
>>> s = (1, 2, 3)
>>> s[-3]
1
>>> s[-4]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: tuple index out of range
```

