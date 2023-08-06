"""nester_km_zhhm.py模块的功能是递归调用print_lol函数打印列表中的数据项
其中可能包含(也可能不包含)嵌套列表。"""


def print_lol(the_list, indent=False, level=-1):
    """
    V1.1.0 这个函数包括一个位置参数，名为"the_list",这可以是任何Python
    列表(也可以是包含嵌套列表的列表)。所指定的列表中的每个数据项会递归
    地输出到屏幕上，各数据项各占一行。
    V1.2.0 第二个参数(名为"level")用来在遇到嵌套列表时插入制表符，如果大于0，
    才插入制表符进行缩进，否则不缩进，同时，控制插入制表符的个数。
    V1.2.1 为函数提供一个可选参数level，并提供一个缺省值-1，当不提供level参数
    调用时，默认level为-1，不对嵌套列表进行缩进处理。level值为正数时，其初始值
    决定缩进从指定级别的tab制表符处开始
    V1.2.2 为函数新增一个可选参数indent,用于控制是否缩进，默认值为False，表示不
    缩进，当需要缩进时，调用新签名的API函数，并设置此参数为True。"""
    # 单行注释:for循环递归调用函数print_lol
    for each_item in the_list:
        if isinstance(each_item, list):
            """if level >= 0:
                level = level+1"""
            """if level >= 0:
                print_lol(each_item, level+1)
            else:
                print_lol(each_item, level)"""
            """if level == -1:
                print_lol(each_item)
            else:
                print_lol(each_item, level + 1)"""
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                for tab_num in range(level):
                    # print(tab_num, end='')
                    print("\t", end='')
            print(each_item)
