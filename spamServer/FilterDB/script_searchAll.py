# 该 py 文件将会将查询服务器数据库中拥有的所有数据
# 该 py 文件不会被其它文件引用，只能被数据库管理员在服务器控制台中手动调用
# 作者：丁婧伊
# 创建日期：2019-8-30
# 最后修改日期：2019-8-30

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