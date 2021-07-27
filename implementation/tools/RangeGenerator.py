def strange(start, end_or_len, sequence='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Create a generator of a range of 'sequential' strings from
    start to end_or_len if end_or_len is a string or containing
    end_or_len entries if end_or_len is an integer.

    >>> list(strange('D', 'F'))
    ['D', 'E', 'F']
    >>> list(strange('Y', 'AB'))
    ['Y', 'Z', 'AA', 'AB']
    >>> list(strange('Y', 4))
    ['Y', 'Z', 'AA', 'AB']
    >>> list(strange('A', 'BAA', sequence='AB'))
    ['A', 'B', 'AA', 'AB', 'BA', 'BB', 'AAA', 'AAB', 'ABA', 'ABB', 'BAA']
    >>> list(strange('A', 11, sequence='AB'))
    ['A', 'B', 'AA', 'AB', 'BA', 'BB', 'AAA', 'AAB', 'ABA', 'ABB', 'BAA']
    """
    seq_len = len(sequence)
    start_int_list = [sequence.find(c) for c in start]
    if isinstance(end_or_len, int):
        inclusive = True
        end_int_list = list(start_int_list)
        i = len(end_int_list) - 1
        end_int_list[i] += end_or_len - 1
        while end_int_list[i] >= seq_len:
            j = end_int_list[i] // seq_len
            end_int_list[i] = end_int_list[i] % seq_len
            if i == 0:
                end_int_list.insert(0, j-1)
            else:
                i -= 1
                end_int_list[i] += j
    else:
        end_int_list = [sequence.find(c) for c in end_or_len]
    while len(start_int_list) < len(end_int_list) or start_int_list <= end_int_list:
        yield ''.join([sequence[i] for i in start_int_list])
        i = len(start_int_list)-1
        start_int_list[i] += 1
        while start_int_list[i] >= seq_len:
            start_int_list[i] = 0
            if i == 0:
                start_int_list.insert(0,0)
            else:
                i -= 1
                start_int_list[i] += 1