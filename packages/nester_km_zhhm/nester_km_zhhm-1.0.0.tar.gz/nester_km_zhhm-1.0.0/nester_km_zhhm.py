"""nester_km_zhhm.py模块的功能是递归调用print_lol函数打印列表中的数据项
其中可能包含(也科可能不包含)嵌套列表。"""


def print_lol(the_list):
    """这个函数包括一个位置参数，名为"the_list",这可以是任何Python
    列表(也可以是包含嵌套列表的列表)。所指定的列表中的每个数据项会递归
    地输出到屏幕上，各数据项各占一行。"""
    # 单行注释:for循环递归调用函数print_lol
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
