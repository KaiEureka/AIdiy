#cs61a #python语法 

## tuple
tuple我之前误认为是类似array的不可变数组，才发现他不是长度不可变，他是啥都不可变，压根就是个常量数组...相当于array<const \*\*>
```python
>>> a = (1, 2, 3)
>>> a[1]
2
>>> a[1] = 2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

## append 
pyList的append方法类似于cppVector的pushback方法

## 对象赋值与身份运算符
在Python中，库对象比如list、tuple等等的赋值号的含义往往不是拷贝，不是深拷贝也不是浅拷贝，压根就不是拷贝，仅仅是创建引用，也就是说`a = [1, 2]`实际上相当于`&&a = [1, 2]`, `a = b`实际上相当于`&a = b`, 这一点要牢记, 如果要复制应该调用copy(浅拷贝)或者deepcopy(深拷贝)等方法, 创建出新对象再绑定引用到新对象上
另外, \=\=号基本上还是表示原本的意思,也就是说内容完全相等即可, 并不强求左右必须是"同一个". 而Py还真的引入了一个运算符用来表示左右是同一个对象的不同引用(或者压根就是相同引用),那就是is, 同时也引入了is not表示is和相反的意思,称之为身份运算符
```python
>>> a = [10]
>>> b = a
>>> a.append(20)
>>> b == a
True
>>> b
[10, 20]
>>> c = a.copy()
>>> a.append(30)
>>> a == c
False
>>> c
[10, 20]
>>> c.append(30)
>>> a == c
True
>>> a is c
False
```

## 缺省参数

缺省参数在Py中的实现相当之诡异, 当 Python 解释器解析函数定义时，会为函数的每个参数创建一个对应的对象来存储默认值。这些默认值对象在函数定义时就被创建并绑定到函数的参数上。换句话说, 默认的取值不是你给定的缺省值, 而是以你给定的缺省值初始化的一个程序员不可见的全局变量值,而由于这个值是有可能被修改的,所以可能会发生一些诡异的情况
For example, 
```python
>>> def f(s = []) :
...     s.append(1)
...     return len(s)
... 
>>> f()
1
>>> f()
2
>>> f()
3
>>> def g(s = [].copy()) :
...     s.append(1)
...     return len(s)
... 
>>> g()
1
>>> g()
2
>>> def h(s = []) :
...     s = s.copy()
...     s.append(1)
...     return len(s)
... 
>>> h()
1
>>> h()
1
>>> h()
1
```
