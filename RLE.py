# service_byte:
# 1 bit (first) is sequence type: 0 - different element, 1 - same element
# 7 bits for sequence length
max_seq = 127
max_seq_same = max_seq + 2
max_seq_diff = max_seq + 1

def save_seq_same(seq_count, last_byte, dest):
    """ Compress the sequence of the same bytes """
    service_byte = 128 | (seq_count - 2)
    dest.append(service_byte)
    dest.append(last_byte)

def save_seq_diff(seq_diff, dest):
    """ Compress sequence of different bytes """
    service_byte = len(seq_diff) - 1
    dest.append(service_byte)
    dest.extend(seq_diff)

def compress(orig):
    """ (list of bytes) -> list of bytes

    Compress the orig array and save it as dest array.

    Returns the compressed list of bytes.

    >>> compress([255, 255, 0, 255, 0, 255])
    [128, 255, 3, 0, 255, 0, 255]
    """
    dest = []
    if len(orig) == 0:
        return dest
    if len(orig) == 1:
        save_seq_diff(orig, dest)
        orig.pop()
        return dest

    seq_count = 1
    prev_byte = orig.pop(0)
    seq_diff = [prev_byte]
    while len(orig) > 0:
        cur_byte = orig.pop(0)
        if cur_byte == prev_byte:
            seq_count += 1
            if len(seq_diff) > 1:
                seq_diff.pop()
                save_seq_diff(seq_diff, dest)
            seq_diff = []

            # check seq lenth
            if seq_count >= max_seq_same:
                save_seq_same(seq_count, prev_byte, dest)
                seq_count = 0

                # proceed the rest of orig array from begining
                dest += compress(orig)
        else:
            seq_diff.append(cur_byte)
            if seq_count > 1:
                save_seq_same(seq_count, prev_byte, dest)
                seq_count = 1

            # check seq lenth
            if len(seq_diff) >= max_seq_diff:
                # check, probably new identical seq started at 128 element
                if len(orig) > 0:
                    if cur_byte == orig[0]:
                        seq_count = 1
                        seq_diff.pop()
                save_seq_diff(seq_diff, dest)
                seq_diff = []

        prev_byte = cur_byte

    if seq_count > 1:
        save_seq_same(seq_count, prev_byte, dest)
    elif len(seq_diff) > 0:
        save_seq_diff(seq_diff, dest)
    elif seq_count == 1:
        save_seq_diff([cur_byte], dest)

    return dest

def decompress(orig):
    """ (list of bytes) -> list of bytes

    Decompress the orig array and save it as dest array.

    Returns the decompressed list of bytes.

    >>> decompress([255, 255, 0, 255, 0, 255])
    [128, 255, 3, 0, 255, 0, 255]
    """
    dest = []
    while len(orig) > 0:
        service_byte = orig.pop(0)
        if service_byte & 128 != 0:
            # sequence of the same bytes
            seq_len = (service_byte & 127) + 2
            val = orig.pop(0)
            for j in range(seq_len):
                dest.append(val)
        else:
            # sequence of different bytes
            seq_len = service_byte + 1
            for j in range(seq_len):
                dest.append(orig.pop(0))
    return dest

if __name__ == '__main__':
    orig_array = [128] * 130
    orig_array += [1]
    compress([0] * 130)

