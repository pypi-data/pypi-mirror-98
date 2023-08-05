# Description
binstore module with Bins C extension to implement storage of items based on value-based binning where binned value determines ordinal index into array where item is stored.   Supports item assignment and slice operations.

## Members
- min - float, minimum value 
- max - float, maximum value
- width - float, bin width 
- n_bins - int, number of bins = int((max - min) / width) + 1
 
## Methods
- bin(value) - perform binning operation on value and returns corresponding bin ordinal value 0 <= n <= n_bins - 1
- put(value, item) - puts item into bin n = bin(value) and returns n
- get(value) - gets item from bin n = bin(value) and returns as tuple of (item, n)
- items() - returns items in bins as dict with left bin edge as key, item in bin as value 

## When performing binning:
1. if value is <= min, bin(value) = 0
2. if value is >= max, bin(value) = n_bins - 1 
3. if value is >= half the distance between left edge of bin n and left edge of bin n+1, then corresponding bin(value) = n+1, otherwise bin(value) = n.  e.g., for min = 0.0, max = 1.0, width = 0.01, bin(0.106) = 11, bin(0.103) = 10.

## Example: 
\>>>b = Bins(min=0.0, max=1.0, width=0.01)
\>>>for i in range(50):
\>>>    b.put(i/100, {'i': i})
0
1
2
.
49
\>>>b.get(0.005)
({'i': 1}, 1)
\>>>b.get(0.000)
({'i': 0}, 0)
\>>>b.get(0.004)
({'i': 0}, 0)
\>>>b.get(0.103)
({'i': 10}, 10)
\>>>b.get(0.106)
({'i': 11}, 11)
\>>>b.put(0.106, {'foo': 'bar'})
11
\>>>b[11]
{'foo': 'bar'}
\>>>b[11] = {'bar': 'foo'}
\>>>b[11]
{'bar': 'foo'}
 
