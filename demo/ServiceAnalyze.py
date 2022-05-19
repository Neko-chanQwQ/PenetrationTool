import socket
import FontColorModule
import time


lst = []
lettercolor = FontColorModule.ChangeColor()
customizeddict = {3306:'mysql', 1521:'oracle', 1080:'socks', 5900:'vnc', 27017:'mongodb'}      #可自定义的端口号字典,增加识别范围


class ServiceAnly:
    def __init__(self, lst):
        self.lst = lst


    def DataProcess(self):
        for i in self.lst:
            #判断输入是否为正整数
            if str(i).isdigit():
                pass
            else:
                gui.ui.outwindow.append(lettercolor.Warn + '[-]{0} is not digit.'.format(str(i)) + ' >>> ' + \
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
                time.sleep(0.1)
                #print('{0} is not digit'.format(str(i)))
                continue

            time.sleep(0.1)
            try:
                port = int(i)
                if port > 65535 or port < 0:
                    gui.ui.outwindow.append(lettercolor.Warn + '[-]PortNumber {0} Overflow (Only 0-65535).'.format(port) + ' >>> ' + \
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
                    continue
                service = socket.getservbyport(port)
                gui.ui.outwindow.append(lettercolor.Res + '[+]Port {0} Service: {1}'.format(port, service) + lettercolor.ColorEnd)

            except socket.error:
                flags = 0       #判断标志,如果flags为1是在自定义字典中找到服务,反之为0
                for x in customizeddict:     #遍历字典的键值
                    if int(i) == x:     #判断键值与端口是否相等
                        service = customizeddict[x]
                        gui.ui.outwindow.append(lettercolor.Res + '[+]Port {0} Service: {1}'.format(int(i), service) + lettercolor.ColorEnd)
                        flags = 1
                        break
                if flags == 1:
                    continue
                elif flags == 0:
                    gui.ui.outwindow.append(lettercolor.Warn + '[-]Port {0} Service not found or Socket error.'.format(i) + ' >>> ' + \
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
                    pass
    


def Receive(mlst):      #接收数据列表
    global lst
    lst = mlst
    return lst
    

def UIreceive(GUI):      #接收GUI实例
    global gui
    gui = GUI
    return gui


def StartAnalyze():     #扫描主函数
    SerAnly = ServiceAnly(lst)
    SerAnly.DataProcess()
    time.sleep(0.1)
    gui.ui.outwindow.append(lettercolor.Mes + '[*]Service Analyze Finished.' + ' >>> ' + \
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
    