import RLE
import unittest

class TestRLE(unittest.TestCase):
    """ Test class for RLE comression. """

    def test_compress_only_identical(self):
        """ Compress array that has only identical values """
        orig_array = [0, 0, 0]
        actual = RLE.compress(orig_array)
        expected = [129, 0]
        self.assertEqual(actual, expected)

    def test_compress_only_different(self):
        """ Compress array that has only different values """
        orig_array = [0, 1, 2]
        actual = RLE.compress(orig_array)
        expected = [2, 0, 1, 2]
        self.assertEqual(actual, expected)

    def test_compress_single_element(self):
        """ Compress array that has only different values """
        orig_array = [100]
        actual = RLE.compress(orig_array)
        expected = [0, 100]
        self.assertEqual(actual, expected)

    def test_compress_start_w_single(self):
        """ Compress array that starts with single and
        then has sequence of identical values """
        orig_array = [200, 0, 0]
        actual = RLE.compress(orig_array)
        expected = [0, 200, 128, 0]
        self.assertEqual(actual, expected)

    def test_compress_end_w_single(self):
        """ Compress array that ends with single and
        before it has sequence of identical values """
        orig_array = [129, 129, 129, 255]
        actual = RLE.compress(orig_array)
        expected = [129, 129, 0, 255]
        self.assertEqual(actual, expected)

    def test_compress_mixed_sequence_complex(self):
        """ Compress array from example """
        orig_array = [0, 0, 0, 0, 0, 0, 4, 2, 0, 4, 4, 4, 4, 4, 4, 4,
        80, 80, 80, 80, 0, 2, 2, 2, 2, 255, 255, 255, 255, 255, 0, 0]
        actual = RLE.compress(orig_array)
        expected = [132, 0, 2, 4, 2, 0, 133, 4, 130, 80, 0, 0, 130, 2, 131, 255, 128, 0]
        self.assertEqual(actual, expected)

    def test_compress_mixed_sequence1(self):
        """ Compress array that starts with the identical values and then has different values """
        orig_array = [255, 255, 0, 255, 0, 255]
        actual = RLE.compress(orig_array)
        expected = [128, 255, 3, 0, 255, 0, 255]
        self.assertEqual(actual, expected)

    def test_compress_mixed_sequence2(self):
        """ Compress array that starts different values and then has the identical values """
        orig_array = [1, 128, 128]
        actual = RLE.compress(orig_array)
        expected = [0, 1, 128, 128]
        self.assertEqual(actual, expected)

    def test_compress_mixed_sequence3(self):
        """ Compress array that starts with one sequence of identiacal elemets
        and then continues with another sequence of identiacal elemets """
        orig_array = [2, 2, 3, 3, 3]
        actual = RLE.compress(orig_array)
        expected = [128, 2, 129, 3]
        self.assertEqual(actual, expected)

    def test_compress_mixed_sequence4(self):
        """ Compress array that starts with one sequence of identiacal elemets
        then has single different element and
        then continues with another sequence of identiacal elemets """
        orig_array = [5, 5, 5, 5, 5, 0, 3, 3, 3]
        actual = RLE.compress(orig_array)
        expected = [131, 5, 0, 0, 129, 3]
        self.assertEqual(actual, expected)

    def test_compress_max_identical(self):
        """ Compress array that has max length (129 = 127 + 2) of identical elements
        and single element after sequence """
        orig_array = [0] * RLE.max_seq_same
        orig_array += [1]
        actual = RLE.compress(orig_array)
        expected = [255, 0, 0, 1]
        self.assertEqual(actual, expected)

    def test_compress_max_1_identical(self):
        """ Compress array that has max + 1 length (130) of identical elements
        Max sequence + single """
        orig_array = [0] * (RLE.max_seq_same + 1)
        actual = RLE.compress(orig_array)
        expected = [255, 0, 0, 0]
        self.assertEqual(actual, expected)

    def test_compress_max_2_identical(self):
        """ Compress array that has max + 2 length (131) of identical elements
        Max sequence + sequence """
        orig_array = [255] * (RLE.max_seq_same + 2)
        actual = RLE.compress(orig_array)
        expected = [255, 255, 128, 255]
        self.assertEqual(actual, expected)

    def test_compress_max_1_identical_and_single(self):
        """ Compress array that has max + 1 length (130) of identical elements
        and one single element after """
        orig_array = [128] * (RLE.max_seq_same + 1)
        orig_array += [1]
        actual = RLE.compress(orig_array)
        expected = [255, 128, 1, 128, 1]
        self.assertEqual(actual, expected)

    def test_compress_max_different(self):
        """ Compress array that has max sequence (128 = 127 + 1) of different elements
        and sequence of identical elemenets after """
        orig_array = list(range(0, RLE.max_seq_diff))
        orig_array += [1, 1, 1, 1]
        actual = RLE.compress(orig_array)
        expected = [127] + list(range(0, RLE.max_seq_diff)) + [130, 1]
        self.assertEqual(actual, expected)

    def test_compress_max_1_different(self):
        """ Compress array that has max + 1 sequence(129) of different elements """
        orig_array = list(range(0, RLE.max_seq_diff + 1))
        actual = RLE.compress(orig_array)
        expected = [127] + list(range(0, RLE.max_seq_diff)) + [0, 128]
        self.assertEqual(actual, expected)

    def test_compress_1_max_different_and_sequence(self):
        """ Compress array that has max - 1 sequence(127) of different elements
        and then starts sequence of the same elemenents """
        orig_array = list(range(0, RLE.max_seq_diff - 1))
        orig_array += [1, 1]
        actual = RLE.compress(orig_array)
        expected = [126] + list(range(0, RLE.max_seq_diff - 1)) + [128, 1]
        self.assertEqual(actual, expected)

    def test_decompress_seq_identical(self):
        """ Decompress array that has only identical elements """
        orig_array = [128, 128]
        actual = RLE.decompress(orig_array)
        expected = [128, 128]
        self.assertEqual(actual, expected)

    def test_decompress_seq_diff(self):
        """ Decompress array that has only different elements """
        orig_array = [1, 0, 1]
        actual = RLE.decompress(orig_array)
        expected = [0, 1]
        self.assertEqual(actual, expected)

    def test_decompress_1(self):
        """ Decompress array that has only 1 element """
        orig_array = [0, 255]
        actual = RLE.decompress(orig_array)
        expected = [255]
        self.assertEqual(actual, expected)

    def test_decompress_max_identical(self):
        """ Decompress array that has max sequence of identical elements """
        orig_array = [255, 255]
        actual = RLE.decompress(orig_array)
        expected = [255] * RLE.max_seq_same
        self.assertEqual(actual, expected)

    def test_decompress_max_diff(self):
        """ Decompress array that has max sequence of different elements """
        orig_array = [127] + list(range(100, RLE.max_seq_diff + 100))
        actual = RLE.decompress(orig_array)
        expected = list(range(100, RLE.max_seq_diff + 100))
        self.assertEqual(actual, expected)

    def test_decompress_mixed_sequence_complex(self):
        """ Decompress array from example """
        orig_array = [132, 0, 2, 4, 2, 0, 133, 4, 130, 80, 0, 0, 130, 2, 131, 255, 128, 0]
        actual = RLE.decompress(orig_array)
        expected = [0, 0, 0, 0, 0, 0, 4, 2, 0, 4, 4, 4, 4, 4, 4, 4,
        80, 80, 80, 80, 0, 2, 2, 2, 2, 255, 255, 255, 255, 255, 0, 0]
        self.assertEqual(actual, expected)

    def test_decompress_mixed_sequence1(self):
        """ Decompress array that stars with seq of identical elements
        then has sequnce of different element """
        orig_array = [128, 255, 3, 0, 255, 0, 255]
        actual = RLE.decompress(orig_array)
        expected = [255, 255, 0, 255, 0, 255]
        self.assertEqual(actual, expected)

    def test_decompress_mixed_sequence2(self):
        """ Decompress array that starts with seq of different elements
        and then has sequnce of identical elements """
        orig_array = [0, 1, 128, 128]
        actual = RLE.decompress(orig_array)
        expected = [1, 128, 128]
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
