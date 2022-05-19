import FontColorModule
import socket
import queue
import threading
import time


#测试数据（从GUI中传入数据）
meslist = []
que = queue.Queue()         #初始化一个队列，用于保存扫描端口队列
lettercolor = FontColorModule.ChangeColor()


class PortScanner(threading.Thread):
    def __init__(self, host):
        super().__init__()
        self.host = str(host)


    def run(self) -> None:
        while True:
            port = que.get()        #获取端口号,que.task_done告诉队列已获取数据,从而让que.join继续或停止
            self.Scanner(port)
            que.task_done()
            time.sleep(0.2)


    def Scanner(self, port):
        conn = socket.socket()
        try:
            conn.connect((self.host, port))
            #print(f'[+]Port{port}:Open.')
            #gui.ui.outwindow.append(lettercolor.Res + f'[+]PortNum:{port} (Status:Open.)' + lettercolor.ColorEnd)
            gui.ui.outwindow.append(lettercolor.Res + '[+]PortNum:{0} (Status:Open.)'.format(port) + lettercolor.ColorEnd)
            conn.close()
        except:
            pass

           
def Receive(host, start, end, thread):      #接收外部数据函数
    global meslist
    meslist = [host, start, end, thread]
    return meslist
    

def UIreceive(GUI):      #接收GUI实例
    global gui
    gui = GUI
    return gui


def StartScan():    #开始扫描函数
    ip = socket.gethostbyname(meslist[0])
    
    for i in range(int(meslist[3])):
        t = PortScanner(ip)
        t.setDaemon(1)      #添加守护进程
        t.start()
        
    for i in range(int(meslist[1]), int(meslist[2])+1):         #根据第二第三项输入构建队列，左闭右开区间，所以endport+1
        que.put(i)

    que.join()
    gui.ui.outwindow.append(lettercolor.Mes + '[*]PortScan Finished.' + ' >>> ' + \
    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
    #print(type(t))
    #print(id(t))
    