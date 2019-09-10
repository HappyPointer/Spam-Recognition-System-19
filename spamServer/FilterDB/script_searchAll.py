"""
说明：脚本，查找数据库表中的全部内容
作者：71117205丁婧伊
创建时间：2019/8/29
最后一次修改时间：2019/8/29
"""
import filter_rule_DB_operation


def searchAll():
    """
    查找数据库中全部内容
    :return:
    """
    x = filter_rule_DB_operation.Filter_operation()
    # 让返回的字典形式变得简单易读,indent = 0实现换行效果
    result = x.find_all_owner()
    print("数据库中全部数据为：")
    for i in result:
        print(i)

searchAll()