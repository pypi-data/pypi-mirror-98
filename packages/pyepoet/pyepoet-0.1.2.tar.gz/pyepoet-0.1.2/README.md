# PyEPoet 0.1.2

## 介绍

刘慈欣电子诗人Python版

## 安装

```python
(python -m) pip install pyepoet
```

## 函数

```python
#生成一首诗，并输出到file
genpoem(verse = 5, line = 10, rhyme = None, file = sys.stdout)
#生成一首诗，并返回一个字符串
gpoem_string(verse = 5, line = 10, rhyme = None)
```

## 速度

押韵：约45000行/秒

不押韵：约1100行/秒

## 示例

```python
from pyepoet import *
genpoem()
print()
genpoem(rhyme = "a")
print()
print(gpoem_string())
```

## 更新历史

### 版本0.1.2 (2021/2/11)

- 初始版本