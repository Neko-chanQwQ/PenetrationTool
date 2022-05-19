#-------------------------------Qt模块导入-------------------------------
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
#-------------------------------功能模块导入-------------------------------
import FontColorModule      
import OSdetectModule
import ScanModuletest
import ServiceAnalyze
import ExploitModule
#-------------------------------标准模块导入-------------------------------
import threading
import time
import sys
import os


currentpath = os.path.dirname(__file__)     #获取当前文件路径
lettercolor = FontColorModule.ChangeColor()        #实例化字体颜色


#UserHelp为使用说明，可更改
UserHelp = '''
1.端口扫描参数用例:127.0.0.1,1,1000,2000(第一项为IP地址或者域名,第二项为起始端口,第三项为结束端口,第四项为线程数)
2.系统识别参数用例:192.168.1.1,ttl/nmap(第一项为IP地址,第二项为ttl扫描或者是nmap扫描)
注意:对自身设备使用ttl扫描需使用IPv4地址,无法使用环路地址,如127.0.0.1
3.端口分析参数用例:21,22,80,443
4.脚本整合可在项目中的Exploit文件夹进行渗透脚本的存放、导入、导出、删除操作(导入参数:import 导出参数:export 删除参数:delete)
5.一切参数使用英文逗号分隔
'''


class loadUI:

    def __init__(self):
        qfile_stats = QFile(currentpath + r'\UI\main.ui')   #UI文件路径，加载UI文件
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        #从文件中加载UI定义

        #从UI定义中动态创建一个相应的窗口对象
        #注意：里面的控件对象也成为窗口对象的属性了
        #比如self.ui.button,self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)
        
        #下面为信号处理
        self.ui.outwindow.setReadOnly(True)     #输出窗口只读
        self.ui.Scanbutton.clicked.connect(self.MultiThreadScan)        #端口扫描按钮点击事件连接
        self.ui.OSbutton.clicked.connect(self.MultiThreadOsDetect)      #操作系统识别按钮点击事件连接
        self.ui.outputclr.clicked.connect(self.ClearOutput)     #清除输出窗口
        self.ui.inputclr.clicked.connect(self.ClearInput)     #清除输入窗口
        self.ui.RestartButton.clicked.connect(self.RestartProgram)      #重启程序
        self.ui.InfoButton.clicked.connect(self.Infobox)        #使用说明
        self.ui.ServiceButton.clicked.connect(self.MultiThreadServiceAnly)     #端口号识别
        self.ui.ExpButton.clicked.connect(self.ExploitSet)        #脚本整合
        self.ui.NullButton.clicked.connect(self.NullFunc)     #待定模块

        #图片显示,程序logo等
        self.ui.logo.setPixmap(currentpath + r'\Icon\jiaran.png')       #右上角logo



    #下面为函数处理部分
    def Infobox(self):      #使用说明
        QMessageBox.information(self.ui, '操作说明', UserHelp)
        return


    def ClearOutput(self):      #清空输出窗口
        slt = QMessageBox.question(self.ui, 'Output Clear', '是否清空输出窗口')
        if slt == QMessageBox.Yes:
            self.ui.outwindow.clear()
            return
        elif slt == QMessageBox.No:
            self.ui.outwindow.append(lettercolor.Mes + '[*]Output Clear Cancel.' + \
            ' >>> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return


    def ClearInput(self):       #清除输入框
        slt = QMessageBox.question(self.ui, 'Input Clear', '是否清空输入窗口')
        if slt == QMessageBox.Yes:
            self.ui.textedit.clear()
            return
        elif slt == QMessageBox.No:
            self.ui.outwindow.append(lettercolor.Mes + '[*]Input Clear Cancel.' + \
            ' >>> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return


    def RestartProgram(self):       #重启进程，用于端口扫描后子线程无法终止导致的后续扫描无法得到预期扫描结果
        slt = QMessageBox.question(self.ui, 'Program Restart!', '程序将重新启动')
        if slt == QMessageBox.Yes:
            python = sys.executable
            os.execl(python, python, * sys.argv)
        elif slt == QMessageBox.No:
            self.ui.outwindow.append(lettercolor.Mes + '[*]Restart Program Cancel.' + \
            ' >>> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return


    def MultiThreadScan(self):      #创建线程扫描防止程序假死
        slt = QMessageBox.question(self.ui, '注意事项', '第二次使用端口扫描前需要重启程序')
        if slt == QMessageBox.Yes:
            ScanThread = threading.Thread(target=self.ScanProcess)
            ScanThread.start()
            return
        elif slt == QMessageBox.No:
            self.ui.outwindow.append(lettercolor.Mes + '[*]Restart Program before you use PortScan again.' + \
            ' >>> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return

    
    def MultiThreadOsDetect(self):      #系统识别线程
        OsThread = threading.Thread(target=self.OsDetect)
        OsThread.start()
        return
        

    def MultiThreadServiceAnly(self):       #服务识别线程
        ServiceThread = threading.Thread(target=self.ServiceAnly)
        ServiceThread.start()
        return
        


    #下方为主逻辑部分
    def ScanProcess(self):      #端口扫描输入信息处理函数
        try:
            meslist = []
            self.ui.outwindow.append(lettercolor.Mes + '[*]Using PortScan Now.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            time.sleep(0.5)
            ininfo = self.ui.textedit.toPlainText()     #获取输入栏信息
            #print(ininfo)
            #解释数据，并生成新列表
            for i in ininfo.split(','):
                meslist.append(i)
            del ininfo
            #print(meslist)
            if meslist == ['']:     #判断输入是否为空
                self.ui.outwindow.append(lettercolor.Warn + '[-]PortScan input is empty.' + ' >>> ' + \
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
                return
            
            self.ui.outwindow.append(lettercolor.Mes + '[*]Domain name or IP address: {0} '.format(meslist[0]) + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            time.sleep(0.5)
            self.ui.outwindow.append(lettercolor.Mes + '[*]StartPort:{0}  EndPort:{1}  ThreadNum:{2}  '.format(meslist[1], meslist[2], meslist[3]) + \
            ' >>> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            time.sleep(0.5)
            #print('[*]Domain name or IP address: {0}'.format(meslist[0]))
            #print('[*]StartPort:{0};  EndPort:{1};  ThreadNum:{2}'.format(meslist[1], meslist[2], meslist[3]))
            #print(meslist)
            
            ip = meslist[0]
            sport = meslist[1]
            eport = meslist[2]
            thnum = meslist[3]
            #print('[*]Using PortScan Now')
            #print(id(meslist))
            del meslist
            #ScanModule.Receive(ip, sport, eport, thnum)
            #ScanModule.StartScan()
            ScanModuletest.Receive(ip, sport, eport, thnum)
            ScanModuletest.UIreceive(self)
            ScanModuletest.StartScan()
            del ip, sport, eport, thnum
            return
        except:
            time.sleep(0.5)
            self.ui.outwindow.append(lettercolor.Warn + '[-]Some Errors Occurred.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            time.sleep(0.5)
            self.ui.outwindow.append(lettercolor.Warn + '[-]Check Your Input Please.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            #print('[-]Some errors occurred!')
            #print('[-]Check your input please')
            return


    def OsDetect(self):
        meslist = []
        self.ui.outwindow.append(lettercolor.Mes + '[*]Using OsDetect Now.' + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        time.sleep(0.1)
        ininfo = self.ui.textedit.toPlainText()
        
        for i in ininfo.split(','):
            i = i.replace("\n", "")     #FixBug:在输入参数后进行回车导致异常报错
            meslist.append(i)

        del ininfo
        #print(meslist)
        if meslist == ['']:
            self.ui.outwindow.append(lettercolor.Warn + '[-]OsDetect input is empty.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return

        try:
            ip = meslist[0]
            scanmethod = meslist[1]
        except:
            self.ui.outwindow.append(lettercolor.Warn + '[-]Some Errors Occurred.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            time.sleep(0.1)
            self.ui.outwindow.append(lettercolor.Warn + '[-]Check Your Input Please.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return

        self.ui.outwindow.append(lettercolor.Mes + '[*]Detecting IP address or DomainName: {0} '.format(meslist[0]) + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        time.sleep(0.1)
        self.ui.outwindow.append(lettercolor.Mes + '[*]Using Detect method: {0} '.format(str(meslist[1].upper())) + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        
        try:
            OSdetectModule.Receive(ip, scanmethod, self)
            OSdetectModule.StartScan()
        except:
            self.ui.outwindow.append(lettercolor.Warn + '[-]Some Errors Occurred.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        return

    
    def ServiceAnly(self):
        lst = []
        ininfo = self.ui.textedit.toPlainText()     #获取输入栏信息
        for i in ininfo.split(','):
            i = i.replace("\n", "")     #FixBug:在输入参数后进行回车导致异常报错
            lst.append(i)
        del ininfo
        if lst == ['']:     #判断输入是否为空
            self.ui.outwindow.append(lettercolor.Warn + '[-]ServiceAnalyze input is empty.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return
        self.ui.outwindow.append(lettercolor.Mes + '[*]Service Analyze Start.' + \
        ' >>> ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        time.sleep(0.5)
        ServiceAnalyze.Receive(lst)
        del lst
        ServiceAnalyze.UIreceive(self)
        ServiceAnalyze.StartAnalyze()
        return

    
    def ExploitSet(self):
        self.ui.outwindow.append(lettercolor.Mes + '[*]ExploitModule Started.' + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        time.sleep(0.1)
        ininfo = self.ui.textedit.toPlainText()     #获取输入栏信息
        mes = ininfo.split()        #数据处理
        if not mes:
            self.ui.outwindow.append(lettercolor.Warn + '[-]ExploitModule input is empty.' + ' >>> ' + \
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
            return
        selectwindow = QMainWindow()        #生成选择文件窗口
        filedialog = QFileDialog(selectwindow, directory=currentpath)
        filedirectory = filedialog.getOpenFileName(selectwindow, '选择文件')
        #fname = os.path.split(filedirectory[0])
        #print(filedirectory)
        ExploitModule.UIreceive(self)
        ExploitModule.StartModule(mes[0], filedirectory)
        return


    def NullFunc(self):     #待扩展功能函数
        self.ui.outwindow.append(lettercolor.Mes + '[*]Waiting For Tool Update.' + ' >>> ' + \
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + lettercolor.ColorEnd)
        return



#下方为图形界面实例化代码
app = QApplication()
app.setWindowIcon(QIcon(currentpath + r'\Icon\tool.png'))

runmain = loadUI()
runmain.ui.show()

app.exec_()
