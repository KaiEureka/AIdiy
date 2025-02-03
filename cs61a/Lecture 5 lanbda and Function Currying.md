#cs61a #python语法 

python中lambda表达式形如 lambda 参数 : 返回值表达式
比如 
```
square = lambda x : x * x
f = lambda : 2
```

这里介绍了一个很唬人的机制, 但其实细分析并没什么的过程,称之为Function Currying(函数科里化, 因为被一个叫做Curry的人重新发现), 实际上就是把一个多参数函数变成了一个高阶单参数函数的过程,示例如下, 细看一下就能明白,并不复杂
![[Pasted image 20250120173532.png]]