import pickle

from actionpack.actions import Chunk
from actionpack.utils import Container
from actionpack.utils import pickleable
from actionpack.utils import tally

from oslash import Left
from oslash import Right
from unittest import TestCase


class ChunkTest(TestCase):

    def setUp(self):
        #self.chunk_provider = lambda iterlen, chunksize: Chunk(Container.lining((1 for _ in range(iterlen))), chunksize)
        self.chunk_provider = lambda iterlen, chunksize: Chunk(Container(1 for _ in range(iterlen)), chunksize)

    def test_can_Chunk_iterator_into_modulus_sized_chunks(self):
        iterlen, chunksize = 100, 5
        chunking = self.chunk_provider(iterlen, chunksize)
        result = chunking.perform()

        chunkcount = 0
        for chunk in result.value:
            chunkcount += 1
            self.assertEqual(len(list(chunk)), chunksize)
        self.assertEqual(chunkcount, iterlen / chunksize)

    def test_can_Chunk_iterator_with_remainder(self):
        iterlen, chunksize = 10, 4
        chunking = self.chunk_provider(iterlen, chunksize)
        result = chunking.perform()

        chunkcount = 0
        for chunk in result.value:
            chunkcount += 1
            if chunkcount > iterlen // 4:
                self.assertEqual(len(list(chunk)), iterlen % chunksize)
            else:
                self.assertEqual(len(list(chunk)), chunksize)
        self.assertEqual(chunkcount, 3)

    def test_can_Chunk_iterator_shorter_than_chunk_size(self):
        iterlen, chunksize = 5, 10
        chunking = self.chunk_provider(iterlen, chunksize)
        result = chunking.perform()

        chunkcount = 0
        for chunk in result.value:
            chunkcount += 1
            self.assertEqual(len(list(chunk)), iterlen)
        self.assertEqual(chunkcount, 1)

    def test_can_pickle(self):
        action = self.chunk_provider(100, 5)
        pickled = pickleable(action)
        unpickled = pickle.loads(pickled)

        self.assertTrue(pickleable(action))
        self.assertEqual(str(unpickled.__dict__), str(action.__dict__))

