# Calculations with error limits

Calculate with error limits:


```python
    from math import pi
    from error_limits import imprecise, Range

    @imprecise
    def calculate_area(r):
        return pi * r **2

    area = calculate_area(Range(0.52, 0.56))
    # [0.8494866535306802, 0.9852034561657592]
```

Another example:

```python
    @imprecise
    def calculate(a, b, c, d=1, e=0):
        return (a * sin(b + c)) ** d + e

    result = calculate(Range(2, 3), 4, 0, e=1)
    # [-1.2704074859237844, 0.4863950093841436]
```

## Tests

Run

    python tests/test.py
