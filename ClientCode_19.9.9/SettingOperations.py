"""
说明：将存储用户设置的本地过滤器强度和获取用户本地的过滤强度封装成类，便于操作
作者：71117205丁婧伊
创建时间：2019/9/2
最后一次修改时间：2019/9/3
"""
import traceback
import os


# 封装类，封装了两个函数，分别是存储用户本地的过滤强度到一个文件中，以及读取用户本地存储的过滤强度
class Setting_Operations:

    # 获取本地存储的过滤强度，输入邮箱地址，输出过滤强度（分别为low，high，medium和default）
    def getIntensity(self, mailAddress):
        try:
            filename = './userFile/'+mailAddress+'.txt'
            if os.path.exists(filename):
                fo = open(filename, "r")
                intensity = fo.read(10)
                fo.close()
                return intensity
            else:
                return 'default'
        except Exception as e:
            traceback.print_exc()
            return 'default'

    # 更改并存储本地的过滤强度，输入中文过滤强度和邮箱地址，返回是否存储成功，True是存储成功，False是失败
    # 2019/9/3 debug: 文件写失败
    # 解决方案:增加try，except，finally增加保护措施
    def setIntensity(self, intensity, mailAddress):
        if intensity == "低强度":
            result = "low"
        elif intensity == "中强度":
            result = "medium"
        elif intensity == "高强度":
            result = "high"
        else:
            result = "default"
        # 以二进制格式打开一个文件只用于写入，原有内容被删除
        try:
            # 2019/9/2 21:41 debug：a bytes-like object is required, not 'str'
            # 将参数wb改为w，问题解决
            filename = './userFile/'+mailAddress+'.txt'
            fo = open(filename, "w")
            fo.write(result)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            fo.close()


