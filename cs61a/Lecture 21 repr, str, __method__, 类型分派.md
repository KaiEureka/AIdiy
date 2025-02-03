Py中一切对象都可以被str()和repr()转化为字符串,repr()转化成的字符串内部的内容就相当于交互式解释器输出的内容.eval只能评估表达式,repr则是可以评估一切,表达式直接评估,非表达式则是会指明其内容
For example, 
```python
>>> 12e12
12000000000000.0
>>> print(repr(12e12))
12000000000000.0
```
str则是返回一个更加人类可读的字符串, 其内容如果没有被特别定义,那么和repr是一样的,如果被特别定义那么自然是不一样的
For example, 
```python
>>> from fractions import Fraction
>>> half = Fraction(1, 2)
>>> repr(half)
'Fraction(1,2)'
>>> str(half)
'1/2'
```
具体而言,str和repr的内容都是可以自定义的,这其实也是之前range(1,3)返回range(1,3)而不是[1, 2]的原因,之前误以为这语法制定者专门开辟的语法糖,现在才发现并不是,其实只是利用了repr和str机制所制作出来的,完全在现有语法框架内,并不是新的语法糖,库作者可以这么写我们也可以,具体如下

---------
在Python中，自定义类可以定义`__repr__`和`__str__`方法来返回自定义的内容，它们的主要作用和区别如下：

- **`__repr__`方法**
    - **作用**：`__repr__`方法是一个用于返回对象的“官方”字符串表示的特殊方法，通常用于开发者调试和记录日志等场景，希望通过该方法返回的字符串能够准确地表达对象的状态，以便于能够用该字符串重新创建出这个对象。
    - **示例**
```python
class MyClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"MyClass({self.value})"

obj = MyClass(42)
print(repr(obj))  
```
    - 输出
`MyClass(42)`

- **`__str__`方法**
    - **作用**：`__str__`方法用于返回对象的字符串表示，主要用于向用户展示对象的信息，通常更注重可读性和用户友好性。当使用`print()`函数输出对象或者使用`str()`函数将对象转换为字符串时，会调用`__str__`方法。
    - **示例**
```python
class MyClass:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"这是一个值为 {self.value} 的MyClass对象"

obj = MyClass(42)
print(str(obj))  
```
    - 输出
`这是一个值为 42 的MyClass对象`

如果没有定义`__str__`方法，Python会尝试调用`__repr__`方法来获取字符串表示。在很多情况下，建议让`__repr__`方法返回的字符串能够准确地表达对象的状态，以便于调试和开发，而`__str__`方法返回更适合用户阅读和理解的内容。
实际上,repr方法的实现恰恰就是调用内置的__repr__
For example, 
```python
def repr(x): 
	return type(x).__repr__(x)
```

为什么不采用下面这种?
```python
def repr(x): 
	return x.__repr__()
```
因为Py的方法可能随时被临时重写,要确保调用这个类的这个方法,可不是这个实例自己绑定的方法,实例可能被绑定了奇怪的东西,是不可信的,看下面这个例子就明白了
```python
class TestClass:
    def __repr__(self):
        return "Original repr"

test_obj = TestClass()

# 重写 __repr__ 属性
test_obj.__repr__ = lambda: "Custom repr"

# 第一种方式
def repr1(x):
    return type(x).__repr__(x)

# 第二种方式
def repr2(x):
    return x.__repr__()

print(repr1(test_obj))  # 输出: Original repr
print(repr2(test_obj))  # 输出: Custom repr
```


--------
Py中特殊的函数也被称为方法,比如`__init__,__repr__,__str__`等等,类似的还有类型转换函数`__bool__, __float__, __int__`,以及和运算符对应的函数比如`__add__`,实际上所有运算符都是在调用对应的特殊方法,比如bool(x)其实是调用`type(x).__bool__(x)`;a + b相当于add(a,b)其实是调用`type(a).__add__(a, b)`
因此很显然,我们可以如此来重载类型转换运算以及重载算术运算符
具体而言的全面介绍如下

------

在Python中，以双下划线开头和结尾的方法被称为特殊方法（也称为魔术方法），这些方法为类提供了与Python内置操作和语法的交互能力。`__add__` 就是其中之一，用于定义对象的加法行为。以下是Python中常见的特殊方法分类介绍：

### 1. 基本定制
- **`__new__(cls, *args, **kwargs)`**：创建对象时调用的第一个方法，它是一个静态方法，负责创建并返回一个新的对象实例。通常用于实现单例模式或自定义对象创建过程。
```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # 输出: True
```
- **`__init__(self, *args, **kwargs)`**：对象初始化方法，在 `__new__` 方法返回实例后调用，用于对对象进行初始化设置。
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 25)
print(p.name)  # 输出: Alice
```
- **`__del__(self)`**：对象被销毁时调用的方法，用于释放对象占用的资源。需要注意的是，由于Python的垃圾回收机制，不能保证该方法一定会被调用。
```python
class Resource:
    def __init__(self):
        print("Resource created")
    def __del__(self):
        print("Resource destroyed")

r = Resource()
del r  # 输出: Resource destroyed
```
- **`__repr__(self)`**：返回一个字符串，用于表示对象的官方字符串表示形式，通常用于调试和开发环境。
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(1, 2)
print(repr(p))  # 输出: Point(1, 2)
```
- **`__str__(self)`**：返回一个字符串，用于表示对象的用户友好字符串表示形式，通常用于打印对象。
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(p)  # 输出: (1, 2)
```

### 2. 比较运算符
- **`__lt__(self, other)`**：定义小于（`<`）比较运算符的行为。
- **`__le__(self, other)`**：定义小于等于（`<=`）比较运算符的行为。
- **`__eq__(self, other)`**：定义等于（`==`）比较运算符的行为。
- **`__ne__(self, other)`**：定义不等于（`!=`）比较运算符的行为。
- **`__gt__(self, other)`**：定义大于（`>`）比较运算符的行为。
- **`__ge__(self, other)`**：定义大于等于（`>=`）比较运算符的行为。
```python
class Person:
    def __init__(self, age):
        self.age = age
    def __lt__(self, other):
        return self.age < other.age

p1 = Person(20)
p2 = Person(25)
print(p1 < p2)  # 输出: True
```

### 3. 算术运算符
- **`__add__(self, other)`**：定义加法（`+`）运算符的行为。
- **`__sub__(self, other)`**：定义减法（`-`）运算符的行为。
- **`__mul__(self, other)`**：定义乘法（`*`）运算符的行为。
- **`__truediv__(self, other)`**：定义真除法（`/`）运算符的行为。
- **`__floordiv__(self, other)`**：定义整除（`//`）运算符的行为。
- **`__mod__(self, other)`**：定义取模（`%`）运算符的行为。
- **`__pow__(self, other[, modulo])`**：定义幂运算（`**`）运算符的行为。
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
print(v3.x, v3.y)  # 输出: 4 6
```

### 4. 反向算术运算符
当左操作数不支持相应的算术运算时，会调用右操作数的反向算术运算符。例如，`a + b` 中，如果 `a` 没有定义 `__add__` 方法，而 `b` 定义了 `__radd__` 方法，则会调用 `b.__radd__(a)`。
- **`__radd__(self, other)`**
- **`__rsub__(self, other)`**
- **`__rmul__(self, other)`**
- **`__rtruediv__(self, other)`**
- **`__rfloordiv__(self, other)`**
- **`__rmod__(self, other)`**
- **`__rpow__(self, other)`**

### 5. 增量赋值运算符
- **`__iadd__(self, other)`**：定义 `+=` 运算符的行为。
- **`__isub__(self, other)`**：定义 `-=` 运算符的行为。
- **`__imul__(self, other)`**：定义 `*=` 运算符的行为。
- **`__itruediv__(self, other)`**：定义 `/=` 运算符的行为。
- **`__ifloordiv__(self, other)`**：定义 `//=` 运算符的行为。
- **`__imod__(self, other)`**：定义 `%=` 运算符的行为。
- **`__ipow__(self, other)`**：定义 `**=` 运算符的行为。
```python
class Counter:
    def __init__(self, value):
        self.value = value
    def __iadd__(self, other):
        self.value += other
        return self

c = Counter(5)
c += 3
print(c.value)  # 输出: 8
```

### 6. 一元运算符
- **`__neg__(self)`**：定义负号（`-`）运算符的行为。
- **`__pos__(self)`**：定义正号（`+`）运算符的行为。
- **`__abs__(self)`**：定义绝对值（`abs()`）函数的行为。
```python
class Number:
    def __init__(self, value):
        self.value = value
    def __neg__(self):
        return Number(-self.value)

n = Number(5)
m = -n
print(m.value)  # 输出: -5
```

### 7. 容器类型相关
- **`__len__(self)`**：定义 `len()` 函数的行为，返回容器的长度。
- **`__getitem__(self, key)`**：定义通过索引或键访问容器元素的行为。
- **`__setitem__(self, key, value)`**：定义通过索引或键设置容器元素的行为。
- **`__delitem__(self, key)`**：定义通过索引或键删除容器元素的行为。
- **`__contains__(self, item)`**：定义 `in` 运算符的行为，判断元素是否在容器中。
```python
class MyList:
    def __init__(self):
        self.data = []
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]
    def __setitem__(self, index, value):
        self.data[index] = value
    def __delitem__(self, index):
        del self.data[index]
    def __contains__(self, item):
        return item in self.data

ml = MyList()
ml.data = [1, 2, 3]
print(len(ml))  # 输出: 3
print(ml[1])    # 输出: 2
ml[1] = 4
print(ml[1])    # 输出: 4
del ml[1]
print(ml.data)  # 输出: [1, 3]
print(3 in ml)  # 输出: True
```

### 8. 迭代器相关
- **`__iter__(self)`**：返回一个迭代器对象，用于支持迭代操作。
- **`__next__(self)`**：定义迭代器的下一个元素获取行为，当没有更多元素时，抛出 `StopIteration` 异常。
```python
class MyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current < self.end:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration

mr = MyRange(0, 3)
for i in mr:
    print(i)  # 输出: 0 1 2
```

### 9. 上下文管理器相关
- **`__enter__(self)`**：进入上下文管理器时调用的方法，返回一个对象，该对象会被赋值给 `as` 后面的变量。
- **`__exit__(self, exc_type, exc_value, traceback)`**：退出上下文管理器时调用的方法，用于处理异常和清理资源。
```python
class File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

with File('test.txt', 'w') as f:
    f.write('Hello, World!')
```



------
## isinstance
Py中提供了一个比type()更智能的判断类型的方法, isinstance(things, type)返回bool值表示things是不是type类型的,这个判断会考虑继承,也就是子类和父类类型不同,但是子类对象也属于父类对象.注意,子类对象是父类类型的,但父类对象不是子类类型的
For example, 
```python
# 定义父类 A
class A:
    def __init__(self):
        print("A 的构造函数被调用")
# 定义父类 B
class B(A):
    def __init__(self):
        print("B 的构造函数被调用")

print(isinstance(B(),A)) #True
print(isinstance(A(),B)) #False
```
通过这个机制可以不修改原类型的方式来实现函数多态, 那就是简单的通过isinstance判断类型然后if-elif-else式来分别运行即可,这个机制其实叫做类型分派
至于Cpp式的函数重载,Py其实是没有的,只有以上变相实现的机制,因为Py是个动态类型的机制,压根没法指定类型那又如何定义形式一致但类型不一致的函数?