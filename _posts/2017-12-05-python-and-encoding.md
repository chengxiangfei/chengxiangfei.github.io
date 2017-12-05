---
layout: post
category: "python"
title:  "python和编码"
tags: [python,encoding]
---

### Encoding declarations
Python脚本中，通常会在第一或第二行写上：
```
# -*- coding: <encoding-name> -*-
```
或者
```
# vim:fileencoding=<encoding-name>
```
这一行注释称为编码声明。编码声明必须放在第一行或第二行，如果在第二行，那么第一行必须也是注释行。

Python会用正则表达式`coding[=:]\s*([-\w.]+)`去匹配编码声明行，匹配到的编码名称会作为Python用来进行词法分析，字符串结尾的识别等。String会被解码为Unicode，然后进行语法分析，在对程序进行解释执行之前再转成原来的编码。因此，如果没有进行编码声明，而脚本中又出现了ASCII不能编码的字符，Python会报`SyntaxError: Non-ASCII character '\xe4' in file XXX on line 7, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details`之类的错误。

### Python2 的str 和 unicode 字符串

## str
Python2中str字符串是指直接用单引号、双引号或三引号括起来的字符串，默认采用编码声明中的编码方式编码字符串，如果没有指定编码声明，则采用ASCII。str的基本单位是一个字节，因此直接用`len()`方法得到不一定是字符串的长度，而是str占字节数。下面例子中，用的是gbk编码，字符`中`占两个字节。如果采用`UTF-8`编码，字符`中`则是3个字节。
```python
>>> len("中")
2
>>> len("中".decode("gbk").encode("UTF-8"))
3
>>> a = "python是最好的语言"
>>> print a [10]

>>>
>>> a[10]
'\xba'
```
同样地，直接用下标或者切片操作str，都不太可能得到正确的字符。


#### unicode
在字符串前面加`u`前缀，这样的字符串是unicode。unicode采用UTF-16编码。每个字符占两个（BMP）或四个字节（SP）。不论是BMP中的字符，或sp中的字符都能正确的识别。关于BMP和SP参看[String encoding](   )。unicode能够正确计算字符串的长度，也可以对unicode进行下标和切片操作。

```
>>> a = u"python是最好的语言"
>>> len(a)
12
>>> print a[11]
言
>>> print a[9:-1]
的语
```
### 内建函数ord

如果ord的输入参数为长度为1的unicode字符串，则返回一个代表该字符的Unicdode代码点（code point）的整数。如果输入是一个8bit的字符串，返回该字符的ASCII码。和内建函数`chr`，`unichr`（用于unicode）互逆。
```
>>> ord('a')
97
>>> ord(u'研')
30740
>>> chr(97)
'a'
>>> unichr(30740)
u'\u7814'
>>> print unichr(30740)
研
```

### sys模块中和编码有关的属性或方法

#### sys.maxunicode
一个整数表明python能够支持的最大的unicode代码点。如果python是32位，则sys.maxunicode=65535，对应于UCS-2; 如果python是64位，则sys.maxunicode=1114111， 对应于UCS-4。
但这并不代表unicode代码点大于65535的字符，32位不能处理。unicode使用UTF-16编码方式，unicode代码点大于65535的字符使用代理对表示。目前发现sys.maxunicode会影响unichr方法，其他的影响我暂时还没有发现，以后发现了再补充。

32位python的`unichr`方法能接受的最大参数为65535.
```
>>> import sys
>>> sys.maxunicode
65535
>>> unichr(6553)
u'\u1999'
>>> unichr(65536)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: unichr() arg not in range(0x10000) (narrow Python build)
```

64位python的`unichr`方法能接受的最大参数为1114111.
```
>>> import sys
>>> sys.maxunicode
1114111
>>> unichr(65536)
u'\U00010000'
>>> unichr(1114112)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: unichr() arg not in range(0x110000) (wide Python build)
```

#### sys.getdefaultencoding()
系统默认编码。Python2中，所有的平台都是ASCII，除非自己重新设置为其他的编码。比如'str'.encode()，没有指定编码时，就会采用默认编码。
#### sys.setdefaultencoding()
设置系统默认编码。不建议重写系统默认编码，可能会造成莫名的bug。

#### sys.getfilesystemencoding()
获取文件系统的编码。这个编码用来编码系统数据，比如文件名，命令行参数，环境变量等。

#### sys.stdin.encoding 和 sys.stdout.encoding

sys.stdin 和 sys.stdout 实际上是文件对象（File Object）。文件对象有个只读的属性encoding是改文件对象使用的编码。当写文件时，如果字符串是Unicode，会使用这个属性的值对Unicode字符串进行编码，进而写到文件中。这个属性的值有可能是None，这种情况下，会使用系统默认的编码方式来编码Unicode 字符串。

我们可以使用sys.stdin.encoding 和 sys.stdout.encoding 来查看解释器的标准输入和标准输出的格式，然后加以转换，避免出现乱码。sys.stdin.encoding 和 sys.stdout.encoding 的值和系统环境有关。

在windows系统中，Python解释器的标准输入、输出和错误流的编码。
```python
>>> sys.stdin.encoding
'cp936'
>>> sys.stdout.encoding
'cp936'
>>> sys.stderr.encoding
'cp936'
```

那么这几中编码都有哪些区别，用在哪些情况呢？stackoverflow上[这个](http://stackoverflow.com/questions/15530635/why-is-sys-getdefaultencoding-different-from-sys-stdout-encoding-and-how-does)答案讲解的很清晰。
>They serve different purposes.

>sys.stdout.encoding should be the encoding that your terminal uses to interpret text otherwise you may get mojibake in the output. It may be utf-8 in one environment, cp437 in another, etc.

>sys.getdefaultencoding() is used on Python 2 for implicit conversions (when the encoding is not set explicitly) i.e., Python 2 may mix ascii-only bytestrings and Unicode strings together e.g., xml.etree.ElementTree stores text in ascii range as bytestrings or json.dumps() returns an ascii-only bytestring instead of Unicode in Python 2 — perhaps due to performance — bytes were cheaper than Unicode for representing ascii characters. Implicit conversions are forbidden in Python 3.

>sys.getdefaultencoding() is always 'ascii' on all systems in Python 2 unless you override it that you should not do otherwise it may hide bugs and your data may be easily corrupted due to the implicit conversions using a possibly wrong encoding for the data.

>btw, there is another common encoding sys.getfilesystemencoding() that may be different from the two. sys.getfilesystemencoding() should be the encoding that is used to encode OS data (filenames, command-line arguments, environment variables).

>The source code encoding declared using # -*- coding: utf-8 -*- may be different from all of the already-mentioned encodings.

>Naturally, if you read data from a file, network; it may use character encodings different from the above e.g., if a file created in notepad is saved using Windows ANSI encoding such as cp1252 then on another system all the standard encodings can be different from it.

>The point being: there could be multiple encodings for reasons unrelated to Python and to avoid the headache, use Unicode to represent text: convert as soon as possible encoded text to Unicode on input, and encode it to bytes (possibly using a different encoding) as late as possible on output — this is so called the concept of Unicode sandwich.

