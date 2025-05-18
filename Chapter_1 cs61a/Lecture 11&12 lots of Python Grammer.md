#cs61a #python语法 #GreatArticle

python果然够狂野, list的方法竟然不是函数, 而是一个直接被强行定义出来的运算符.... 这语法糖的浓度爆表了好吧
## in, not in
引入了 in 和 not in 这两个运算符(第一个还能忍, 第二个真的没法不吐槽)
值得注意的是, 这两个运算符优先度相当之高, 甚至比逻辑运算符not还高
```python
>>> digits = [1, 8 ,2, 8]
>>> 1 in digits
True
>>> '1' not in digits
True
>>> not '1' in digits
True
>>> not ('1' in digits)
True
>>> False in digits
False
>>> not '1' not in digits
False
>>> [1, 8] in digits
False
```

## range
range可以构造list, `range(n)` 返回`[0, 1, ...., n -1]`, `range(l, r)` 返回`[l, l + 1, ..., r - 1]`, `range[l, r, step]`返回`[l, l + step, l + 2 * step, ... , the max factor less than r]`, 但值得注意的是, range并不是真的返回了一个list, range就是range, 我所说的返回其实是值这个range相当于什么list,  但range本身就是range, 不是什么别的, range只有被显式转换或者在需要list的位置处被隐式转换后才是list, 这说起来可能有些抽象,但确实如此, 看下面这个例子吧
```python
>>> range(1, 3)
range(1, 3)
>>> list(range(1, 3))
[1, 2]
>>> range(1, -2)
range(1, -2)
>>> list(range(1, -2))
[]
```
interesting, 这说明他妈的range并不是一个函数, 而也是一个特别被定义出来的语法, 本质上也是个语法糖, 所有被特别定义出来的东西几乎都是实现一些没有他们也能实现爱你的功能, 因此都可以称之为语法糖, python真的是含糖量超标了啊哈哈(更新:后来发现实际上使用repr和str来实现的,并不是语法糖,而是Python开发了这么一个很好的造糖机器:自定义repr()和str(),这里要夸夸Python)

## 列表推导 List Comprehensions
```python
newlist = [f(x) for x in oldlist]
# 相当于数学上的newS = {f(x) | x ∈ oldS and f(x) exist}
newlist = [f(x) for x in oldlist if cond(x)]
# 相当于数学上的newS = {f(x) | x ∈ oldS and cond(x) is True and f(x) exist}
# for is |, in is ∈, and cond(x), the bool-expression behind if, is the fit-condition 
# Crazy Syntax Suger
# CRAZY PYTHON
# 注意到, 这个列表推导功能是自带边界检查的, 就算没有写, 但是如果f(x)不存在那也不会报错, 只是这个f(x)不会进入newlist而已(废话不存在的东西怎么进入)
```
for example, 
```python
>>> odds = [1, 3, 5, 7, 9]
>>> [x*x for x in odds]
[1, 9, 25, 49, 81]
>>> [x*x for x in odds if 25 % x == 0]
[1, 25]
```
而且

以为这就结束了? no no, python 的疯狂不止如此, 下面这种特殊的List Comprehension
```python
[oldlist[i] for i in range(l, r, step)]
```
可以写作
```python
oldlist[l : r : step]
```
这称之为列表切片LIst Slicing. 
并且, 列表切片的任何一部分都可以被省略掉, l被省略掉默认为0, r被省略掉默认为len(oldlist),  step被省略掉会默认为1, 同时step被省略掉的时候还可以同时略去最后一个:不写(当然也可以不略去)
因此,列表切片还可以有如下形式
```python
oldlist[l : r] #[oldlist[i] for i in range(l, r)]
oldlist[:r] #[oldlist[i] for i in range(0, r)]
oldlist[l:] #[oldlist[i] for i in range(l, len(oldlist))]
oldlist[:]  
oldlist[l : : step]
oldlist[ : r : step]
oldlist[ : : step]
oldlist[ : : ]#[oldlist[i] for i in range(0, len(oldlist), 1)] 
```
注意与matlab的区别, lr是左闭右开的边界, step写在第三位而不是中间

## python中"类型"这个概念本身的辨析

无需多言, python中的容器几乎总是类似于matlab元胞数组那般荤素不忌,  容器中的元素可以是任何东西这不奇怪, cpp中的模版编程可以实现相同的效果, 只不过麻烦些, 但可以同时是任何不同东西就很神奇了, 这显然是cpp中无法实现的, python似乎压根没有容器类型这个概念, 一切容器本质上似乎都是同一个表示类型的母类派生出来的子类, 因此自然可以实现, 诶你别说, cpp如果也这么搞, 用多态还真的实现这个效果, 所以python其实就是把这个功能官方做了出来并且把多态的细节隐藏起来了?这么考但也不错. 数据类型顶多分成int float两类, 其他所有类型似乎都是class而已, 并不是什么写死的类型, 可能python有且之后两个类型int和float, 这是因为cpu中压根也就有且只有这两种类型, 没想到啊竟然还能联系到计组的知识
总而言之, python可以任意乱搞
```python
[1, [1,2]] #legal
(1, [1, (1, 1, (1, 1))]) #also legal
```

## sum
sum(list, initialValue = 0)可以直接返回list中元素的总和, initialValue是初始值, sum的默认初始值是0, 当把不能相加的东西加起来时候python还是会报错的,因此有如下交互
```python
>>> sum([[2, 3], [4]])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'list'
>>> sum([[2, 3], [4]], [])
[2, 3, 4]
>>> sum([["123", "23"],["23"]], ["56"])
['56', '123', '23', '23']
```
注意, 就算如此sum函数也是不可以执行str相加的(完全可以做到嘛,为什么不做, 不解),因此以下指令会报错
```python
>>> sum(["12", "2"], "")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: sum() can't sum strings [use ''.join(seq) instead]
```

## 函数参数显示指定与关键字参数
在介绍max函数之前, 由于max函数用到了关键字参数, 因此需要介绍一下python中的这个语法. 首先需要介绍py中多了一种指定参数的方式, 那就是显示指定, 方式如下
```python
>>> def f(a = 3, b = 5) :
...     return a + b
... 
>>> f()
8
>>> f(b = 3)
6
>>> f(b = 7)
10
>>> f(b = 9, a = 10)
19
>>> def f(a = 1, b = 3, c = 5):
...     return a + b + c
... 
>>> f(2, c = 4, b = 3)
9
```
当然这么搞的前提是必须至少把所有无初始值的参数全部确定下来, 否则会报错,这很显然,过程如下
```python
>>> def f(a, b) :
...     return a + b
... 
>>> f(b = 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: f() missing 1 required positional argument: 'a'
```

py其他地方和c++规则基本相同, 比如有初始值的参数后面不能再有没初始值的参数,举例如下
```python
>>> def f(a = 1, b, c = 5):
  File "<stdin>", line 1
    def f(a = 1, b, c = 5):
                    ^
SyntaxError: non-default argument follows default argument
```
那么同样的逻辑类比地, 在调用参数的时候, 显然显示指定的参数后面不能有非显式指定的参数,否则也会报错, 举例如下
```python
>>> def f(a, b) :
...     return a + b
... 
>>> f(b = 2, 3)
  File "<stdin>", line 1
    f(b = 2, 3)
              ^
SyntaxError: positional argument follows keyword argument
```

python中的函数有两种参数, 位置参数和关键字参数, 位置参数就和c++中的参数一样,是靠位置对应来匹配的; 还有一种参数是关键字参数, 那就是只能被显示指定的参数. 而为了将位置参数和关键字参数分开, 就要引入 `*` 的又一个新用法`*`可以做函数签名中的一个分隔符,位置参数在`*`之前，关键字参数在`*`之后, 形式如下
```python
>>> def func(a, b, *, c, d):
...     print(a, b, c, d)
... 
>>> func(1, 2, c = 3, d = 4)
1 2 3 4
>>> func(1, 2,3 ,4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: func() takes 2 positional arguments but 4 were given
```
有默认值的参数和可以被显示指定的参数以及关键字参数是三个不同的概念, 经常被搞混, 记得辨析清楚, 所以参数调用的时候都可以被显示指定, 关键字参数是指那些只能被显式指定的参数, 而有默认值的参数和关键字参数并不同, 他们确实有逻辑上的部分相似性, 我们刚才就用有默认值的参数的语法来推导出了关键字参数的一个语法, 但要记住两者毕竟不是同一个东西
## max
max就是一个有关键字参数的build-in函数, 形如`max(list, *, key = lambda(x):x, default)`
当 default未被指定的时候, max的list参数为空列表会报错, 当default被指定了的时候, max的list参数为空列表不会报错, 而是会直接返回default的值(实现方法是default是有初始值的,而这个初始值在列表为空的情况下会引发报错, 因此初始值必须被覆盖掉)
而key是一个函数, max会返回key(x)最大的x, 当未指定key的时候key(x)就是x本身, 当有多个能使key(x)达到最大值的x时, 输出最靠前的x.
举例如下, 
```python
>>> numbers = [1, 2, 3, 4]
>>> print(max(numbers, key=lambda x: -x))
1
>>> print(max(numbers, key=lambda x: 1))
1
>>> numbers = [5, 1, 2, 3, 4]
>>> print(max(numbers, key=lambda x: 1))
5
```
当然还有min, 用法和max一致
## pass
py中没有分号, 那么就没有空语句, 但py又没有大括号, 因此有的时候必须用空语句, 否则无法表示诸如c++中的while(T--);这类不执行任何循环体的循环语句, 也无法表示另外的一些东西, 比如没有任何方法的类或者什么也不做的条件分支等等这些需要用空语句或者空大括号来表达的内容

因此引入了pass语句, 它的含义就和c++中的单独的一行;或者{} 一样, 就是个空语句, 由此就可以有以下形式
```python
if x > 5:
    pass
else:
    print("x is less than or equal to 5")
```

## all
all(list)当list中所有元素的Bool值都为True的时候返回True,否则返回False,相当于多元与.注意这里list可以用Function Comprehension的方式来构建,搭配两个语法,for example:
```python
>>> all([x < 5 for x in range(5)])
True
>>> all(range(5))
False
```
当然还有any, 用法和all一致, 含义是多元或

## !!!!!exec(str)!!!!!
Python提供了一种直接把字符串中的内容当成代码来执行的方式,非常方便,直接exec(str)即可,其中str是你想要执行的存储了指令的字符串.C++想做到这个极其复杂, 但Python很简单.当然这也意味着我们需要更慎重的使用这个功能,以防止Bug或类SQL注入攻击。
要注意, exec只执行,不会像交互式解释器那样输出表达式的评估值
而还有一个类似的eval, 它可以评估(也就是求值)符合Python语法的表达式的值并返回.
for example,
```python
>>> def f(x) :
...     return x * x
... 
>>> eval("f(2)")
4
>>> exec('def g(x): \n return x * x')
>>> exec('print(g(4))')
16
>>> exec('g(4)')
>>> eval('g(4)')
16
>>> exec("""def func(x) :
...     print("test")
...     print(x)
... 
... 
... 
... """)
>>> func(5)
test
5
```

## string's in
当in运算符用于string时, 表现得有些奇怪, 用于判断的时候表示前者是否是后者的子串substring, 用于枚举时则枚举构成该string的所有字符对应的单字符字符串
for example
```python
>>> for i in "ABCDEFG" :
...     print(i)
... 
A
B
C
D
E
F
G
>>> print([i for i in "ABCDEFG"])
['A', 'B', 'C', 'D', 'E', 'F', 'G']
>>> #but

>>> 'AB' in "ABCDEFG"
True
```

## 字典Dict
for example, 
```python
>>> mydict = {'I' : 1, 'V' : 5, 'X' : 10}
>>> mydict['x']              #未定义的被查询会报错
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'x'
>>> mydict['X']
10
>>> mydict['x'] = 1          #但未定义的可以直接被赋值,相当于是个加元素的语法糖
>>> mydict['x']
1
>>> mydict[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 1
```

values()方法返回所有的value, 这里的dict_values()也是个可转化为list的对象,同理还有keys()方法
```python
>>> mydict.values()
dict_values([1, 5, 10, 1])    
>>> list(mydict.values())
[1, 5, 10, 1]
>>> sum(mydict.values())
17
>>> mydict.keys()
dict_keys(['I', 'V', 'X', 'x'])
```

重复的key会被覆盖掉
```python
>>> {1: 'first', 1:'second'}  
{1: 'second'}
```

key可以是int,float或string,但不可以是其他的容器,因为需要"可哈希"才可以做key. 这同时也告诉我们dict是个Hashmap
```python
>>> {'12':'test'}
{'12': 'test'}
>>> {'':'test'}
{'': 'test'}
>>> {[1, 2]:'test}  
  File "<stdin>", line 1
    {[1, 2]:'test}
                  ^
SyntaxError: EOL while scanning string literal
```

字典也可以推导, 有Dictionary Comprehensions, 形如`{keyExpr : valueExpr for varName in varRange if filterExpr}`
for example, 
```python
>>># {keyExpr : valueExpr for varName in varRange if filterExpr}
>>># if filterExpr is optional
>>> {x * x : x for x in range(1, 6) if x > 2 }
{9: 3, 16: 4, 25: 5}
```

然而, 有意思的是虽然PyDict是个HashMap, 但新版本中的Dict确实有序的, 这让人很难理解为什么这么设计, 这种设计会造成性能损失,但显然设计者不在乎,他们只在乎好用.换句话说新版本的Py中Dict仍然底层实现是Hash表,但是会强制保留其有序性, 这个有序性并不是真的有序性, 而是保留插入顺序,保证访问顺序一定按照插入顺序来,至于实际大小则无所谓
## 附
python中真的要注意整数除法是//呀....被这个坑着调了10min的bug才发现