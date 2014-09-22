import LZ77
import unittest

class TestLZ77(unittest.TestCase):
    """ Test class for LZ77 comression. """

    def test_find_sequence_pos1(self):
        text = 'abab'
        actual = LZ77.find_best_subsequence(text, 2)
        expected = 'ab'
        self.assertEqual(actual, expected)

    def test_find_sequence_pos2(self):
        text = 'ababa'
        actual = LZ77.find_best_subsequence(text, 2)
        expected = 'ab'
        self.assertEqual(actual, expected)

    def test_find_sequence_pos3(self):
        text = 'abbbabb'
        actual = LZ77.find_best_subsequence(text, 4)
        expected = 'abb'
        self.assertEqual(actual, expected)

    def test_find_sequence_pos4(self):
        text = 'ababbb'
        actual = LZ77.find_best_subsequence(text, 2)
        expected = 'ab'
        self.assertEqual(actual, expected)

    def test_find_sequence_best(self):
        text = 'abcabcdeabcd'
        actual = LZ77.find_best_subsequence(text, 8)
        expected = 'abcd'
        self.assertEqual(actual, expected)

    def test_find_sequence_neg1(self):
        text = 'abaabb'
        actual = LZ77.find_best_subsequence(text, 2)
        expected = ''
        self.assertEqual(actual, expected)

    def test_find_sequence_neg2(self):
        text = 'aabbxbb'
        actual = LZ77.find_best_subsequence(text, 2)
        expected = ''
        self.assertEqual(actual, expected)

    def test_find_sequence_max(self):
        a_int = ord('a')
        seq = ''.join(map(chr, range(a_int, a_int + LZ77.max_seq)))
        text = seq * 2
        actual = LZ77.find_best_subsequence(text, len(seq))
        expected = seq
        self.assertEqual(actual, expected)

    def test_find_sequence_max_1(self):
        a_int = ord('a')
        seq = ''.join(map(chr, range(a_int, a_int + LZ77.max_seq + 1)))
        text = seq * 2
        actual = LZ77.find_best_subsequence(text, len(seq))
        expected = seq[:LZ77.max_seq]
        self.assertEqual(actual, expected)

    def test_find_sequence_max_pos(self):
        text = 'abc' + ('d' * (LZ77.max_block - 3)) + 'abc'
        actual = LZ77.find_best_subsequence(text, LZ77.max_block)
        expected = 'abc'
        self.assertEqual(actual, expected)

    def test_find_sequence_max_1_pos(self):
        text = 'abc' + ('d' * (LZ77.max_block - 2)) + 'abc'
        actual = LZ77.find_best_subsequence(text, LZ77.max_block + 1)
        expected = ''
        self.assertEqual(actual, expected)

#######################

    def test_compress_1_char(self):
        """ Compress string of 1 char """
        text = 'a'
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(b'a')
        self.assertEqual(actual, expected)

    def test_compress_seq_diff_8_char(self):
        """ Compress string of 8 char (full 1 service byte) """
        text = '12345678'
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(b'12345678')
        self.assertEqual(actual, expected)

    def test_compress_seq_diff_9_char(self):
        """ Compress string of 9 char (2 service bytes) """
        text = '123456789'
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(b'12345678') \
                   + bytearray([0]) + bytearray(b'9')
        self.assertEqual(actual, expected)

    def test_compress_2_idenctical_char(self):
        """ Compress string of 2 identical char """
        text = 'aa'
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(b'aa')
        self.assertEqual(actual, expected)

    def test_compress_4_idenctical_char(self):
        """ Compress string of 4 identical char """
        text = 'bbbb'
        actual = LZ77.compress(text)
        expected = bytearray([32]) + bytearray(b'bb') + bytearray([0, 16])
        self.assertEqual(actual, expected)

    @unittest.skip("algorith improvement is needed")
    def test_compress(self):
        """ Compress string from example """
        text = 'The compression and the decompression leavq an impression. Hahahahaha!'
        actual = LZ77.compress(text)
        expected = bytearray([0, 84, 104, 101, 32, 99, 111, 109, 112, 0, 114, 101, 115, 115,
                    105, 111, 110, 32, 4, 97, 110, 100, 32, 116, 1, 49, 100, 101,
                    130, 1, 90, 108, 101, 97, 118, 101, 1, 117, 32, 65, 105, 2,
                    151, 46, 32, 72, 97, 104, 0, 21, 0, 33])
        print(expected)
        print(actual)
        self.assertEqual(actual, expected)

    def test_compress_1(self):
        """ Compress string of type: seq1_char_se1 """
        text = 'abcdabc'
        actual = LZ77.compress(text)
        expected = bytearray([8]) + bytearray(b'abcd') + bytearray([0, 49])
        self.assertEqual(actual, expected)

    def test_compress_2(self):
        """ Compress string of seq1_seq2_seq2_seq_1 """
        text = 'abcdefdeabc'
        actual = LZ77.compress(text)
        expected = bytearray([3]) + bytearray(b'abcdef')\
                   + bytearray([0, 32]) + bytearray([0, 113])
        self.assertEqual(actual, expected)

    def test_compress_3(self):
        """ Compress string of seq1_seq2_seq_1:
        service byte: 00000001"""
        text = 'abcdefgabcde'
        actual = LZ77.compress(text)
        expected = bytearray([1]) + bytearray(b'abcdefg') + bytearray([0, 99])
        self.assertEqual(actual, expected)

    def test_compress_4(self):
        """ Compress string of seq1_seq2_seq_2:
        service bytes: 00000000, 10000000 """
        text = 'abcdefghcdefgh'
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(b'abcdefgh')\
                   + bytearray([128]) + bytearray([0, 84])
        self.assertEqual(actual, expected)

    def test_compress_5(self):
        """ Compress string of seq1_seq11_seq_12:
        where seq11, seq12 are in seq1 """
        text = 'abcdefcdeab'
        actual = LZ77.compress(text)
        expected = bytearray([3]) + bytearray(b'abcdef')\
                   + bytearray([0, 49]) + bytearray([0, 128])
        self.assertEqual(actual, expected)

    def test_compress_max_seq_len(self):
        """ Compress string that has repeated sequence of max len (17) """
        a_int = ord('a')
        seq = ''.join(map(chr, range(a_int, a_int + LZ77.max_seq)))
        text = '123' + seq + '345' + seq
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(text[:8], 'utf-8')\
                   + bytearray([0]) + bytearray(text[8: 16], 'utf-8')\
                   + bytearray([1]) + bytearray(text[16: 23], 'utf-8')\
                   + bytearray([1, 63])
        self.assertEqual(actual, expected)

    def test_compress_max_1_seq_len(self):
        """ Compress string that has repeated sequence of max+1 len (18) """
        a_int = ord('a')
        seq = ''.join(map(chr, range(a_int, a_int + LZ77.max_seq + 1)))
        text = seq + '12' + seq + '1234'
        actual = LZ77.compress(text)
        expected = bytearray([0]) + bytearray(text[:8], 'utf-8')\
                   + bytearray([0]) + bytearray(text[8: 16], 'utf-8')\
                   + bytearray([12]) + bytearray(text[16: 20], 'utf-8')\
                   + bytearray([1, 63]) + bytearray([1, 49])\
                   + bytearray('34', 'utf-8')
        self.assertEqual(actual, expected)

    def test_compress_offset_less_len(self):
        """ Compress string that has repeated sequences where offset
        is less then sequence lenth """
        text = 'ababab'
        actual = LZ77.compress(text)
        expected = bytearray([32]) + bytearray(b'ab') + bytearray([0, 18])
        self.assertEqual(actual, expected)

#################

    def test_decompress_1_char(self):
        """ Decompress string of 1 char """
        b_array = bytearray([0]) + bytearray(b'a')
        actual = LZ77.decompress(b_array)
        expected = 'a'
        self.assertEqual(actual, expected)

    def test_decompress_seq_diff_8_char(self):
        """ Decompress string of 8 char (full 1 service byte) """
        b_array = bytearray([0]) + bytearray(b'12345678')
        actual = LZ77.decompress(b_array)
        expected = '12345678'
        self.assertEqual(actual, expected)

    def test_decompress_seq_diff_9_char(self):
        """ Decompress string of 9 char (2 service bytes) """
        b_array = bytearray([0]) + bytearray(b'12345678') \
                   + bytearray([0]) + bytearray(b'9')
        actual = LZ77.decompress(b_array)
        expected = '123456789'
        self.assertEqual(actual, expected)

    def test_decompress_1(self):
        """ Decompress string that has repeated sequence """
        b_array = bytearray([8]) + bytearray(b'abcd') + bytearray([0, 49])
        actual = LZ77.decompress(b_array)
        expected = 'abcdabc'
        self.assertEqual(actual, expected)

    def test_decompress_2(self):
        """ Decompress string that has 2 repeated sequences """
        b_array = bytearray([3]) + bytearray(b'abcdef')\
                   + bytearray([0, 32]) + bytearray([0, 113])
        actual = LZ77.decompress(b_array)
        expected = 'abcdefdeabc'
        self.assertEqual(actual, expected)

    def test_decompress_3(self):
        """ Decompress string that ends with repeated sequence:
        service byte: 00000001"""
        b_array = bytearray([1]) + bytearray(b'abcdefg') + bytearray([0, 99])
        actual = LZ77.decompress(b_array)
        expected = 'abcdefgabcde'
        self.assertEqual(actual, expected)

    def test_decompress_4(self):
        """ Decompress string that has repeated sequences at the begin of service_byte:
        service bytes: 00000000, 10000000 """
        b_array = bytearray([0]) + bytearray(b'abcdefgh')\
                   + bytearray([128]) + bytearray([0, 84])
        actual = LZ77.decompress(b_array)
        expected = 'abcdefghcdefgh'
        self.assertEqual(actual, expected)

    def test_decompress_max_seq_len(self):
        """ Decompress string that has repeated sequence of max len (17) """
        a_int = ord('a')
        seq = ''.join(map(chr, range(a_int, a_int + LZ77.max_seq)))
        text = '123' + seq + '345' + seq
        b_array = bytearray([0]) + bytearray(text[:8], 'utf-8')\
                   + bytearray([0]) + bytearray(text[8: 16], 'utf-8')\
                   + bytearray([1]) + bytearray(text[16: 23], 'utf-8')\
                   + bytearray([1, 63])
        actual = LZ77.decompress(b_array)
        expected = text
        self.assertEqual(actual, expected)

    def test_decompress_offset_less_len(self):
        """ Decompress string that has repeated sequences where offset
        is less then sequence lenth """
        b_array = bytearray([32]) + bytearray(b'ab') + bytearray([0, 18])
        actual = LZ77.decompress(b_array)
        expected = 'ababab'
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(exit=False)
