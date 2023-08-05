
<img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=604800" />
<a href="https://github.com/Gato-X/python-LinkedTuple/blob/main/LICENSE" target="_blank"><img alt="License:MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>

</p>

A **LinkedTuple** is a read-only structure of linked (nested) tuples much like lists in functional languages.

Instances have a head element that can be anything and a tail element that can be either another LinkedTuple or None. 

Being a nested container of elements, a LinkedTuple is less efficient than a list or a plain tuple, but its main advantage is that it allows branching. That is, a tail can be shared by more than one LinkedTuple




## Install using pip
```
pip install linkedtuple
```

## Class

- **LinkedTuple(head[,tail])**

	Returns a new LinkedTuple instance with the provided head and possibly a tail

	
## Properties

- **head**

	read only head 
	
- **tail**

	read only tail 
	
	
## Methods

- **make(iterable)** [classmethod]

	Returns a new LinkedTuple chain with the elements taken from the iterable

- **plus(element)**

	Returns a new LinkedTuple with _element_ as head and the current ListTuple as tail

- **reversed()**

	Returns a new LinkedTuple with the items in reverse order

## Examples


We can create a LinkedTuple with a single element

	>>> from linkedtuple import LinkedTuple

	>>> LinkedTuple('x')
	LinkedTuple(head='x', tail=None)


Or from an iterable.

```
>>> ltup = LinkedTuple.make([1,2,3,4])

>>> ltup
LinkedTuple(head=4, tail=LinkedTuple(head=3, tail=LinkedTuple(head=2, tail=LinkedTuple(head=1, tail=None))))
```

Note the elements are present in reverse order.
	
So far, we've shown LinkedTuples as represented when calling repr() on them. When casting to string we get a more compact representation.

```
>>> repr(ltup)
'LinkedTuple(head=4, tail=LinkedTuple(head=3, tail=LinkedTuple(head=2, tail=LinkedTuple(head=1, tail=None))))'

>>> str(ltup)
'(4,(3,(2,(1,None))))'
```

LinkedTuples have a few available read-only properties, the most important ones are _head_ and _tail_.

```
>>> ltup.head
4

>>> ltup.tail
LinkedTuple(head=3, tail=LinkedTuple(head=2, tail=LinkedTuple(head=1, tail=None)))
```

Passing an iterable as a single element to LinkedTuple won't expand the iterable and will result in a LinkedTuple with the iterable as head and no tail.
```
>>> LinkedTuple([1,2,3,4])
LinkedTuple(head=[1, 2, 3, 4], tail=None)
```

We can create a new LinkedTuple from an existing one plus a new element.

```
>>> str(ltup.plus('X'))
'(X,(4,(3,(2,(1,None)))))'
```

The previous one doesn't (and can't) change. LinkedTuples are immutable.
```	
>>> str(ltup)
'(4,(3,(2,(1,None))))'

>>> ltup.head = 8
Traceback (most recent call last):
	File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
```

We can ask for the number of elements in a LinkedTuple, however this is slow because all the chain has to be traversed to count them.

```
>>> print(len(ltup))
4
```
		
LinkedTuples are iterables themselves, so we can do things like the following:
```
>>> list(ltup)
[4, 3, 2, 1]

>>> for item in ltup:
...     print(item)
... 
4
3
2
1
```
	
We can generate a new LinkedTuple from another LinkedTuple with the elements reversed

```
>>> str(ltup)
'(4,(3,(2,(1,None))))'

>>> str(ltup.reversed())
'(1,(2,(3,(4,None))))'
```


## Contact

* Me on GitHub [Gato-X](https://github.com/Gato-X)
* Project [page](https://github.com/Gato-X/python-LinkedTuple) on GitHub
* If you find any issues, please let me know [here](https://github.com/Gato-X/python-LinkedTuple/issues)

