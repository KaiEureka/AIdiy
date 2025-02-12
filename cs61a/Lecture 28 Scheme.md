#cs61a #Lisp #Scheme 
Lisp 由美国计算机科学家约翰・麦卡锡（John McCarthy）在 1958 年发明，是第二古老的高级编程语言（仅次于 Fortran）。它的设计灵感来源于数学中的 lambda 演算。Lisp各个版本逐渐整合成了一个统一的版本，称为Commom LISP。然而留下了一种方言，名为Scheme。Scheme十分简洁，其语法规范的全部内容甚至没有比CommomLisp规范的目录长，以其极简主义而被推崇

很显然，我们学习Scheme有一大作用，那就是这种语言的编译器非常好写，可以用于练习编译原理。同时加深对函数式编程和Lambda算子的理解

guile可以用来编译和运行Scheme，在mac系统下使用brew即可自动安装。

其一切过程都是函数形式的，或者说表达式形式的，写成了括号形式，聚体育法细节很简单 
![[../Attachment/pictures/Pasted image 20250212175000.png]]
Lambda表达式更是Scheme的核心
![[../Attachment/pictures/Pasted image 20250212175304.png]]

以及一个没屁用的cond语法糖
![[../Attachment/pictures/Pasted image 20250212175537.png]]

由于一切嵌套结构是用括号来完成的，而括号内需要时一个表达式，因此需要引入begin，其作用类似于Cpp的逗号，可以把若干个表达式视为一个式子，从而塞进只有一个式子才能进的地方，比如：
![[../Attachment/pictures/Pasted image 20250212175655.png]]
## let表达式


与define这种定义变量和函数的绑定式类似的，还有一个Let表达式。define表示全局的定义，let则是局部的定义，相当于引入了一个暂时的临时变量
```scheme
(let ((var1 val1)
      (var2 val2)
      ...
      (varN valN))
  body1
  body2
  ...
  bodyM)
```
let\*表达式语法上和let一样，但是let\*允许后续定义式使用前面的定义的临时变量，如下
```scheme
(let* ((x 2)
       (y (* x 3)))
  (+ x y))
```
letrec表达式就更强大了，允许表达式之间不按顺序的随意递归引用，如下
```scheme
(letrec ((factorial (lambda (n)
                      (if (= n 0)
                          1
                          (* n (factorial (- n 1)))))))
  (factorial 5))
```

let表达式最终肯定是要返回结果的，当有多个body语句时最后一个语句的评估值就是返回值，当只有一个语句时自然这个语句就是“最后一个语句”