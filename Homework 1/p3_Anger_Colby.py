def find_dup_str(s, n):
    if n <= 0 or n > len(s):
        return ''

    for i in range(len(s) - n + 1):
        part1 = s[i:i + n]

        for j in range(i + n, len(s) - n + 1):
            part2 = s[j:j + n]

            if part1 == part2:
                return part1

    return ''


def find_max_dup(s):
    for n in range(len(s) // 2, 0, -1):
        dup = find_dup_str(s, n)
        if dup != '':
            return dup

    return ''


s = input('Enter a string: ')
n = int(input('Enter substring length: '))
print(find_dup_str(s, n))

s = input('Enter a string for maximum duplicated substring: ')
print(find_max_dup(s))
