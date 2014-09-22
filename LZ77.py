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
    return result

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
            seq = find_best_subsequence(text, cur_pos)
            if seq == '': # save single char
                result += bytearray(text[cur_pos:cur_pos + 1], 'utf-8')
                cur_pos += 1
            else: # sequence is found
                seq_len = len(seq)
                # get position relative to current - 1
                pos = cur_pos - text.index(text[cur_pos:cur_pos + seq_len]) - 1
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
                if end <= len(result):
                    result += result[start:end]
                else:                  
                    while size > 0:
                        diff = end - len(result)
                        result += result[start:]
                        start += diff
                        end += diff
                        size -= diff
                        
        cur_pos += 1
    return result    

if __name__ == '__main__':
    b_array = bytearray([32]) + bytearray(b'ab') + bytearray([0, 18])
    decompress(b_array)
