#cs61a #python语法 


py也存在链式赋值比如```b=a=3```,行为和cpp一致,但这其实是一个被单独拿出来特别实现出来的语法糖, 并不是像cpp那样由于万物皆有返回值而自然推导出来的语法 py的赋值语句是没有返回值的, 连None都不返回,也就是说```print(a = 5)```会直接报错, 而不是输出None

-----
py中还有一种断言语句,类似于条件语句,当条件为真的时候什么也不会发生,当条件为假的时候终止程序并将跑出AssertionError异常, 并后面的内容当作错误原因输出出来,比如
```python
assert 2 > 3, "math is existed"
```
运行后输出
```
Traceback (most recent call last):
  File "/Users/Kai/Desktop/cs61a/lab/lab01/test.py", line 1, in <module>
    assert 2 > 3, "math is broken"
AssertionError: math is existed
```

-----
py中有一种在cpp中绝对错误的没道理的行为,他可以直接返回一个局部函数,不仅这个局部函数不会被销毁,甚至这个局部函数用到的其他局部变量也都不会被销毁,而是会被保存起来,这是一种语法糖,称之为闭包,形式如下
```python
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function


# 使用闭包
add_five = outer_function(5)
print(add_five(3))  # 输出 8
print(add_five(7))  # 输出 12
```
也就是说,A中有一些局部变量和局部函数,且某个局部函数f引用了A中的部分局部变量,并且A返回了这个局部函数f,那么f和被f引用的局部变量就会被打包起来,那些局部变量的值就和床创建f的那个A运行到return f的那一刻的那些对应变量的值一样
注意, 是"A运行到return f的那一刻", 而不是定义局部函数的那一处,没什么道理,语法糖不是推断出来的语法,而是凭空定义的,就是不讲道理的. 下面是个例子,能很好地说明这一点
```python
def outer_function(x):
    def inner_function(y):
        return x + y
    x = x + 1
    return inner_function


# 使用闭包
add_five = outer_function(5)
print(add_five(3))  # 输出 9
print(add_five(7))  # 输出 13
```

-----
