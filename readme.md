# Apriori & FP-growth python实现


这两个算法实现是数据挖掘课程的作业，算法比较容易理解，于是尝试用python来写，运用frozenset还有一些集合运算技巧，最终运行效率还行。

Python版本：`3.6.4`

测试数据大概8.8万条，最小支持度设为0.01时，FP-growth用时0.8s，Apriori用时4.3s，FP-growth只需要对数据进行两次遍历，发现频繁项集的效率大大提高。
