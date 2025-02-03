#cs61a #python语法 

Python中的类方法第一个变量就是调用者本身,通常命名为self(但不强求),从第二个开始是真正调用的内容,class内部直接定义的是类静态变量,是属于全类的,Py中的类数据成员无需定义,直接拿来就用即可,构造函数写作__init__(必须如此)内可以直接定义他们的初始值,甚至使用者也可以在类外部使用类的时候随意为某个实例创造新数据成员,直接赋值即可,不会报错.如果临时创造的新数据成员和类变量重名, 那么仅仅针对这个实例,数据成员就会顶替掉原本的类方法(这个语法糖和dict类似,直接为不存在的东西赋值被视为引入新成员,是可以的,但访问不存在的东西确实要报错的)
For example, 
```python
class Account :
    interest = 0.02
    def __init__(self, name) :
        self.balance = 0
        self.name = name

    def deposit(myself, amount) :
        myself.balance += amount

    def withdraw(self, amount) :
        self.balance -= amount

    def get_balance(self) :
        return self.balance

JA = Account("Jim")
TA = Account("Tom")

JA.fuck = 2 
print(JA.fuck) #output 2
#print(TA.fuck) #ERROR

Account.interest = 0.08
print(JA.interest) #output 0.08
print(TA.interest) #output 0.08

JA.interest = 0.04
print(JA.interest) #output 0.04
print(TA.interest) #output 0.08
```

有意思的是,类方法可以和实例绑定,从函数成为方法(method),这个语法糖表明Py真的一切都是一类值...不像cpp,cpp几乎啥都是二等公民
```python
>>>tom_account = Account('Tom')
>>> f1 = Account.deposit
>>> type(f1)
<class 'function'>
>>> f2 = tom_account.deposit
>>> type(f2)
<class'method'>
>>>Account.deposit(tom_account, 1001)
1011
>>> tom_account.deposit(1007)
2018
```

------

## 继承
Py中继承的语法如下
```Python
class CheckingAccount(Account):
	interest = 0.01
	def withdraw(self, amount):
		amount = amount + 1
		balance -= amount
```
即可创建Account类派生的CheckingAccount类
Py中派生类的同名函数将会简单的隐藏掉基类对应的函数, 注意和cpp一样,是隐藏而不是覆盖,如果指名道姓还是可以访问的,Py没有::运算符, 直接用点运算符来实现这一点
For example, 
```python
class CheckingAccount(Account):
	interest = 0.01
	withdraw_fee = 1
	def withdraw(self, amount):
		amount = amount + withdraw_fee
		return Account.withdraw(self, amount)
```
如下是个较为复杂的例子
![[Pasted image 20250202154414.png]]

---------
Py本身就是动态语言, 不需要虚机制也可以多态,因此没有虚函数等语法.但还是有多重继承的语法的,使用也很简单,直接如下即可
```python
class sbAccount(CheckingAccount, SavingAccount):
	def __init__(self, aholder):
		self.holder = aholder
		self.balance = 1
```
Py中如果子类没有自己的构造函数,那就用第一个父类的构造函数来构造自己,如果有自己的构造函数,那就调用自己的构造函数,调用完以后也并不会自动调用自己父类的构造函数,如果不显式地由程序员调用,那就压根不会被调用,可以玩一下下面这个测试代码,就明白了
```python
class A:
    def __init__(self):
        print("A 的构造函数被调用")
class B:
    def __init__(self):
        print("B 的构造函数被调用")
class C(A, B):
    def __init__(self):
        print("C 的构造函数被调用")
# 创建子类 C 的实例
c = C()
# 查看子类 C 的 MRO 列表
print(C.__mro__)
```
如果两个父亲有同名方法,或者任何其他的,总之和上面是同一个问题,那就是现在函数需要一个xx方法(init或者程序员调用的某方法),到底用哪个?那就是要看MRO列表,也就是调用顺序,Py中采用用了非常简单从继承列表的左为优先进行深度优先遍历,第一个搜到的就是被调用的同名方法,也仅仅会调用这一个,就如此实现多态

---------

Py中的类的每个实例都可以被用户任意的绑定新的数据成员,要阻止这种行为可行的,如下即可
```python
class A:
	__slots__ = ('attr1', 'attr2')
```
这样A类就有且只能有attr1和attr2这两个成员了

-----
在Py中可以通过方法名前加两个下划线表示私有权限,加单个下划线表示受保护权限,非法的访问会引起报错,但是,实际上Py还是提供了无视一切权限的访问方式,只需要加上_类名前缀即可,实际上这正是私有和保护权限的成员被隐藏起的方式,之前的报错也不是真的报错,而是访问了不存在的东西而引起的自然报错而已,Py所谓的权限控制只不过是系统加上了一个前缀帮你隐藏起来了而已,并不是真正强制的要求,你还是可以完全通过语法来越过权限设置的,只不过这么做并不被推荐