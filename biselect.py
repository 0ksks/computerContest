def binary(n:int)->list[str]:
    """
    生成n位二进制数，用于获取指定集合的幂集

    Args:
        n (int): 元素个数

    Returns:
        list[str]: 二进制码，1代表含有，0代表不含有
    """
    res = []
    for i in range(1, 2**n):
        binary = format(i, '04b')
        res.append(binary)
    return res
def select(li:list)->list[list]:
    """
    获取指定集合的幂集

    Args:
        li (list): 指定集合

    Returns:
        list[list]: 幂集
    """
    ress = []
    bis = binary(len(li))
    for bi in bis:
        res = []
        for i,c in enumerate(list(bi)):
            if c=="1":
                res.append(li[i])
        ress.append(res)
    return ress
if __name__ == "__main__":
    print(*select("a b c d".split()), sep="\n")