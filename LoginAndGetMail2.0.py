import imaplib
import email
import re
import time
import chardet
import flitering_rule
import socket
import MainUI0_9
import json

def parseHeader(message):
    """
    解析邮件首部
    :param message:
    :return:
    """
    headerlist = []

    subject = message.get('subject')
    dh = email.header.decode_header(subject)
    if dh[0][1] is None:
        subject = str(dh[0][0])
    else:
        subject = str(dh[0][0], dh[0][1])  # .encode('gb2312')
    # 主题
    print('Subject:', subject)
    # 发件人
    print('From:', email.utils.parseaddr(message.get('from'))[1])
    # 收件人
    print('To:', email.utils.parseaddr(message.get('to'))[1])
    # 日期
    print('Date : ' + message["Date"])

    headerlist.append(subject)
    headerlist.append(email.utils.parseaddr(message.get('from'))[1])
    headerlist.append(email.utils.parseaddr(message.get('to'))[1])
    headerlist.append(message["Date"])

    return headerlist

def parseBody(message):
    """
    解析邮件，信体
    :param message:
    :return:
    """
    # 循环信件中的每一个mime的数据块
    for part in message.walk():
        # 这里要判断是否是multipart，是的话，里面的数据是一个message 列表
        if not part.is_multipart():
            charset = part.get_charset()
            # 如果是附件，这里就会取出附件的文件名
            name = part.get_param("name")
            if name is None:
                # 编码方式
                encoding_type = part.get_charset()
                # 内容类型，一般有image,text/plain,text/html
                content_type = part.get_content_type()

                try:
                    # 如果是纯文本
                    if (content_type == 'text/plain'):
                        # gbk解决中文编码，utf-8解决英文编码
                        # 打印邮件体
                        print(str(part.get_payload(decode=True), 'gbk'))
                        print('\n')
                        # 只要打印了一次就返回，解决原始邮件体和html版本邮件体重复度读取的问题
                        return str(part.get_payload(decode=True), 'gbk')
                    # 如果是html
                    elif content_type == 'text/html':
                        # 把邮件转换为html格式
                        a = str(part.get_payload(decode=True), 'gbk')
                        # 编写正则表达式匹配汉字
                        b = re.compile(u"[\u4e00-\u9fa5]{1,2}")
                        # 匹配汉字
                        c = b.findall(a)
                        # 输出匹配结果
                        bodystr = ''
                        for i in c:
                            print(i, end='')
                            bodystr += i
                        print('\n')
                        return bodystr
                except:
                    if (content_type == 'text/plain'):
                        # 打印邮件体
                        print(str(part.get_payload(decode=True), 'utf-8'))
                        print('\n')
                        return str(part.get_payload(decode=True), 'utf-8')
                    elif content_type == 'text/html':
                        # print(str(part.get_payload(decode=True), 'gbk'))
                        # 把邮件转换为html格式
                        a = str(part.get_payload(decode=True), 'utf-8').encode('utf-8')
                        # 编写正则表达式匹配汉字
                        b = re.compile(u"[\u4e00-\u9fa5]{1,2}")
                        # 匹配并输出匹配结果
                        c = b.findall(a)
                        bodystr = ''
                        for i in c:
                            print(i)
                            bodystr += i
                        print('\n')
                        return bodystr
            else:
                # 如果有附件，打印附件名并将附件保存到指定目录
                # 目前是如果有附件，则不读附件，只读文本
                dh = email.header.decode_header(name)
                fname = dh[0][0]
                encode_str = dh[0][1]
                if encode_str != None:
                    if charset == None:
                        fname = fname.decode(encode_str, 'gbk')
                    else:
                        fname = fname.decode(encode_str, charset)
                data = part.get_payload(decode=True)
                # 打印附件名称
                print('Attachment : ' + fname)
                # 保存附件
                if fname != None or fname != '':
                    savefile(fname, data, '')

def savefile(filename, data, path):
    """
    保存文件方法（都是保存在指定的根目录下）
    :param filename:
    :param data:
    :param path:
    :return:
    """
    try:
        # 文件名
        filepath = path + filename
        print('Saved as ' + filepath)
        f = open(filepath, 'wb')
    except:
        print('filename error')
        f.close()
    f.write(data)
    f.close()

def getEmailHost(adress):
    """
    根据邮箱后缀选取邮箱应该使用的host
    :param adress:
    :return:
    """
    p = re.findall('@(.*?).com', adress)
    if p[0] == 'qq':
        return 'imap.qq.com'
    elif p[0] == '163':
        return 'imap.163.com'
    elif p[0] == 'outlook':
        return 'imap-mail.outlook.com'
    return None

def confirmEmailFormat(adress):
    """
    根据输入的邮箱判断邮箱格式是否正确
    :param adress:
    :return:
    """
    p = re.match('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', adress)
    if p == None:
        return '邮箱格式错误！'
    else:
        return '邮箱格式正确！'

def logIn(username, password):
    """
    登录邮箱
    :param host:
    :param username:
    :param password:
    :param port:
    :return:
     """

    resultlist = []
    # 在此处判断邮箱格式是否正确
    p = re.match('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', username)
    if p == None:
        resultlist.append('邮箱格式错误')
        return resultlist
    else:
        pass

    # 在此处根据邮箱后缀获取
    host = getEmailHost(username)

    # 在此处执行登录操作
    try:
        # 使用IMAP4_SSL，通过SSL加密的套接字连接
        serv = imaplib.IMAP4_SSL(host, 993)
    except Exception as e:
        try:
            # 使用IMAP4连接
            serv = imaplib.IMAP4(host, 143)
        except Exception as e:
            resultlist.append('连接失败，请检查服务器和端口名称！')
            return resultlist

    try:
        # 登录邮箱
        serv.login(username, password)
    except:
        resultlist.append('登陆失败，请检查您的邮箱和密码是否正确！')
        return resultlist

    resultlist.append('登陆成功！')
    resultlist.append(serv)

    return resultlist

def checkNewMail(serv):
    serv.select('INBOX')  # 参数可以选择收件文件夹
    typ, data = serv.search(None, 'ALL')
    num_old = len(data[0].split())
    while True:
        # 进行更新
        typ, data = serv.search(None, 'ALL')
        num_new = len(data[0].split())
        if num_new == num_old:
            pass
        elif num_new > num_old:
            oneemail = []
            print('您收到了一封新邮件！')
            emaillist=[]
            for num in range(num_old, num_new):
                emailcontent=[]
                typ, data = serv.fetch(data[0].split()[num], '(RFC822)')
                # 数据元组
                text = data[0][1]
                # 编码方式
                encoding = chardet.detect(text)['encoding']
                new_text = str(text, encoding)
                # 转换为email.Message对象
                message = email.message_from_string(new_text)
                # 解析邮件头部
                emailcontent.append(parseHeader(message))
                # 解析邮件体
                emailcontent.append(parseBody(message))

                emaillist.append(emailcontent)
            # 更新邮件数量
            num_old = num_new
            return emaillist

def getAllMail(serv):
    # IMAP4.select([mailbox[, readonly]])第一个参数是邮箱名，默认是INBOX，readonly是只能读，不能修改
    serv.select()  # 参数可以选择收件文件夹
    # IMAP4.search()第二个参数：All,Unseen,Seen,Recent,Answered, Flagged，返回
    typ, data = serv.search(None, 'ALL')
    # 通过编号遍历search出的所有邮件
    for num in data[0].split():
        try:
            # 打印邮件序号
            typ, data = serv.fetch(num, '(RFC822)')
            # 数据元组
            text = data[0][1]
            new_text = str(text, encoding=chardet.detect(text)['encoding'])
            # 转换为email.message对象
            message = email.message_from_string(new_text)  # 转换为email.message对象
            # 解析邮件头部
            parseHeader(message)
            # 解析邮件体
            parseBody(message)
        except Exception as e:
            print(e)

    # serv.close()
    # serv.logout()

def filter(oneEmail, rulerlist):
    rule=flitering_rule.Flitering_rule()
    for i in rulerlist:
        rule=i
        judgelist=[0,0]

        if rule.sender==None:
            judgelist[0]=2
        elif rule.sender!=oneEmail[0][1]:
            judgelist[0]=1

        if rule.keyword==None:
            judgelist[0]=2
        elif rule.keyword not in oneEmail[1] and rule.keyword not in oneEmail[0][0]:
            judgelist[1]=1

        if 0 in judgelist and 1 not in judgelist:
            print('识别正确')
            if rule.black_list:
                return 'junk'
            elif rule.star_mail:
                return 'star'
            elif rule.white_list:
                return 'mail'
    return None

def checkAndJudgeNewMail(serv,rulerlist):
    while True:
        emaillist=checkNewMail(serv)
        for oneemail in emaillist:
            resulte=filter(oneemail,rulerlist)
            if resulte=='junk':
                print('这是一封垃圾邮件')
            elif resulte=='star':
                print('这是一封星标邮件')
            elif resulte=='mail':
                print('这是一封正常邮件')
            elif resulte=='model':
                print('交付模型处理')
                response_result=send_client('request_result',oneemail[1])
                return response_result
            elif resulte==None:
                print('交付模型处理')
                response_result=send_client('request_result',oneemail[1])
                return response_result

def send_client(action,content):
    link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    link.connect(('localhost', 1023))
    while True:
        data = {'action':action,'content':content}
        if not data:
            break
        else:
            link.sendall(repr(data).encode())
            break
    response=link.recv(1023)
    if response.strip()=='':
        pass
    else:
        print(eval(response))
    link.close()

def showRulerList(rulelist):
    rule=flitering_rule.Flitering_rule()
    rule_str_list=[]
    for i in rulelist:
        rule=i
        rule_str='当收到'
        rule_str=rule_str+'来自:\''+rule.sender+'\''
        rule_str=rule_str+'包含:\''+rule.keyword+'\'时'
        rule_str=rule_str+'将该邮件视为:'+rule.type
        rule_str_list.append(rule_str)
    return rule_str


def saveFliterRule(username, rule_list):
    try:
        rule=flitering_rule.Flitering_rule()
        rule_dict_list=[]
        for i in rule_list:
            rule=i
            rule_dict={'sender':rule.sender,'key_word':rule.keyword,'type':rule.type}
            rule_dict_list.append(rule_dict)
        rule_dict_all={username:rule_dict_list}
        rule_json = json.dumps(rule_dict_all, indent=4)
        f=open(username+'.json','w',encoding='utf-8')
        f.write(rule_json)
        f.close()
        print('写入成功!')
    except:
        print('写入时发生了错误')

def loadFliterRule(username):
    try:
        f=open(username+'.json','r',encoding='utf-8')
        rule_json=json.load(f)
        f.close()
        rule_list=rule_json[username]
        return rule_list
    except:
        print('无法打开文件')
        return '不存在该文件'



if __name__ == '__main__':
    username = "3389089691@qq.com"
    password = "rnhprnvdybxwciec"

    # username = "seu_gzd@outlook.com"
    # password = "5636636a"

    serv = logIn(username, password)
    getAllMail(serv[1])
    print(serv)
    a=flitering_rule.Flitering_rule('3389089691@qq.com',None,False,True)

    lista=[]
    lista.append(a)

    checkAndJudgeNewMail(serv[1],lista)


