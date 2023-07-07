if __name__ == '__main__':
    n = int(input())
    arr = sorted([*map(int, input().split())])
    c = []
    if len(arr) == n:
        for i in arr:
            if i != max(arr):
                c.append(i)
    print(max(c))
