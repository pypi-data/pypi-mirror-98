"""nester_km_zhhm.py模块的功能是递归调用print_lol函数打印列表中的数据项
其中可能包含(也科可能不包含)嵌套列表。"""


def print_lol(the_list, level):
    """这个函数包括一个位置参数，名为"the_list",这可以是任何Python
    列表(也可以是包含嵌套列表的列表)。所指定的列表中的每个数据项会递归
    地输出到屏幕上，各数据项各占一行。
    第二个参数(名为"level")用来在遇到嵌套列表时插入制表符，如果大于0，
    才插入制表符进行缩进，否则不缩进，同时，控制插入制表符的个数。"""
    # 单行注释:for循环递归调用函数print_lol
    for each_item in the_list:
        if isinstance(each_item, list):
            if level >= 0:
                level = level+1
            print_lol(each_item, level)
        else:
            for tab_num in range(level):
                # print(tab_num)
                print("\t", end='')
            print(each_item)
