class Flitering_rule:
    """
    过滤规则类
    """
    sender = None  # 发件人
    keyword = None  # 关键词
    type = None # 邮件类型

    def __init__(self , sender = None, keyword = None, type = None):
        self.sender = sender
        self.keyword = keyword
        self.type = type


