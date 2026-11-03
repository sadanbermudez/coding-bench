import sys, os, unittest; sys.path.insert(0, os.getcwd())

import asyncio
from retry import retry
class T(unittest.TestCase):
    def run_(self, c):
        return asyncio.run(c)
    def test_success_after_failures(self):
        waits, calls = [], []
        async def fake_sleep(s): waits.append(s)
        @retry(attempts=4, base_delay=1, factor=3, retry_on=(ConnectionError,), sleep=fake_sleep)
        async def f(x):
            '''doc'''
            calls.append(x)
            if len(calls) < 3: raise ConnectionError("down")
            return x * 2
        self.assertEqual(self.run_(f(21)), 42)
        self.assertEqual(waits, [1, 3]); self.assertEqual(f.__name__, "f"); self.assertEqual(f.__doc__, "doc")
    def test_gives_up(self):
        waits = []
        async def fake_sleep(s): waits.append(s)
        @retry(attempts=3, base_delay=0.5, sleep=fake_sleep)
        async def g():
            raise TimeoutError("t")
        with self.assertRaises(TimeoutError):
            self.run_(g())
        self.assertEqual(waits, [0.5, 1.0])
    def test_not_retried(self):
        waits = []
        async def fake_sleep(s): waits.append(s)
        @retry(retry_on=(ConnectionError,), sleep=fake_sleep)
        async def h():
            raise KeyError("k")
        with self.assertRaises(KeyError):
            self.run_(h())
        self.assertEqual(waits, [])
    def test_bad(self):
        with self.assertRaises(ValueError):
            retry(attempts=0)

if __name__ == "__main__":
    unittest.main()
