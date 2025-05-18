#cs61a #python语法 

Py中的异常语句是`raise <expression>`，其中表达式必须可以被评估为某个类或者某个类的实例(实际上只能接类实例, 能接类只是一个让人困惑的语法糖,实际行为是直接调用默认构造函数创造了一个默认实例,Py中所有类都有默认构造函数所以不用担心这里引发异常)，Py内置了一些异常类，程序会自动调用这些异常类，程序员可以手动调用这些类，程序员也可以定义并调用自己的用于表示异常的类

常用内置类有
- TypeError 函数调用错误，即函数调用时传参的数量/类型错误
- NameError 名字找不到
- KeyError  访问不存在的键
- RecursionError 递归太深
这些类想要创建实例只需要导入一个字符串作为构造函数参数即可，这也是异常类一般而言的表示方式，比如`TypeError("异常信息")`。
具体而言，举例如下
```python
def double(x):
	if isinstance(x, str):
		raise TypeError("double takes only Tunibers")
	return 2 * x
	
>>> double('2')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in double
TypeError: double takes only Tunibers
```

------


异常本身是一个个可以存入信息的实例，而非只有一种异常，不仅仅是为了在发生异常时采用raise语句让程序员知道发生了什么异常，还为了能让程序员为程序引入处理异常的方式，这就需要try语句了
```python
try:
	<try suite>
except <exception class> as <name>: # as <name> 是可选部分
	<except suite>
# 如果想要捕获多种异常,可以直接写多个except字句
except <exception class> as <name>: 
	<except suite>
```

无论如何，`<try suite>`都会被执行, 当`<try suite>`执行时如果没发生异常,则`<except suite>`不会被执行. 如果发生异常但不是`<exception class>`类型的异常,那么会正常中断程序输出异常信息, 但如果发生的异常恰好是`<exception class>`类型的异常,则不会中断程序,而是会执行`<except suite>`内的内容,同时如果写了`as <name>`那就会为捕获的这个异常实例命名为`<name>`方便在`<except suite>`内访问这个异常
注意到,不论是扔出的异常还是铺获的异常, 都是一个实例. 只不过是铺获的时候是且只能是选择针对某一类进行铺获而已,表达异常信息的终究是实际存在的对象,而不是类本身,这是合理的. 

For example, 
![[../Attachment/pictures/Pasted image 20250216222442.png]]

制作IO时或者各种东西的时候,都可能面对一种需求,即出现异常时,程序不应该立刻崩溃停机,而是应该继续运行下去,并用一种可以接受的方式来解决这个异常,这就是try语句的意义了,这和cpp的try-catch语句是一样的

-----------

解释器内容待完成