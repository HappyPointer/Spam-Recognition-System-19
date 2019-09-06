import imaplib
import email
import re
import time
import traceback

import chardet
import socket

from retrying import retry


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
    # print('Subject:', subject)
    # 发件人
    # print('From:', email.utils.parseaddr(message.get('from'))[1])
    # 收件人
    # print('To:', email.utils.parseaddr(message.get('to'))[1])
    # 日期
    # print('Date : ' + message["Date"])
    #添加主题，发件人，收件人，日期到列表里
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
                subject = message.get('subject')
                dh = email.header.decode_header(subject)
                # 内容类型，一般有image,text/plain,text/html
                content_type = part.get_content_type()
                try:
                    # 如果是纯文本
                    if (content_type == 'text/plain'):
                        # gbk解决中文编码，utf-8解决英文编码
                        # 只要打印了一次就返回，解决原始邮件体和html版本邮件体重复度读取的问题
                        print(dh[0][1])
                        if dh[0][1]==None:
                            return str(part.get_payload(decode=True), encoding='gbk')
                        else:
                            return str(part.get_payload(decode=True),encoding=dh[0][1] )
                    # 如果是html
                    elif content_type == 'text/html':
                        # 把邮件转换为html格式
                        if dh[0][1] == None:
                            a = str(part.get_payload(decode=True), encoding='gbk')
                        else:
                            a = str(part.get_payload(decode=True), encoding=dh[0][1])
                        # 编写正则表达式匹配汉字
                        b = re.compile(u"[\u4e00-\u9fa5]{1,2}")
                        # 匹配汉字
                        c = b.findall(a)
                        # 输出匹配结果
                        bodystr = ''
                        for i in c:
                            bodystr += i
                        return bodystr
                except:
                    traceback.print_exc()
                    if (content_type == 'text/plain'):
                        # 打印邮件体
                        return str(part.get_payload(decode=True), encoding='utf-8')
                    elif content_type == 'text/html':
                        # print(str(part.get_payload(decode=True), 'gbk'))
                        # 把邮件转换为html格式
                        a = str(part.get_payload(decode=True), 'utf-8')
                            # .encode('utf-8')
                        # 编写正则表达式匹配汉字
                        b = re.compile(u"[\u4e00-\u9fa5]{1,2}")
                        # 匹配并输出匹配结果

                        c = b.findall(a)
                        bodystr = ''
                        for i in c:
                            bodystr += i
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
        traceback.print_exc()
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
        traceback.print_exc()
        try:
            # 使用IMAP4连接
            serv = imaplib.IMAP4(host, 143)
        except Exception as e:
            traceback.print_exc()
            resultlist.append('连接失败，请检查服务器和端口名称！')
            return resultlist

    try:
        # 登录邮箱
        serv.login(username, password)
    except:
        traceback.print_exc()
        resultlist.append('登陆失败，请检查您的邮箱和密码是否正确！')
        return resultlist

    #将登录成功信息，登陆凭证，用户名添加至list
    resultlist.append('登陆成功！')
    resultlist.append(serv)
    resultlist.append(username)

    return resultlist

def checkNewMail(serv):
    # 参数可以选择收件文件夹
    serv.select('INBOX')
    #按搜索条件进行搜索
    typ, data = serv.search(None, 'ALL')
    #获取历史邮件数量
    num_old = len(data[0].split())
    while True:
        # 进行更新
        typ, data = serv.search(None, 'ALL')
        #获取新的邮件数量
        num_new = len(data[0].split())
        if num_new == num_old:
            pass
        elif num_new > num_old:
            oneemail = []
            print('您收到了新邮件！')
            #新创建一个邮件列表来存储邮件
            emaillist=[]
            for num in range(num_old, num_new):
                try:
                    emailcontent=[]
                    typ, data_new = serv.fetch(data[0].split()[num], '(RFC822)')
                    # 数据元组
                    text = data_new[0][1]
                    # 编码方式
                    encoding = chardet.detect(text)['encoding']
                    new_text = str(text, encoding)
                    # 转换为email.Message对象
                    message = email.message_from_string(new_text)
                    # 解析邮件头部
                    emailcontent.append(parseHeader(message))
                    # 解析邮件体
                    emailcontent.append(parseBody(message))
                except Exception as e:
                    traceback.print_exc()

                emaillist.append(emailcontent)
            # 更新邮件数量
            num_old = num_new
            return emaillist

def getAllMail(serv):
    """
    获取邮箱内全部的邮件
    :param serv:
    :return:
    """
    # IMAP4.select([mailbox[, readonly]])第一个参数是邮箱名，默认是INBOX，readonly是只能读，不能修改
    serv.select()  # 参数可以选择收件文件夹
    # IMAP4.search()第二个参数：All,Unseen,Seen,Recent,Answered, Flagged，返回
    typ, data = serv.search(None, 'ALL')
    maillist=[]
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
            messageall=[]
            # 解析邮件头部
            messageheader=parseHeader(message)
            # 解析邮件体
            messagebody=parseBody(message).strip()
            messageall.append(messageheader)
            messageall.append(messagebody)
            maillist.append(messageall)
        except Exception as e:
            # print(e)
            traceback.print_exc()
    return maillist

    # serv.close()
    # serv.logout()
def getSomeMail(serv,num_old):
    """
    获取邮箱内全部的邮件
    :param serv:
    :return:
    """
    # IMAP4.select([mailbox[, readonly]])第一个参数是邮箱名，默认是INBOX，readonly是只能读，不能修改
    serv.select()  # 参数可以选择收件文件夹
    # IMAP4.search()第二个参数：All,Unseen,Seen,Recent,Answered, Flagged，返回
    typ, data = serv.search(None, 'ALL')
    num_new=len(data[0].split())
    if num_new == num_old:
        return False

    maillist=[]
    # 通过编号遍历search出的所有邮件
    for num in range(num_old+1,num_new+1):
        try:
            # 打印邮件序号
            num=repr(num)
            typ, data = serv.fetch(num.encode(), '(RFC822)')
            # 数据元组
            text = data[0][1]
            new_text = str(text, encoding=chardet.detect(text)['encoding'])
            # 转换为email.message对象
            message = email.message_from_string(new_text)  # 转换为email.message对象
            messageall=[]
            # 解析邮件头部
            messageheader=parseHeader(message)
            # 解析邮件体
            messagebody=parseBody(message).strip()
            messageall.append(messageheader)
            messageall.append(messagebody)
            maillist.append(messageall)
        except Exception as e:
            # print(e)
            traceback.print_exc()
    return maillist

def getMailNum(serv):
    serv.select()
    typ,data=serv.search(None,'ALL')
    return len(data[0].split())
def getMailByDate(serv):
    """
    根据日期获取一个邮件列表
    :param serv:
    :return:
    """
    # IMAP4.select([mailbox[, readonly]])第一个参数是邮箱名，默认是INBOX，readonly是只能读，不能修改
    serv.select()  # 参数可以选择收件文件夹
    # IMAP4.search()第二个参数：All,Unseen,Seen,Recent,Answered, Flagged，返回
    typ, data = serv.search(None, 'BEFORE','1-may-2019')
    maillist=[]
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
            messageall=[]
            # 解析邮件头部
            messageheader=parseHeader(message)
            # 解析邮件体
            messagebody=parseBody(message)
            #把邮件头部，主题添加至一个列表里
            messageall.append(messageheader)
            messageall.append(messagebody)
            maillist.append(messageall)
        except Exception as e:
            # print(e)
            traceback.print_exc()

    return maillist


def filter(oneEmail, rulelist):
    """
    根据过滤规则对一封邮件进行过滤处理
    :param oneEmail:
    :param rulelist:
    :return:
    """
    #如果没有过滤规则，则直接交至服务器处理
    if rulelist==None:
        return None
    #如果有过滤规则，则按照对应逻辑判断其类型
    for i in rulelist:
        rule=i
        judgelist=[0,0]
        if rule['sender']=='':
            judgelist[0]=2
        elif rule['sender']!=oneEmail[0][1]:
            judgelist[0]=1

        if rule['key_word']=='':
            judgelist[1]=2
        elif rule['key_word'] not in oneEmail[1] and rule['key_word'] not in oneEmail[0][0]:
            judgelist[1]=1

        if 0 in judgelist and 1 not in judgelist:
            print('识别正确')
            return rule['type']
    #若所有规则均不符合，则交付服务器处理
    return None
@retry(stop_max_attempt_number=3)
def send_client_email_list(intensity,emaillist):
    response_result_list=[]
    email_content_list=[]
    for oneemail in emaillist:
        email_content_list.append({'body':oneemail[1],'intensity':intensity})
    judge_result_list=send_client('request-result',email_content_list)
    num=0
    for result in judge_result_list['content']:
        response_result=[]
        response_result.append(emaillist[num])
        if result==1:
            response_result.append('正常邮件')
        elif result==-1:
            response_result.append('垃圾邮件')
        elif result==0:
            response_result.append('未知类型')
            print('未知类型的返回数据')

        response_result_list.append(response_result)
        num+=1
    print(response_result_list)
    return response_result_list




def checkAndJudgeNewMail(serv,rulerlist):
    """
    检测新的邮件，并且判断邮件类型并返回一个邮件和结果tuple的列表
    :param serv:
    :param rulerlist:
    :return:
    """
    #通过调用查新函数来获取新邮件
    emaillist=checkNewMail(serv)
    #建立邮件和结果tuple的列表
    response_result_list=[]
    email_list=[]
    #对邮箱中的每一封邮件进行判断
    for oneemail in emaillist:
        response_result=[]
        #将邮件交至过滤器处理
        resulte=filter(oneemail,rulerlist)
        #将邮件主题添加至列表里
        #根据过滤器的对应结果，给出相对应的判断
        if resulte=='black':
            response_result.append(oneemail)

            response_result.append('垃圾邮件')
            print('这是一封垃圾邮件')
        elif resulte=='star':
            response_result.append(oneemail)

            response_result.append('星标邮件')
            print('这是一封星标邮件')
        elif resulte=='white':
            response_result.append(oneemail)

            response_result.append('白名单邮件')
            print('这是一封正常邮件')
        elif resulte==None:
            email_list.append(oneemail)

        if response_result!=[]:
            response_result_list.append(response_result)
    try:
        response_result_list2=send_client_email_list(email_list)
    except:
        response_result_list2=[]
        for email in email_list:
            response_result=[]
            response_result.append(email)
            response_result.append('网络异常')
            response_result_list2.append(response_result)
        traceback.print_exc()
    response_result_list+=response_result_list2
    return response_result_list


def checkAndJudgeOldMail(serv,intensity,rulerlist):
    """
    获取邮箱内的历史邮件并给出其判断结果
    :param serv:
    :param rulerlist:
    :return:
    """
    print('sensitivty : ' + intensity)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    #根据getallmail函数获取全部邮件
    emaillist=getAllMail(serv)
    print(emaillist)
    response_result_list=[]
    email_list=[]
    #对每一封邮件进行处理
    for oneemail in emaillist:
        response_result=[]
        #交至过滤器处理
        resulte=filter(oneemail,rulerlist)
        #根据过滤器返回的结果，进行不同的处理
        if resulte=='black':
            response_result.append(oneemail)

            response_result.append('垃圾邮件')
            print('这是一封垃圾邮件')
        elif resulte=='star':
            response_result.append(oneemail)

            response_result.append('星标邮件')
            print('这是一封星标邮件')
        elif resulte=='white':
            response_result.append(oneemail)

            response_result.append('正常邮件')
            print('这是一封正常邮件')
        elif resulte==None:
            email_list.append(oneemail)

        if response_result != []:
            response_result_list.append(response_result)
    try:
        response_result_list2 = send_client_email_list(intensity,email_list)
    except:
        response_result_list2 = []
        for email in email_list:
            response_result = []
            response_result.append(email)
            response_result.append('网络异常')
            response_result_list2.append(response_result)
        traceback.print_exc()

    print(4)
    for response_result in response_result_list2:
        response_result_list.append(response_result)
    print(5)
    # print(response_result_list)

    return response_result_list

def judgeNewMail(intensity,emaillist,rulelist):
    """
    判断一个列表的邮件是否为垃圾邮件
    :param emaillist:
    :param rulelist:
    :return:
    """
    #由于逻辑和以上函数逻辑及其相似，不多赘述
    email_list=[]
    response_result_list=[]
    for oneemail in emaillist:
        response_result=[]
        resulte=filter(oneemail,rulelist)
        if resulte=='black':
            response_result.append(oneemail)

            response_result.append('垃圾邮件')
            print('这是一封垃圾邮件')
        elif resulte=='star':
            response_result.append(oneemail)

            response_result.append('星标邮件')
            print('这是一封星标邮件')
        elif resulte=='white':
            response_result.append(oneemail)

            response_result.append('正常邮件')
            print('这是一封正常邮件')
        elif resulte==None:
            email_list.append(oneemail)

        if response_result != []:
            response_result_list.append(response_result)
            # try:
            #     judge_result=send_client('request-result',oneemail[1])
            #     if judge_result['content']==1:
            #         response_result.append('正常邮件')
            #     elif judge_result['content']==-1:
            #         response_result.append('垃圾邮件')
            #     else:
            #         print('??????????')
            # except:
            #     print('网络通讯出现错误!')
            #     response_result.append('网络通讯错误')
    try:
        response_result_list2 = send_client_email_list(intensity,email_list)
    except:
        response_result_list2 = []
        for email in email_list:
            response_result = []
            response_result.append(email)
            response_result.append('网络异常')
            response_result_list2.append(response_result)
        traceback.print_exc()

    response_result_list += response_result_list2
    print(response_result_list)
    return response_result_list

def send_client(action,content):
    """
    根据对应参数所给出的action，content发送对应请求到服务器，获取对应的资源
    :param action:
    :param content:
    :return:
    """
    #初始化连接
    link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #和服务器进行连接
    link.connect(('106.52.236.143', 3389))
    #构建要发送的内容
    data = {'action':action,'content':content}
    len_s=len(repr(data).encode())
    print(repr(len_s).encode())
    link.send(repr(len_s).encode())
    print(456789)
    if not data:
        #如果数据为空，就返回none
        return None
    else:
        #发送数据
        print(repr(data))
        print(repr(data).encode(encoding='utf-8'))
        link.sendall(repr(data).encode(encoding='utf-8'))
    #接收服务器所返回的数据
    response=link.recv(10240000)
    if not response:
        #如果服务器发送字节为空，那么直接返回
        link.close()
        return None
    else:
        #格式化服务返回的数据并将其返回
        response_dict=eval(response)
        link.close()
        return response_dict

def returnStrRuleList(rulelist):
    """
    这里的rulelist是字典的集合
    :param rulelist:
    :return:
    """
    #在这里将过滤器规则列表转化为字符串格式的列表
    rule_str_list=[]
    for i in rulelist:
        rule=i
        rule_str='当收到'
        rule_str=rule_str+'来自:\''+rule['sender']+'\''
        rule_str=rule_str+'包含:\''+rule['key_word']+'\'时'
        rule_str=rule_str+'将该邮件视为:'+rule['type']
        rule_str_list.append(rule_str)
    return rule_str_list

def showRuleList():
    """
    这里会返回规则的字符串集合
    :return:
    """
    #载入用户名
    rulelist=loadFilterRule('3389089691@qq.com')
    #获得字符串格式的过滤规则列表
    rule_str_list=returnStrRuleList(rulelist)
    return rule_str_list

def saveFilterRule(username, rule_list):
    """
    这里的rulelist是字典的集合
    :param username:
    :param rule_list:
    :return:
    """
    #此函数的作用就是把dict形式的过滤规则转换为json格式的过滤规则并保存为json文件
    try:
        rule_dict_list=[]
        #根据过滤器规则建立字典
        rule_dict_all={username:rule_dict_list}
        #将字典转换为json格式
        rule_json = json.dumps(rule_dict_all, indent=4)
        #写入json文件之中
        f=open(username+'.json','w',encoding='utf-8')
        f.write(rule_json)
        f.close()
        print('写入成功!')
    except Exception as e:
        traceback.print_exc()

def loadFilterRule(username):
    """
    根据用户名载入对应的过滤规则
    :param username:
    :return:
    """
    try:
        #打开对应用户json文件
        f=open(username+'.json','r',encoding='utf-8')
        #载入
        rule_json=json.load(f)
        f.close()
        rule_list=rule_json[username]
        return rule_list
    except:
        traceback.print_exc()
        print('无法打开文件')
        return '不存在该文件'

def fetch_mails(mail_user,mail_password):
    print(465)
    mailbox = imaplib.IMAP4_SSL(host = 'imap.qq.com', port = 993)
    mailbox.login(mail_user, mail_password)
    mailbox.select('INBOX')
    typ, data = mailbox.search(None, 'SINCE', '1-Jul-2019')
    print(data[0])


if __name__ == '__main__':
    username = "3389089691@qq.com"
    password = "rnhprnvdybxwciec"

    # # username = "seu_gzd@outlook.com"
    # # password = "5636636a"
    # username = "1063650139@qq.com"
    # password = "vqkrvgpdmtfjbbcf"
    # username = "290452313@qq.com"
    # password = "wpnorbeothacbjbf"
    fetch_mails(username,password)

    # print(judgeNewMail(emaillist,None))
    # getMailByDate(serv[1])
    # print(serv)
    # a=flitering_rule.Flitering_rule('3389089691@qq.com',None,False,True)
    #
    # lista=[]
    # lista.append(a)
    #
    # checkAndJudgeNewMail(serv[1],lista)

    # dic_list=[{'id':1,'owner':'a1','sender':'','key_word':'才寻鲲','type':'black'}]
    # dict_list=[flitering_rule.Flitering_rule(None,'才寻鲲',None)]
    # saveFliterRule('3389089691@qq.com',dic_list)
    # print(showRuleList())
    # dic_list = [{'id': 1, 'owner': 'a1', 'sender': '', 'key_word': '才寻鲲', 'type': 'black'}]
    # len_list=0
    # response_result_list = checkAndJudgeOldMail(serv[1], dic_list)
    # if len(response_result_list) > len_list:
    #     print(response_result_list[len_list:len(response_result_list)])
    #     len_list=len(response_result_list)
    # else:
    #     pass





