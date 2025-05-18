#cs61a #python语法 

py中的逻辑运算符和cpp一样是短路的, 但也有区别, 那就是在cpp中逻辑运算符的结果一定是bool量, 但python中逻辑运算符的结果就是操作数之一.

比如 and 的规则是 左侧操作数的bool值为True则运算结果为右侧操作数,否则运算结果为左侧操作数,举个例子
	12 and 13的结果是13 
	0 and 13 的结果是0
	None and 13的结果是None
	True and -1的结果是-1
or 同理 返回的东西是操作数之一 并不一定是bool量

不过not难得良心,返回的东西确确实实是bool量,所以not not()其实相当于bool()

以及表达式的value确实是bool量, 比如print(1>0)结果是True

evaluate表达式的bool值的时候, 只有None  0  ""  False 这四个东西以及与这四个相等的东西的Bool值是False, 其他所有东西的Bool值都是True

-----------
另外附加一个发现的规则, 在交互式解释器中, 只要输入的东西evaluate值不为None, 就会被输出, 而None则不会被输出, 所以print("test")只会输出test不会输出test\nNone, a = 5则是什么也不会输出.在非None的时候,是Function会直接输出这是一个Function, 非Function会输出其值

---------

py中没有函数声明, 但函数也需要先定义后使用, 但这个先后顺序同样非常实用主义, 解释器是一行一行向下解析的, 只要函数被实际调用的那一刻, 解释器已经知道了函数的定义以及函数直接或间接调用的函数的定义即可, 而并不需要函数本身在逻辑上满足先后顺序, 也就是说,
```python
def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    "*** YOUR CODE HERE ***"
    return a * b // gcd(a, b)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

multiple(3, 4)
```
虽然先定义muliple后定义gcd, 但由于调用multiple的那一句multiple(3,4)出现在gcd之后,所以解释器解释到这里的时候可以正常工作,因此完全不会报错.
而如果这样, 那么就会报错了:
```python
def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    "*** YOUR CODE HERE ***"
    return a * b // gcd(a, b)
    
multiple(3, 4)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
```

这又是解释类语言和编译类语言的区别了,解释类语言不需要逻辑上自洽,只需要解释器明白即可.... 显然以上两种在cpp中都是语法错误,但在py中则是一种可以另一种不行

----------
以及发现了一道很有趣的题, 我用了一种非常优雅的做法解决了本题, 肯定比出题教授的解法更优雅, 同样功能cpp可能需要30行才能解决,第一次意识到py这种解释性语言的好处了,就是他会有很多语法特性, 这些语法特性有利于简单的几行代码描述出复杂的逻辑,而这是cpp所做不到的, 题目如下
```python
def cycle(f1, f2, f3):
    """Returns a function that is itself a higher-order function.

    >>> def add1(x):
    ...     return x + 1
    >>> def times2(x):
    ...     return x * 2
    >>> def add3(x):
    ...     return x + 3
    >>> my_cycle = cycle(add1, times2, add3)
    >>> identity = my_cycle(0)
    >>> identity(5)
    5
    >>> add_one_then_double = my_cycle(2)
    >>> add_one_then_double(1)
    4
    >>> do_all_functions = my_cycle(3)
    >>> do_all_functions(2)
    9
    >>> do_more_than_a_cycle = my_cycle(4)
    >>> do_more_than_a_cycle(2)
    10
    >>> do_two_cycles = my_cycle(6)
    >>> do_two_cycles(1)
    19
    """
    "*** YOUR CODE HERE ***"
    def resfunc(n, now = 0) :
        return lambda x : x if now == n else resfunc(n, now + 1)([f1, f2, f3][now % 3](x))
    return resfunc
```
