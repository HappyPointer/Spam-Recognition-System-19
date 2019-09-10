"""
说明：脚本，清空数据库
作者：71117205丁婧伊
创建时间：2019/8/29
最后一次修改时间：2019/8/29
"""
import filter_rule_DB_operation


def cleanTable():
    """
    清空数据库
    """
    x = filter_rule_DB_operation.Filter_operation()
    result = x.clean_table()
    if(result):
        # 如果清空数据库成功
        print("清空数据库成功！")
        # 如果失败，则在clean_table()中print("清空失败！")

cleanTable()