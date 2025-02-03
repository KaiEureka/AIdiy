#cs61a #python语法 

## iterator
`iter(container)`可以返回指向输入对象的最早元素的迭代器, next(it)可以返回迭代器当前所指向元素,并让迭代器自动指向下一个元素, 访问最后一个元素的下一个元素将会导致抛出异常
对的, 操作非常简单, 甚至没法不移动指针得单独访问迭代器所指向的元素,  Py不重视这个机制,所以设计的很简陋,也确实没必要使用

Py中的迭代器机制很奇怪, 更像是赋值了一个新对象(实际上不是,接下来解释),然后有一个单项指针指向这个新对象, 可以通过这个单向指针实现访问, 也可以通过`for r in it`的方式来访问it所指向的元素到末尾元素之间的每个值,并把it移动到末尾元素的下一个位置,也就是失效处, 迭代器也可以转化为list或者tuple等容器,也就是把迭代器所指向对象到末尾元素的每个元素组成的新容器,当然也会同时让迭代器失效,换句话说迭代器就是只能访问一次,但你当然可以通过直接把访问结果存下来来实现多次访问. 实际上for能这么操作正是因为迭代器可以如此转化为list,for这里并不是语法糖,充其量算是一个自动转换

正是因为迭代器可以转化为list所以看上去像是复制了一遍,也就是说迭代器本身像是容器,但显然迭代器实际上不是容器,他真的只是指针,访问的完全是原数组的内容,创建为迭代器后更新原数组内容迭代器访问到的当然也是新的值,能够直接转为容器仅仅是因为每个库容器的构造函数都是添加了如此操作的指令而已,通过遍历来创建,并不是真的拷贝.

For example, 
```python
>>> x = [1, 2, 3]
>>> it = iter(x)
>>> next(it)
1
>>> list(it)
[2, 3]
>>> for r in it :
...     print(r)
... 
>>> 
>>> it
<list_iterator object at 0x102796eb0>
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>> it = iter(x)
>>> for r in it :
...     print(r)
... 
1
2
3
>>> it = iter(x)
>>> b = []
>>> b += it
>>> b
[1, 2, 3]
```

## map and yield
Py中有一个长得很唬人的东西, 就是这个map, 看上去像是一种容器, 但Py中已经有了Dict, 因此没把Map定义为容器, map实际上仅仅是一个函数而已,接受两个参数,前一个是函数,后一个是容器, map创建一个新容器,该容器的元素是输入容器每个元素经过输入函数的变化后的结果, 返回新容器的迭代器,我猜内部实现如下
```python
def map(func, container) :
	return iter([func(r) for r in container])
```
但实际并非如此, 实际上的实现利用了yield关键字,这是一个cpp中知道cpp20才引入的概念,因为不合CPP设计理念,更适合Py等解释性动态语言的设计理念,yield可以实现懒求值,也就是他返回的迭代器只有访问到的值会被计算出来,没访问到的值不会被存储也不会被计算.

一个用到了yield的函数属于高阶函数,该高阶函数返回一个迭代器,迭代器指向的是一个函数,该函数的返回值是高阶函数中的yield值,函数的下一次执行会从上次返回的yield句之后继续,获取返回值的办法是把访问该函数也就是把函数迭代器放进next中.这个特殊的迭代器会被称为生成器
For example, 
```python
>>> def f(x):
...     yield x
...     yield x - 1
...     yield x - 2
... 
>>> t = f(3)
>>> t
<generator object f at 0x10277d890>
>>> next(t)
3
>>> next(t)
2
>>> next(t)
1
>>> next(t)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

所以map的实现实际上是
```python
def map(func, container) :
	for r in container :
		yield func(r)
```

有一个语法糖(Py是这样的,比奶龙还糖)
```python
yield from a
#相当于
for x in a:
	yield x
```
yield 的高级用法, 务必看懂
```python
def partitions(n, m) :
	'''
	>>> for p in partitions(6, 4): print(p)
	2 + 4
	1 + 1 + 4
	3 + 3
	1 + 2 + 3
	1 + 1 + 1 + 3
	2 + 2 + 2
	1 + 1 + 2 + 2
	1 + 1 + 1 + 1 + 2
	1 + 1 + 1 + 1 + 1 + 1
	'''
	if n > 0 and m > 0:
		if n == m :
			yield str(m)
		for p in partitions(n - m, m) :
			yield p + ' + ' + str(m)
		yield from partitions(n, m - 1)

def UnLazyPartitions(n, m):
	'''
	>>> for p in UnLazyPartitions(6, 4): print(p)
	2 + 4
	1 + 1 + 4
	3 + 3
	1 + 2 + 3
	1 + 1 + 1 + 3
	2 + 2 + 2
	1 + 1 + 2 + 2
	1 + 1 + 1 + 1 + 2
	1 + 1 + 1 + 1 + 1 + 1
	'''
	if n < 0 or m == 0 :
		return []
	else :
		exact_match = []
		if n == m :
			exact_match = [str(m)]
		with_m = [p + ' + ' + str(m) for p in UnLazyPartitions(n - m, m)]
		without_m = UnLazyPartitions(n, m - 1)  
		return exact_match + with_m + without_m


```

## filter(func, iterable)
返回能使func返回True的可迭代对象iterable(也就是容器)的元素构成的迭代对象,说白了就是用func对iterable进行一个筛选, 但这个筛选是不会改变原iterable的,只会返回一个满足条件的元素构成的新iterable, 这个iterable会统一为filter格式,可以被iterable构造函数转化为任何其他形式
For example, 
```python
>>> f = lambda y : y > 20
>>> a = [10, 20, 40, 50]
>>> filter(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: filter expected 2 arguments, got 1
>>> filter(f, a)
<filter object at 0x102796340>
>>> b = filter(f, a)
>>> b
<filter object at 0x1027962e0>
>>> a
[10, 20, 40, 50]
>>> list(b)
[40, 50]
```

## IO
说了这么多,竟然忘了学Py的IO了,实际上Py的IO极其简单,输出print类似于C的printf,而输入则是需要input()函数,input会读入一整行,把内容存储到一个字符串中,需要读入后自行转换
For example, 
```python
name = "Alice"
age = 25
print("我的名字是 %s，我今年 %d 岁。" % (name, age))
```
For example, 
```python
>>> input()
213 132
'213 132'
>>> s = input()
1
>>> int(s)
1
>>> int('213')
213
>>> int('342 ')
342
>>> int('342 324 2')
>>> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: '342 324 2'
```
Py中的print还支持更方便的操作
For example, 
```python
name = "Bob"
age = 30
print("我的名字是 {}，我今年 {} 岁。".format(name, age))

# 以及f-string更方便,开头一个f,中间{}直接插值,便可自动评估

name = "Charlie"
age = 35
print(f"我的名字是 {name}，我今年 {age} 岁。")
```

显然输入整数只需要`n = int(input())`即可, 输入内容无法转化为整数时会抛出异常,可以通过以下方法来确保鲁棒性
For example, 
```python
while True:
    try:
        num = int(input("请输入一个整数: "))
        break
    except ValueError:
        print("输入无效，请输入一个整数。")
```
总之似乎现在的水平已经足以写算法题了,打篮球杯时要加油呀