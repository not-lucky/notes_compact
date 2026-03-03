def is_match_regex_optimized(s: str, p: str) -> bool:
    m, n = len(s), len(p)

    prev_row = [False] * (n + 1)
    prev_row[0] = True

    for j in range(2, n + 1):
        if p[j - 1] == '*':
            prev_row[j] = prev_row[j - 2]

    for i in range(1, m + 1):
        curr_row = [False] * (n + 1)

        for j in range(1, n + 1):
            curr_p = p[j - 1]
            curr_s = s[i - 1]

            if curr_p == curr_s or curr_p == '.':
                curr_row[j] = prev_row[j - 1]

            elif curr_p == '*':
                prev_p = p[j - 2]

                match_zero = curr_row[j - 2]

                match_one_more = False
                if prev_p == curr_s or prev_p == '.':
                    match_one_more = prev_row[j]

                curr_row[j] = match_zero or match_one_more

        prev_row = curr_row

    return prev_row[n]

print(is_match_regex_optimized("aa", "a*"))
