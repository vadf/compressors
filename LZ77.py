max_block = 4096 # 12 bits + 1
max_seq = 17 # 4 bits + 2
min_seq = 2
coding_size = 8 # one byte for coding info: 0 simple character, 1 - link to seqeunce

def find_best_subsequence(text, cur_pos):
    """ (str, int) -> str

    Returns the best subsequence of text[cur_pos:X] in text[shift:cur_pos]

    Precondition: min_seq <= cur_pos <= len(text) - min_seq
    """
    result = ''
    cur_len = min_seq
    is_seq_found = False
    # if we have sequence of cur_len, check for sequence cur_len + 1
    while cur_len <= max_seq \
    and text[cur_pos:cur_pos + cur_len] in text[:cur_pos]:
        is_seq_found = True
        cur_len += 1
    if is_seq_found:
        result = text[cur_pos:cur_pos + cur_len - 1]
        if len(result) < 2:
            result = ''
    return result

def compress(text):
    """ (str) -> array of bytes

    Returns compressed text in array of bytes
    """
    dest = bytearray()
    cur_pos = 0
    while cur_pos < len(text):
        dest += bytearray([0]) # add service_byte
        service_pos = len(dest) - 1
        for i in range(coding_size):
            seq = find_best_subsequence(text, cur_pos)
            if seq == '': # save single char
                dest += bytearray(text[cur_pos:cur_pos + 1], 'utf-8')
                cur_pos += 1
            else: # sequence is found
                seq_len = len(seq)
                # get position relative to current - 1
                pos = cur_pos - text.index(text[cur_pos:cur_pos + seq_len]) - 1
                link_bytes = pos << 4 | (seq_len - min_seq) # 2 bytes
                dest += bytearray([link_bytes >> 8, link_bytes & 255])
                cur_pos += seq_len
                # mark sequence bit
                dest[service_pos] = dest[service_pos] | (1 << coding_size - i - 1)

    return dest

if __name__ == '__main__':
    a_int = ord('a')
    seq = ''.join(map(chr, range(a_int, a_int + max_seq + 1)))
    text = seq + '12' + seq + '1234'
    compress(text)
