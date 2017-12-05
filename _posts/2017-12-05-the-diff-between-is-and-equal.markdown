---
layout: post
category: "python"
title:  "is和==的区别"
tags: [python]
---

# is 和 == 的区别

我们先来看一段代码
```
>>> a = 1
>>> b = 1
>>> a == b
True
>>> a is b
True

>>> c = 1000
>>> d = 1000
>>> c == d
True
>>> c is d
False

```

会不会觉得很奇怪，在上面的代码中 `a==b`, `c==d` 的值都是`True`，这在我们的预料之中，
那为啥`a is b` 和 `c is d` 这两个表达式的值不同呢？
要回答这个问题，我们首先来看一下`Python`的数据模型（data model）。 

### 数据模型
在`Python`中，一切都是对象，即使是内建类型和函数也是对象。每一个对象有一个标识符(identity), 
一个类型(type)和一个值(value)。
对象的identity一旦被建立，就不会被改变了，现阶段（Python2）可以认为identity 就是这个对象在内存中的地址。
`Python`的内建函数`id()`返回一个整数代表对象的identity（现阶段`id()`的实现就是对象的地址）。
一个对象的type也是不可改变的。type决定了对象支持哪些方法，也定义了这个对象可以接受哪些值。
我们可以用内建函数`type()`返回一个对象的type。
有些对象的值是可以改变的，这些对象称之为mutable，比如`dict`，`list`等；有些对象的值是不可变的，这些对象称之为immutable，
比如`str`，`int`， `tuple`等。

### `is` 和 `==` 比较的是啥？
了解了`Python`的数据模型，现在我们可以来说说，`is`和`==`比较的是啥了。

##### `==`
python2 的官方文档上有说明，操作符  `<`, `>`, `==`, `>=`, `<=`, and `!=` 比较两个对象的值。
比较的对象必须是同一种类型。如果两个对象不是同一种类型，那比较结果总是不想等的。


相同类型的对象之间的比较行为取决于对象的type：
* 数字（Numbers）就是数学意义上的比较。
* 字符串（Strings）： 先用内建函数`ord()`计算出每个字符的数字结果，然后再进行比较。
对于ascii表中的字符，`str`和`unicode`能得出一样的结果，如：
```
>>> 'abc' == u'abc'
True
```
然而对于超出ascii的字符就不一样了，
```
>>> '中国' == u'中国'
False
```
不一样的原因，和编码的问题有关系，这块没有仔细研究过，先不说了。
* 元祖(tuples)和列表(lists)按顺序一一比较内部的元素。如果两个元祖（列表）相等，意味着
元祖（列表）中的每个元素都相等，并且这俩元祖（列表）的长度也想等。
* Mapping（dictionaries）， 两个Mapping对象相等，除非他们的sorted（key, value）list 相等。
* 许多其他的内建类型只有是同一个对象的时候才相等。
##### `is`
`is` 比较的是对象的标识符即`identity`。 只有`a` 和 `b` 是同一个对象的不同引用时，`a is b`才是`True`。
`is not`相反。

说到这里，再回头去看开头的代码，`a` 和 `b` 的值相等，`c` 和 `d` 的值相等，所以 `a==b`和`c==b`都是`True`。
等等，那`a` 和 `b` 为啥是同一个对象，`c` 和 `d`为啥又不是同一个对象啦？ 别急，这里还有一个概念要说。。。

### 字符串驻留(Stirng Interning)
[String Intering] (https://en.wikipedia.org/wiki/String_interning) 在维基百科上是这样解释的：
> In computer science, string interning is a method of storing only one copy of each distinct string value,
 which must be immutable. Interning strings makes some string processing tasks more 
 time- or space-efficient at the cost of requiring more time when the string is created 
 or interned. The distinct values are stored in a string intern pool.
 
 
翻译过来就是说每个不同的字符串只保存一份在字符串驻留池（string intern pool）中，这些字符串都是不可变的。
字符串驻留技术使得字符串在创建或驻留时需要等多的时间或空间。字符串驻留技术能够使字符串的比较工作更快。具体的技术实现和优点
在这里就不多说了啊，大家有兴趣的自己去查资料（其实是我也没看呢）。
很多面向对象的语言，Python，PHP，lua，Java等都实现了字符串驻留。
这样我们就可以明白，当我们写下
```
>>> s1 = 'abcde'
>>> s2 = 'abcde'
```
这两行代码时，我们实际上只创建了一个字符串对象，`s1` 和 `s2`都是对这个对象的引用，所以`s1 is s2`的值是`True`。
```
>>> s1 is s2
True
```
但并不是所有的字符串都会被驻留，只有一些简单并常见的字符串才会被驻留，像下面这个随意在键盘上敲出来的字符串，就没有被驻留。
`s3`和`s4`是两个不同的对象。
```
>>> s3 = 'hdkghiddfdlkg;seod'
>>> s4 = 'hdkghiddfdlkg;seod'
>>> s3 is s4
False
>>> s3 == s4
True
```

除了字符串，其他的对象也可以应用驻留技术。维基百科上有这样一句话：
> Objects other than strings can be interned. 
For example, in Java, when primitive values are boxed into a wrapper object, 
certain values (any boolean, any byte, any char from 0 to 127, and any short or int between −128 and 127) are interned, 
and any two boxing conversions of one of these values are guaranteed to result in the same object.


大意是说java的基本类型被包装为相应的对象的同时，会把这个值也保留在驻留池中。对同一个值的两次装箱过程会是同一个对象（是这么说的吗？）。

在`Python`的[文档](https://docs.python.org/2/reference/datamodel.html#objects-values-and-types)中也说，对于不可变类型（immutable types）产生新值的操作实际上会返回一个引用，
这个引用会指向一个已经存在的类型（type）和值（value）都和我们的结果一样。因此在开头的代码中`a` 和 `b`并不是产生了两个不同的对象，
而是同一对象的两个引用。虽然目前我看到的文档中并没有说明，Python采用的是何种技术，我猜测可能是驻留技术。
对于较小的整数，`Python`会返回驻留池中对象的一个引用，而对于较大的整数，
不在`Python`的驻留池中，则直接创建对象。因此，开头的代码中`c`和`d`是两个不同的对象，在内存中的地址不一样，`c is d`当然是`False`了。
这个结论对于数学计算除来的部分结果也适用：
```
>>> a = 19
>>> b = 1020-1001
>>> a is b
True
```
但不是所有的情况都适用：
```
>>> s1 = '123'
>>> s2 = '123'
>>> s1 is s2
True
>>> s3 = ''.join(['1', '2', '3'])
>>> s1 is s3
False
>>> s1 == s3
True
```

至于驻留的范围，我还没有找到，如果找到，在更新吧。

说了这么多，还是如果要比较对象是不是同一个对象那就用`is`， 如果要比较对象值是否相等，那就用`==`。
