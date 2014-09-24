max_block = 4096 # 12 bits + 1
max_seq = 17 # 4 bits + 2
min_seq = 2
coding_size = 8 # one byte for coding info: 0 simple character, 1 - link to seqeunce

def find_best_subsequence(text, cur_pos):
    """ (str, int) -> (str, int)

    Returns the best subsequence of text[cur_pos:X] in text[shift:cur_pos]
    and it position

    Precondition: min_seq <= cur_pos <= len(text) - min_seq
    """
    result = ''
    cur_len = min_seq
    is_seq_found = False
    # if we have sequence of cur_len, check for sequence cur_len + 1
    start_pos = cur_pos - max_block
    start_pos = 0 if start_pos < 0 else start_pos
    while cur_len <= max_seq \
    and text[cur_pos:cur_pos + cur_len] in text[start_pos:cur_pos]:
        is_seq_found = True
        cur_len += 1
    if is_seq_found:
        result = text[cur_pos:cur_pos + cur_len - 1]
        if len(result) < 2:
            result = ''
    return (result, text[start_pos:].index(result) + start_pos)

def get_subseq_len(text, seq, pos):
    """ (string, int) -> int

    Returns the length of subsequence in text that starts from position pos
    and has part of seq

    >>> get_subseq_len('hahaha', 'ha', 4)
    2
    >>> get_subseq_len('hihiha', 'hi', 4)
    1
    >>> get_subseq_len('hahaah', 'ha', 4)
    0
    """
    length = 0
    text_len = len(text)
    for i in range(len(seq)):
        if text_len - 1 < pos + i:
            break
        if seq[i] == text[pos + i]:
            length +=1
        else:
            break
    return length


def compress(text):
    """ (str) -> array of bytes

    Returns compressed text in array of bytes
    """
    result = bytearray()
    cur_pos = 0
    while cur_pos < len(text):
        result += bytearray([0]) # add service_byte
        service_pos = len(result) - 1
        for i in range(coding_size):
            seq, pos = find_best_subsequence(text, cur_pos)
            if seq == '': # save single char
                result += bytearray(text[cur_pos:cur_pos + 1], 'utf-8')
                cur_pos += 1
            else: # sequence is found
                seq_len = len(seq)
                # check probably we have the same sequnce after that one
                while True:
                    upd_len = get_subseq_len(text, seq, cur_pos + seq_len)
                    seq_len += upd_len
                    if upd_len * 2 != seq_len:
                        break
                # get position relative to current - 1
                pos = cur_pos - pos - 1
                link_bytes = pos << 4 | (seq_len - min_seq) # 2 bytes
                result += bytearray([link_bytes >> 8, link_bytes & 255])
                cur_pos += seq_len
                # mark sequence bit
                result[service_pos] = result[service_pos] | (1 << coding_size - i - 1)

    return result

def decompress(b_array):
    """ (bytearray) -> string

    Returns decompressed text from array of bytes
    """
    result = ''
    total_len = len(b_array)
    cur_pos = 0
    while cur_pos < total_len:
        service_byte = b_array[cur_pos]
        for i in range(coding_size):
            cur_pos += 1
            if cur_pos >= total_len:
                break
            if service_byte & (1 << (coding_size - i - 1)) == 0:
                result += chr(b_array[cur_pos])
            else:
                offset = (b_array[cur_pos] << 4) | (b_array[cur_pos + 1] >> 4) + 1
                size = (b_array[cur_pos + 1] & 15) + 2
                start = len(result)- offset
                end = start + size
                cur_pos += 1
                if size <= offset:
                    result += result[start:end]
                else:
                    # case when length > offset, so need to add several sequences
                    while start < end:
                        diff = len(result) - start
                        result += result[start:end]
                        start += diff

        cur_pos += 1
    return result

if __name__ == '__main__':
    text = 'The compression and the decompression leave an impression. Hahahahaha!'
    print(text)
    compressed = compress(text)
    print(compressed)
    decompressed = decompress(compressed)
    print(decompressed)
