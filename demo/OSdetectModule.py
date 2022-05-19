import nmap
import time
import socket
import FontColorModule
from kamene.all import *


lettercolor = FontColorModule.ChangeColor()


class OsScan():
    def __init__(self, ip):
        self.ip = str(ip)

    
    def NmapScan(self):
        nscan = nmap.PortScanner()    
        try:
            #print(self.ip)
            result = nscan.scan(hosts = self.ip, arguments='-O')      #填写nmap参数
            os = result["scan"][self.ip]['osmatch'][0]['name']      #切片提取操作系统数据
            time.sleep(0.5)
            gui.ui.outwindow.append(lettercolor.Res + '[+]Target:{0} OS:{1}(For reference only!!!)'.format(self.ip, os) + lettercolor.ColorEnd)
            time.sleep(0.5)
            gui.ui.outwindow.append(lettercolor.Mes + '[*]OsDetect Finished.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return
        except:
            gui.ui.outwindow.append(lettercolor.Warn + '[-]Invalid input or Connect timeout.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return

    
    def TtlScan(self):
        pktip = kamene.all.IP(dst = self.ip)
        icmp = kamene.all.ICMP()
        packet = pktip / icmp
        result = sr1(packet, timeout=3, verbose=0)	#构造ping包向目标主机发送

        if result is None:
            pass
        elif int(result['IP'].ttl) <= 64:    #判断目标主机响应包中TTL值是否小于等于64
            gui.ui.outwindow.append(lettercolor.Res + '[+]Target:{0} OS:Linux/Unix(For reference only!!!)'.format(self.ip) \
            + lettercolor.ColorEnd)     #是的话就为linux/Unix
        else:
            gui.ui.outwindow.append(lettercolor.Res + '[+]Target:{0} OS:Windows(For reference only!!!)'.format(self.ip) \
            + lettercolor.ColorEnd)  #反之就是Windows
        
        time.sleep(0.5)
        gui.ui.outwindow.append(lettercolor.Mes + '[*]OsDetect Finished.' + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)



def Receive(Host, Method, GUI):
    global host, gui, scanmethod
    host = Host
    scanmethod = Method
    gui = GUI
    return host, gui, scanmethod
    

def StartScan():
    tranhost = socket.gethostbyname(host)
    scan = OsScan(tranhost)
    if str(scanmethod).upper() == 'TTL':
        scan.TtlScan()
    elif str(scanmethod).upper() == 'NMAP':
        scan.NmapScan()
    else:
        gui.ui.outwindow.append(lettercolor.Warn + '[-]Invalid input ScanMethod.' + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
    return

