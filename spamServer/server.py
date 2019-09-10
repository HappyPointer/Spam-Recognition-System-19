# coding=utf-8

# 该文件是服务器监听用户请求，对不同请求进行响应的主要逻辑代码
# 作者：何颖智、郭振东
# 创建日期：2019-8-23
# 最后修改日期：2019-9-5

import socket
import threading
import FilterDB.filter_rule_DB_operation as filter_rule_DB_operation
import BayesClassifier as Classifier
from nltk.corpus import stopwords
import datetime
import traceback

# 在这里设置信号量，信号量为多少，就可以同时处理多少请求
sem = threading.Semaphore(10)


# 该函数为服务器接受到用户请求后，创建的处理线程所执行的函数
def receive_server(socklink, address):
    try:
        with sem:
            # 第一次从用户处接受将要发送字符串的长度
            length = socketlink.recv(102400)
            length = eval(length.decode())

            totalData = []  # 记录用户发送的 byte 类型通信内容
            current_length = 0
            while current_length < length:
                recv = socklink.recv(102400)
                current_length += len(recv)
                totalData.append(recv)

            # 解码获得字典格式的通信内容
            data = b''.join(totalData)
            data.decode()

            if not data:   # 未接受到相关信息
                print('No data received from ' + str(address) + "!  Request cancelled."
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))
                raise Exception("No data received.")
            else:
                data_dic = eval(data)  # 按约定好的通信格式，将字符串转换为字典变量

            if data_dic['action'] == 'request-result':
                # 在这里调用模型进行预测，然后返回一个结果（1（非垃圾）或-1（垃圾））
                bayes = Classifier.BayesClassifier()
                list = bayes.classify(data_dic['content'])
                content = []   # 如果返回结果为 0 说明出现了错误
                for result_item in list:
                    if result_item == 'ham':
                        content.append(1)
                    elif result_item == 'spam':
                        content.append(-1)
                    else:
                        content.append(0)

                # 以下为服务器对于用户端的返回，返回预测结果
                response_data = {'action': 'response-reslut', 'content': content}
                socklink.sendall(repr(response_data).encode())
                print('Request-result from ' + str(address) + " handled successfully."
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))

            elif data_dic['action'] == 'request-info':
                # 在这里可以根据data['content']中的username(这里的username是用户的目前的邮箱)获得对应的配置规则
                # 创建数据库操作对象
                DB_operation = filter_rule_DB_operation.Filter_operation()
                # 以下为服务器对于用户端的返回，返回对应的配置
                response_data = DB_operation.search_owner(data_dic)
                socklink.sendall(repr(response_data).encode())
                print('Request-info from ' + str(address) + " handled successfully."
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))

            elif data_dic['action'] == 'post':
                # 在这里需要写一个函数来接收data['content']中的配置规则,并返回一个值代表是否存储正确与否(1代表存储正确,-1代表存储失败)
                DB_operation = filter_rule_DB_operation.Filter_operation()
                # 以下为服务器对于用户端的返回，返回是否上传成功
                response_data = DB_operation.add_one_rule(data_dic)
                socklink.sendall(repr(response_data).encode())
                print('post from ' + str(address) + " handled successfully."
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))

            elif data_dic['action'] == 'delete':
                # 收到一个删除过滤规则的请求
                DB_operation = filter_rule_DB_operation.Filter_operation()
                # 调用数据库规则删除函数，返回操作是否成功
                response_data = DB_operation.delete_one_rule(data_dic)
                socklink.sendall(repr(response_data).encode())
                print('delete request from ' + str(address) + " handled successfully."
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))

            else:
                # 如果以上格式均不符合，那么打印错误
                print('Unknown request type from ' + str(address) + '. Request cancelled'
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))

    except Exception as error:
        print('Error happened in processing thread. \nClient: ' + str(address) + "\nError: "
              + str(error) + "    " + str(datetime.datetime.now().strftime('%F %T')))
        traceback.print_exc()
    finally:
        socklink.close()


if __name__ == '__main__':
    sock = None
    try:
        # 提前加 nltk 载语料库，防止第一次访问时过于频繁导致的错误
        stopwords.words('english')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 在这里可以更换为服务器的IP,端口视情况而定
        sock.bind(('172.16.0.2', 3389))
        # 在这里可以设置等待队列的最大数量，目前设置的是1，如果需求比较大的话，可以设置较大的数量
        sock.listen(100)

        print('Server launched successfully, waiting for requests...'
              + "    " + str(datetime.datetime.now().strftime('%F %T')))

        """
        在这里服务器进行监听，如果有客户端要求接入，
        在信号量允许的情况下，服务器会新建一条进程进行通信，
        在信号量不允许，等待队列允许的情况下，服务器将其加入等待队列
        在信号量不允许，等待队列不允许的情况下，服务器将用户请求抛弃
        在这里，允许的情况代表服务器可以进行处理，
        不允许的情况代表服务的队列已经爆满，无法处理
        进程最大数量的设置为 信号量的多少
        等待队列最大数量的设置 listen()中的数字
        """
        socketlink = None
        while True:
            try:
                socketlink, address = sock.accept()
                print('Received a request from ' + str(address) + "    " + str(datetime.datetime.now().strftime('%F %T')))
                # 客户端发起请求时，服务器会新建一条进程，与其通信
                t = threading.Thread(target=receive_server, args=(socketlink,address))
                t.start()
            except:
                # 如果发生错误，那么将通信关闭
                if socketlink is not None:
                    socketlink.close()
                print('Error happened in accepting socket linkage.\nServer has been closed.'
                      + "    " + str(datetime.datetime.now().strftime('%F %T')))
                break

    except:
        print('Error happened in main server thread.\nServer has been closed.'
              + "    " + str(datetime.datetime.now().strftime('%F %T')))
        traceback.print_exc()
    finally:
        # 在 finally 代码块中关闭socket,释放该程序占用的端口
        if sock is not None:
            sock.close()

    print('Server program has been terminated.')
