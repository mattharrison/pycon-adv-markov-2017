from collections import Counter
import unittest

import markov as mar

class TestMarkov(unittest.TestCase):
    def test_char_iter(self):
        lines = ['abc', 'def']
        c = mar.CharIter(lines)
        res = list(c)
        self.assertEqual(res, ['a', 'b', 'c', 'd', 'e', 'f'])

    def test_char_gen(self):
        lines = ['abc', 'def']
        c = mar.char_gen(lines)
        res = list(c)
        self.assertEqual(res, ['a', 'b', 'c', 'd', 'e', 'f'])

    def test_word_gen(self):
        lines = ['hello world', 'bye matt']
        w = mar.word_gen(lines)
        res = list(w)
        self.assertEqual(res, ['hello', 'world', 'bye', 'matt'])

    def test_window(self):
        lines = ['hello world', 'bye matt']
        w = mar.word_gen(lines)
        win = mar.window_gen(w, 2)
        res = list(win)
        self.assertEqual(res,
                         [['hello', 'world'], ['world', 'bye'], ['bye', 'matt']]
                         )
        
    def test_cmarkov(self):
        lines = ['abc', 'def']
        m = mar.CharMarkov(lines, 3)
        self.assertEqual(m.tables, [{'a': Counter({'b': 1}), 'b': Counter({'c': 1}), 'c': Counter({'d': 1})}, {'ab': Counter({'c': 1}), 'bc': Counter({'d': 1}), 'cd': Counter({'e': 1})}, {'abc': Counter({'d': 1}), 'bcd': Counter({'e': 1}), 'cde': Counter({'f': 1})}])
        
        
    def test_get_table(self):
        lines = ['abc', 'def']
        t = mar.get_table(mar.char_gen(lines))
        self.assertEqual(t, {'a': {'b': 1}, 'b': {'c': 1}, 'c': {'d': 1}, 'd': {'e': 1}, 'e': {'f': 1}})

           
if __name__ == '__main__':
    unittest.main()
