
### 困惑
1. 首先按理来说，学习率应该随着训练逐渐变小才好，但我乱试验时写了一个每迭代10个epoch就让学习率翻倍的离谱策略，却意外的表现得极其好，完全没有震荡，loss收敛到了1e-10都还在稳定收敛，请问这是为什么？
2. 我对FNN的理解是在高维空间中拟合出超平面包络住所有分类数据，按照这个理解是足够拟合出任何复杂的超平面的，也就是说测试集上如果我不管是否测试机过拟合的话，我是可以强行训练到训练集100%准确率的，但实际却并非如此，训练集停到了99.65%，剩下的数据我可视化一看也不复杂啊，但网络就是死活不理解学不会。而且我这么不管过拟合的狂训却不知道为什么完全没导致过拟合，起码测试集的准确率单调递增涨到了97.5%，为什么测试集都做不到100%呢？
3. 最离谱是这个，我第一遍写错了，反向传播计算梯度时忘了把最后一层softmax计算在内了，运行代码时却跑起来了！收敛到了训练集97测试机95的成绩，这太离谱了，梯度压根就算错了这咋还能正常跑呢。我后来做数值微分梯度校验时才发现我写错了，然后改正了，然后就一直不明白为什么错了却能跑对...
4. 经过实验测试，我发现在图片识别这个问题中，交叉熵显著地优于MSE，为什么？

等等还有很多问题，但以上这三个是我实在困惑的，其他的我自己基本能逐渐搞懂

已全部解决

