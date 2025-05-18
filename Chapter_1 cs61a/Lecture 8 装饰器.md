#cs61a #python语法 

py中又有一种语法糖了, 是在def的前一行加上@xxx之类的语句,表示下面def的这个函数实际上是被xxx装饰器修饰后的效果, 也就是说
```python
@decorator
def f() :
	something
```
等价于
```python
def pref():
	something
f = decorator(pref)
```

为了引入一个强行定义的语法糖甚至直接引入了一个新符号, py的语法规则果然简单粗暴, 或者说py压根就没有语法规则, 只不过是一大堆语法糖凑在了一起的一坨东西而已, 用起来确实简单, 但其实记忆起来反而麻烦一些,但问题不大

注意 decorator可以是module中定义好了的装饰器, 也可以是任何自己定义的装饰器, 之前说过,装饰器就是一种特殊的闭包, 输入函数并输出函数, 所感的内容基本就是在函数运行之前和运行之后输出一些东西或者做一些其他事情,也即形如:
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 在调用原函数之前的操作
        print("Before function execution")
        result = func(*args, **kwargs)
        # 在调用原函数之后的操作
        print("After function execution")
        return result
    return wrapper
```

举个例子, 下面是一个自定义的很有用的decorator
```python
def trace(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数 {func.__name__}，参数：args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"函数 {func.__name__} 调用结束，结果：{result}")
        return result
    return wrapper
```
其中 args 是把所有元素打包成 tuple后的内容,  kwargs是把所有key-value对打包成dict后的内容,因此```def wrapper(*args, **kwargs)```可以搞定任何形式的函数参数