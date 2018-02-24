---
layout: post
category: "python"
title:  "pyspark 使用udf遇到的问题"
tags: [python, pyspark, udf]
---

在使用`PySpark`的`DataFrame`处理数据时，会遇到需要用自定义函数（user defined function, udf）对某一列或几列进行运算，生成新列的情况。`PySpark`的`udf`使用方法如下。

先初始化SparkContext和SparkSession

``` python
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession

spark_conf = SparkConf().setAppName("udf_example")
spark_context = SparkContext(conf=spark_conf)
spark = SparkSession.builder.config(conf=spark_conf).enableHiveSupport().getOrCreate()
```

使用装饰器的方法把一个python函数注册为udf

``` python
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import udf

# 使用装饰器把一个python函数注册为udf, 装饰器中的参数为返回的数据类型
@udf('int')
def slen(s):
    if s is not None:
        return len(s)

# 当装饰器不带任何参数时，默认的数据类型为str
@udf()
def to_upper(s):
    if s is not None:
        return s.upper()

# 也可以使用pyspark.sql.types作为装饰器的参数指定udf返回类型  
@udf(IntegerType())
def add_one(x):
    if x is not None:
        return x + 1

# 也可以先定义一个python函数，然后用udf注册
def add_two(x):
    if x is not None:
        return x + 2

add_tow_udf = udf(add_two, IntegerType())

# 创建一个DataFrame
df = spark.createDataFrame([(1, None, 21), (2, 'Lucy', 20)], ('id', 'name', 'age'))
# 使用udf
df.select(slen("name").alias("slen(name)"), to_upper("name"), add_one("age")).show()
# 增加一列
df2 = df.withColumn("ont_age", add_one("age"))
print(df2.head(2))

```
输出结果为：


| slen(name) | to_upper(name) | add_one(age) |
| ---------- | -------------- | ------------ |
|      null  |          null  |          22  |
|         4  |          LUCY  |          21  |
| ---------- | -------------- | ------------ |


有时候仅仅对DataFrame中的一列进行操作不能满足需求，udf需要有多个参数，这种情况也是可以处理的。 比如说我们做文本分类时通常会使用tf-idf作为特征，在计算idf时，就需要把文档总数和某个词出现的文档数传入到udf中。

``` python
from math import log
from pyspark.sql.types import FloatType
from pyspark.sql.functions import lit
def idf(D, Ti):
    """
    idf_i = log(D/Ti)
    :param D:  文档总数
    :param Ti:  包含词t_i 的文档数
    :return:
    """
    if Ti == 0:
        return 0.0
    return log(D *1.0 / Ti)

# 把idf注册为一个udf，返回值类型为float
compute_idf = udf(idf, FloatType())
# 文档数
document_count = 40
dataframe = spark.createDataFrame([("hello", 30), ("word", 10), ("example",15)], ("word", "num_count"))
# 需要使用 pyspark.sql.functions.lit 把 document_count 转为字面值, 
idf = dataframe.withColumn("idf", compute_idf(lit(document_count), "num_count"))
print(idf.head(2))
```
输出结果：

[Row(word=u'hello', num_count=30, idf=0.28768208622932434), Row(word=u'word', num_count=10, idf=1.3862943649291992)]

如果直接传入document_count到 计算idf的udf中的话，会引起method col([class java.lang.Integer]) does not exist 的错误。主要是因为PySpark把传入的参数都当做一列来处理，而我们的DataFrame中是不存在40这一列的。

``` python
idf = dataframe.withColumn("idf", compute_idf(document_count, "num_count"))

Py4JErrorTraceback (most recent call last)
<ipython-input-9-281e0b407efe> in <module>()

...

Py4JError: An error occurred while calling z:org.apache.spark.sql.functions.col. Trace:
py4j.Py4JException: Method col([class java.lang.Integer]) does not exist
	at py4j.reflection.ReflectionEngine.getMethod(ReflectionEngine.java:318)
	at py4j.reflection.ReflectionEngine.getMethod(ReflectionEngine.java:339)
	at py4j.Gateway.invoke(Gateway.java:274)
	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at py4j.commands.CallCommand.execute(CallCommand.java:79)
	at py4j.GatewayConnection.run(GatewayConnection.java:214)
	at java.lang.Thread.run(Thread.java:745)
```

也可以通过lit先把document_count这个字面值添加到DataFrame中成为新的一列，再使用udf计算idf。

``` python
new_dataframe = dataframe.withColumn("document_count", lit(document_count))
idf = new_dataframe.withColumn("idf", compute_idf("document_count", "num_count"))
print(idf.head(2))
```

输出结果：
[Row(word=u'hello', num_count=30, document_count=40, idf=0.28768208622932434), Row(word=u'word', num_count=10, document_count=40, idf=1.3862943649291992)]

DataFrame中多了两列document_count 和 idf。