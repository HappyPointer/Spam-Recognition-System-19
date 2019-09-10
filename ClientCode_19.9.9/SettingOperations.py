import traceback
import os


class Setting_Operations:

    # 获取本地存储的过滤强度
    def getIntensity(self,mailAddress):
        try:
            filename=mailAddress+'.txt'
            if os.path.exists(filename):
                fo = open(filename, "r")
                intensity = fo.read(6)
                fo.close()
                return intensity
            else:
                return 'default'

            # 输出
            # if (intensity == "low"):
            #     intensity_result="低强度"
            # elif (intensity == "high"):
            #     intensity_result="高强度"
            # else:
            #     # 当文件为空时默认是中强度
            #     intensity_result="中强度"
            # return intensity_result
        except Exception as e:
            traceback.print_exc()
            return 'default'

    # 更改本地的过滤强度
    # debug:文件写失败 解决方案:增加try，except，finally增加保护措施
    def setIntensity(self, intensity, mailAddress):
        if(intensity == "低强度"):
            result = "low"
        elif(intensity == "中强度"):
            result = "medium"
        elif(intensity == "高强度"):
            result = "high"
        else:
            result = "default"
        # 以二进制格式打开一个文件只用于写入，原有内容被删除
        try:
            # 2019/9/2 21:41 debug：a bytes-like object is required, not 'str'
            # 将参数wb改为w，问题解决
            filename=mailAddress+'.txt'
            fo = open(filename, "w")
            fo.write(result)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            fo.close()


