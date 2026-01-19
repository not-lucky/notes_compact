from random import randint


def quicksort(a, l=0, h=None):
    if h is None:
        h = len(a) - 1

    if l < h:
        p = partition(a, l, h)
        quicksort(a, l, p)
        quicksort(a, p + 1, h)


def partition(a, l, h):
    p = a[randint(l, h)]

    i, j = l - 1, h + 1

    while True:
        i += 1
        while a[i] > p:
            i += 1

        j -= 1
        while a[j] < p:
            j -= 1

        if i >= j:
            return j

        a[i], a[j] = a[j], a[i]


arr = [randint(0, 1 << 16) for _ in range(10)]

arr1 = arr[:]

quicksort(arr)

print(f"{arr=}\n{sorted(arr1, reverse=True)=}")
