
'''
    *Fontcolor setting.
    *You can import this module to change fontcolor.
    *Auther:shiro
'''


class FontColor:
    def __init__(self):
        self.Warn = '''<font color=\"#FF0000\">'''       #警告提示（消极方面）
        self.Mes = '''<font color=\"#808000\">'''        #信息提示（参数提示等，中立方面）
        self.Res = '''<font color=\"#EE82EE\">'''        #结果提示（积极方面）
        self.ColorEnd = '''</font>'''


def ChangeColor():
    lettercolor = FontColor()
    return lettercolor

