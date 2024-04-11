import unicodedata
from opencc import OpenCC

cc = OpenCC('t2s')  # 't2s'表示繁体转简体


def full2half(input_str):
    return ''.join([unicodedata.normalize('NFKC', char) for char in input_str])


def clearT(s):
    s = cc.convert(full2half(s))
    return s.strip().strip(r'\n').replace('\n', '\\n')
