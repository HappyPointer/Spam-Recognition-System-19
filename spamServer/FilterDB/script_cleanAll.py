import filter_rule_DB_operation


def cleanTable():
    x = filter_rule_DB_operation.Filter_operation()
    result = x.clean_table()
    if(result):
        # 如果清空数据库成功
        print("清空数据库成功！")
        # 如果失败，则在clean_table()中print("清空失败！")

cleanTable()