#cs61a #python语法 

在python中，单引号 (`'`) 和双引号 (`"`) 没有本质上的区别。它们都可以用来定义字符串，并且功能完全相同，py中没有类似于char的东西

另外顺便学了一下print的用法，AI给出了一个好的解析:

在 Python 中，如果你想在 print函数中输出多个值而不在它们之间加入空格，可以使用 `sep` 参数将分隔符设置为空字符串。默认情况下，print函数在输出多个值时会在它们之间插入一个空格。
例如：

```python
def func(a, b, c):
    print(a, b, c, sep='')  # 不在 a, b, c 之间插入空格

my_list = [1, 2, 3]
func(*my_list)  # 输出 123

my_dict = {'a': 1, 'b': 2, 'c': 3}
func(**my_dict)  # 输出 123
```

在这个例子中，`sep=''` 将分隔符设置为空字符串，因此print函数在输出 a、b和 c时不会在它们之间插入空格。

如果你只想输出两个值而不在它们之间插入空格，可以这样做：

```python
print('Hello', 'World', sep='')  # 输出 HelloWorld
```

或者，如果你想在函数中实现类似的效果：

```python
def func(a, b):
    print(a, b, sep='')  # 不在 a 和 b 之间插入空格

func('Hello', 'World')  # 输出 HelloWorld
```

这样，你可以在输出多个值时控制它们之间的分隔符。


此外, py在发生错误时输出的Traceback信息是这样的, 他会错误发生出不断上溯, 一直到一个顶级调用为止, 然后把这个调用链按照先后顺序输出, 比如运行
```python
def e():
	print("This is a test")
def h(x):
	return x + 0
def g(x, y):
	return h(x + y * 5)
def f(x):
    e()
    return g(x + x, x)

e()
f("hi")

```
输出
```
This is a test
This is a test
Traceback (most recent call last):
  File "/Users/Kai/Desktop/cs61a/hw/hw01/test.py", line 12, in <module>
    f("hi")
  File "/Users/Kai/Desktop/cs61a/hw/hw01/test.py", line 9, in f
    return g(x + x, x)
  File "/Users/Kai/Desktop/cs61a/hw/hw01/test.py", line 6, in g
    return h(x + y * 5)
  File "/Users/Kai/Desktop/cs61a/hw/hw01/test.py", line 4, in h
    return x + 0
TypeError: can only concatenate str (not "int") to str
```
注意到Traceback表示开始展示报错处所在调用链, Traceback中没有e()相关的内容, 就是因为e是一次正常调用, 不在"从第一个错误处到顶级调用"的这条链上, 不论是顶级frame中的e还是f中的e,都不在这条错误链上

另外py有一个语法细节就是不允许混用Tab和空格表示的缩进, 因为缩进本身具有严格的含义, 这点是我最讨厌py的一点, 为什么不能学cpp用大括号而不是缩进来表达语义呢?

py中#表示单行注释, 没有多行注释, 但是'''xxx'''可以用来表示跨行字符串(会把跨行这个动作本身解析为\n), 那么凭空的一个字符串自然不会产生任何作用, 所以完全可以用跨行字符串(正式名称是文档字符串)来变相表达跨行注释的效果,比如
```python
def square(x):
       '''
       >>> square(2)
       4
       '''
       return x * x
```
\`\`\`中间的内容就是注释

特别的, 文档字符串(docstring)中的内容写成特定形式可以视为一个示例, 并被doctest模块自动运行,AI是这么解释这个过程的:

`doctest` 是 Python 标准库中的一个模块，用于从文档字符串（docstring）中提取示例代码并执行这些示例，以验证它们的输出是否与预期结果一致。这有助于确保代码的正确性，并提供使用示例。
### 编写 `doctest`
要编写一个 `doctest`，你需要在函数的文档字符串中包含示例代码和预期输出。以下是一个示例，展示如何编写一个 `doctest` 来断言 `square(2) == 4`：

```python
def square(x):
    """
    Return the square of x.

    >>> square(2)
    4
    >>> square(3)
    9
    """
    return x * x
```

在这个示例中，文档字符串包含了两个 `doctest`：
- `>>> square(2)` 预期输出 `4`
- `>>> square(3)` 预期输出 `9`

### 运行 `doctest`
要运行 `doctest`，你可以使用 `doctest` 模块的 `testmod` 函数。以下是一个示例，展示如何运行 `doctest`：

```python
import doctest

def square(x):
    """
    Return the square of x.

    >>> square(2)
    4
    >>> square(3)
    9
    """
    return x * x

if __name__ == "__main__":
    doctest.testmod()
```

当你运行这个脚本时，`doctest` 模块会自动提取文档字符串中的示例并执行它们。如果所有示例的输出都与预期结果一致，则测试通过；否则，`doctest` 会报告失败的示例。

如果一切正常，运行脚本不会有任何输出，表示所有测试通过。如果有测试失败，`doctest` 会报告失败的示例和实际输出。

通过添加这些 `doctest`，你可以确保你的函数在各种输入下都能正确工作，并且可以自动化测试这些示例。

总的来说,  `doctest`模块通过解析文档字符串（docstring）中的特定格式来识别和执行测试。它会识别文档字符串中以 >>> 开头的行作为输入，并将后续的行视为预期输出。具体来说，doctest 会执行这些输入行，并将实际输出与预期输出进行比较。如果它们匹配，则测试通过；否则，测试失败。

doctest 会识别以 >>> 开头的行作为输入。这些行通常模拟交互式 Python 解释器中的输入。紧跟在输入行之后的行被视为预期输出，直到遇到下一个 >>> 或者文档字符串的结束。

python运行指令后面加 -i 可以在运行Python脚本后启动交互式解释器,以便在运行技术后继续调试代码

有一个简便的无需改原代码的doctest方式, 就是直接用
```
python3 -m doctest -v program.py
```
即可