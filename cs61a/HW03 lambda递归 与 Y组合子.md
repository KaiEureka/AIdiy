#cs61a #python语法 

发现了一种实现lambda函数递归的方式

```python
func = lambda x : edgeValue if x == edge else recursionExpressionBasedOnFunc
```
这里的 = 不是赋值, 而是一种绑定, 把func这个名字和右边这个lambda绑定了起来,就相当于强行给lambda起了名字 因此就可以递归了, 这就是原理.这显然也是基于Python是解释类语言的这个性质, 因为解释器的执行规则是遇到fact就重新跳到这里来执行因此实现了绑定这个操作嘛

然后有一种不用赋值这个过程的递归, 称之为Y组合子

```python
def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial',
    ...     ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'FunctionDef', 'Recursion'])
    True
    """
    
    # how
    return (lambda anyfunc : anyfunc(anyfunc))  (lambda func : (lambda n : 1 if n == 1 else mul(func(func)(sub(n, 1)), n))) 

```

返回值代替赋值,那么就只能赋值一次, 起不到一直绑定的作用,因此把

```python
func = lambda n : 1 if n == 1 else mul(func(sub(n, 1)), n)
```

改成
```python
lambda func : (lambda n : 1 if n == 1 else mul(func(func)(sub(n, 1)), n))
```

就给出一个能让函数递归展开一步的函数

再给出一个让输入无限调用自身的函数`lambda f : f(f)` 

再让前者调用后者, 就实现了递归

那么昨天[[lab02 逻辑运算与bool_evaluate]]的那个三行函数(算上函数头四行)还可以进一步简化为一行函数
```python
lambda f1, f2, f3 : (lambda f:f(f)) (lambda func : lambda n, now = 0 : lambda x : x if now == n else func(func)(n, now + 1)([f1, f2, f3][now % 3](x)))
```

今天的这个巧式虽然实现了递归, 但是不够优雅, 如何不改变原递归函数形式来实现递归呢?很简单就是把这个递归形式的假递归函数到巧式的过程本身写成一个函数, 然后调用这个函数即可, 也就是
```python
def make_anonymous_factorial():
    
    return (lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda func : lambda n : 1 if n == 1 else mul(func(sub(n, 1)), n))
```

其中这个`(lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))`就是大名鼎鼎的Y组合子,Y(f)即可有递归形式的f生成有递归功能的真递归式

这东西没有什么直接使用的必要,他被提出仅仅是在逻辑上证明任何递归函数都可以被Lambda表示(用这种方法即可,因此得证), 而循环都可以转化为递归, 因此Lambda演算是图灵完备的, 这奠定了函数式编程的基础, 同时也是一个重要的计算机数学定理