"""
This is a docstring. Here is an example
of running a Markov prediction:

>>> m = Markov('ab')
>>> m.predict('a')
'b'

>>> m.predict('c')
Traceback (most recent call last):
  ...
KeyError

>>> get_table('ab')
{'a': {'b': 1}}

>>> random.seed(42)
>>> m = Markov('Find a city, find yourself a city to live in', 4)
>>> test_predict(m, 20, 'F', 4)
'Find a city, find a c'

>>> with open('ts.txt', encoding='windows_1252') as fin:
...     data = fin.read()
>>> m2 = Markov(data, 4)
>>> test_predict(m2, 100, 'T', 4)
"""

import argparse
from collections import Counter
import functools
import random
import sys
import time

class CharIter:
    def __init__(self, lines):
        self.data = iter(lines)
        self.line = None
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        while 1:
            if self.line is None:
                self.line = next(self.data)
            try:
                char = self.line[self.pos]
            except IndexError:
                self.line = next(self.data)
                self.pos = 0
            else:
                self.pos += 1
                return char

def noisy(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        # before
        print("Before")
        res = f(*args, **kwargs)
        # after
        print("After")
        return res
    return inner

def timer(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        # before
        start = time.time()
        res = f(*args, **kwargs)
        # after
        print("Took {} seconds".format(
            time.time()-start))
        return res
    return inner

def cheat(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        return 42
    return inner


@timer
def sleep(x):
    time.sleep(x)
              
@noisy
def adder(x, y):
    return x + y

#adder = noisy(adder)

def char_gen(lines):
    """ This is a generator """
    for line in lines:
        for c in line:
            yield c

def word_gen(lines):
    for line in lines:
        for word in line.split():
            yield word

def window_gen(data, size):
    win = []
    for thing in data:
        win.append(thing)
        if len(win) == size:
            yield win
            win = win[1:]
    

def blastoff():
    print("Hi")
    yield 1
    print("after 1")
    yield 2
    print("Goodbye")
          

def just_name(klass):
    def name(self):
        return '{}'.format(
            self.__class__.__name__)
    klass.__str__ = name
    return klass
    
@just_name
class Markov:
    def __init__(self, data, size=1):
        self.tables = []
        for i in range(size):
            self.tables.append(get_table(data, i+1))
        #self.table = get_table(data)

    def predict(self, data_in):
        table = self.tables[len(data_in) - 1]
        options = table.get(data_in, {})
        if not options:
            raise KeyError()
        possible = ''
        for result, count in options.items():
            possible += result*count
        result = random.choice(possible)
        return result


class WordMarkov(Markov):
    def __init__(self, lines, size=1):
        data = word_gen(lines)
        self.tables = get_tables(data, size)
 

class CharMarkov(Markov):
    def __init__(self, lines, size=1):
        data = char_gen(lines)
        self.tables = get_tables(data, size)
 

def get_tables(data, size=1, join_char=''):
    tables = []
    for tokens in window_gen(data, size+1):
        for i in range(size):
            try:
                table = tables[i]
            except IndexError:
                tables.append({})
                table = tables[i]
            key = join_char.join(tokens[:i+1])
            try:
                result = tokens[i+1]
            except IndexError:
                continue
            counts = table.setdefault(key, Counter())
            counts[result] += 1
    return tables
                

    
def get_table(data, size=1, join_char=''):
    results = {}
    for tokens in window_gen(data, size+1):
        item = join_char.join(tokens[:size])
        try:  # if i == len(line): # Look before you leap
            output = tokens[size]
        except IndexError:
            # easier to ask for forgiveness than permission
            break
        inner_dict = results.get(item, {})
        inner_dict.setdefault(output, 0)
        inner_dict[output] += 1
        results[item] = inner_dict
    return results

def test_predict(m, num_chars, start, size=1):
    res = [start]
    for i in range(num_chars):
        let = m.predict(start)
        res.append(let)
        start = ''.join(res)[-size:]
    return ''.join(res)

def repl(m, size=1):
    """
    This starts a repl, provide a Markov and
    optional size
    """
    while 1:
        txt = input(">")
        try:
            res = m.predict(txt[-size:])
        except KeyError:
            print("Try again...")
        print(res)

def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file', help='Input file')
    p.add_argument('--encoding', help='File encoding default(utf8)',
                   default='utf8')
    p.add_argument('-s', '--size', help='Size of input default(1)',
                   default=1, type=int)
    p.add_argument('-t', '--test', help='run tests', action='store_true')

    opts = p.parse_args(args)
    if opts.file:
        with open(opts.file, encoding=opts.encoding) as fin:
            data = fin.read()
        m = Markov(data, opts.size)
        repl(m)
    if opts.test:
        import doctest
        doctest.testmod()
    

if __name__ == '__main__':
    print("EXECUTED")
    #import doctest
    #doctest.testmod()
    main(sys.argv[1:])
else:
    print("IMPORTED")


