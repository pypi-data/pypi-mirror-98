from operator import itemgetter
from collections import OrderedDict
from functools import reduce

__all__=['LinkedTuple']

class LinkedTuple(tuple):
	'LinkedTuple(head, tail)'

	__slots__ = ()

	def __new__(_cls, head, tail=None):
		'Create new instance of LinkedTuple(head, tail)'
		assert(tail is None or isinstance(tail,LinkedTuple))
		return tuple.__new__(_cls, (head, tail))

	@classmethod
	def make(cls, iterable, new=tuple.__new__):
		'Make a new LinkedTuple chain from a sequence or iterable'
		return reduce(lambda tl, hd: new(cls, (hd,tl)), iterable, None)

	def __iter__(self):
		'Get an iterable for the LinkedTuple chain'
		yield self[0]
		t = self[1]
		while t is not None:
			yield t[0]
			t = t[1]

	def reversed(self):
		'Creates and returns a new LinkedTuple with the items in reverse order'
		n = None
		q = self

		while q: 
			n = LinkedTuple(q.head, n)
			q = q.tail

		return n

	def plus(self, new_head):
		'Creates and returns a new LinkedTuple with a new head and self as tail'
		return self.__class__(new_head, self)

	def __repr__(self):
		'Return a nicely formatted representation string'
		return self.__class__.__name__ + '(head=%r, tail=%r)' % self

	def __str__(self):
		'Return a nicely formatted representation string'
		return '(%s,%s)' % self

	def __len__(self): 
		'Counts the number of elements in a LinkedTuple (this is slow)'
		n = self
		c = 0
		while n is not None: 
			c+=1
			n = n.tail
		return c

	@property
	def __dict__(self):
		'Return a new dict mapping field names to their values'
		d = OrderedDict()
		d['head']=self[0]
		d['tail']=self[1]
		return OrderedDict(d)

	def __getnewargs__(self):
		'Return self as a plain tuple.  Used by copy and pickle.'
		return tuple(self)

	def __getstate__(self):
		'Exclude the OrderedDict from pickling'
		return None

	head = property(itemgetter(0), doc='Head')

	tail = property(itemgetter(1), doc='Tail')

