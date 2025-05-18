#unix #terminal #cs61a

## mv A B
当B是一个文件夹的时候是把A移入B，当B是一个文件名的时候，则表示将A重命名为B，并删除掉原有的B（如果有的话），但这不是单独的特殊逻辑或者特殊语法，这其实是合理的，想想这里面的逻辑就能理解

## cd
- cd .. 进入母目录 （这里要注意 ..代表母目录，.代表当前目录）
- cd - 返回上一步的目录
- cd ~ 进入$HOME 也可以直接写作cd
- cd

## cp A B
把A复制一份并以B为名字，比如cp example/unix_commands.txt .表示把example/unix_commands.txt复制到当前路径下

## cat A
简单的查看某文件的内容

## rm
- rm A ： A必须是一个文件，此时表示删除A
- rm -r A ： A此时是一个文件夹， 表示递归地删除A 

## man
相当于帮助指令，比如man ls