# 该 py 文件将会将服务器的数据库完全清空
# 该 py 文件不会被其它文件引用，只能被数据库管理员在服务器控制台中手动调用
# 作者：丁婧伊
# 创建日期：2019-8-30
# 最后修改日期：2019-8-30

import filter_rule_DB_operation


def cleanTable():
    x = filter_rule_DB_operation.Filter_operation()
    result = x.clean_table()
    if(result):
        # 如果清空数据库成功
        print("清空数据库成功！")
        # 如果失败，则在clean_table()中print("清空失败！")

cleanTable()