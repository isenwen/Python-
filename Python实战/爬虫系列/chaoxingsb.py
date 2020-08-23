from PyQt5 import QtCore
import sys, os, pymysql,base64
from json import loads
from requests import get
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, QLabel
from PyQt5.QtCore import QTimer



headers = {
    "Host": "106.52.197.16:8080",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    #'Cookie': 'UM_distinctid=16e63db9abc1eb-052985a15157e3-e343166-1fa400-16e63db9abd12a; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; PHPSESSID=uvvf71tsq8l2eeh0ci574k6931',
}


class Ui_MainWindow(QMainWindow):


    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 150)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 50, 310, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(150, 24, 120, 12))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")

        self.pushButton = QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(155, 95, 75, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralWidget)

        self.pushButton.clicked.connect(self.word_get)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "知到超星答案查询助手 准确率高达99%！"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "登陆验证【可试用】请输入帐号,请找管理员 索取"))
        self.label.setText(_translate("MainWindow", "请在下方输入您的帐号"))
        self.pushButton.setText(_translate("MainWindow", "登陆"))

    def mysql_connect2(self):
        db2 = pymysql.connect(host= " ", user="root", password="  ", database="info", port=3306)
        cursor2 = db2.cursor()
        sql2 = "select name,has_count from userinfo where name = %s"
        Miyao = self.lineEdit.text()
        sql1 = "select has_count from userinfo where name = %s"
        try:
            ret = cursor2.execute(sql2, Miyao)
            cursor2.execute(sql1, Miyao)
            has_count = int(cursor2.fetchone()[0])
            if ret and has_count >= 0:
                return True
            else:
                return False
        except:
            db2.rollback()
        finally:
            cursor2.close()
            db2.close()

    def word_get(self):
        flag = self.mysql_connect2()

        if flag:
            ui_hello.show()
            MainWindow.close()
            return True
        else:
            QMessageBox.warning(self,
                                "警告",
                                "密钥无效，请联系管理员获取",
                                QMessageBox.Yes)
            self.lineEdit.setFocus()


class QTextEditDemo(QWidget):
    def __init__(self):
        super(QTextEditDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("超星智慧树/慕课答题助手")
        self.resize(800, 600)
        self.textEdit1 = QTextEdit()
        self.textEdit2 = QTextEdit()
        self.buttonText1 = QPushButton("搜一下[单击即可，点多次不会快，甚至更慢]")
        self.label = QLabel("请在下方输入你想搜索的题目，然后点击“搜一下”即可")
        self.textEdit2.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit1)
        layout.addWidget(self.textEdit2)
        layout.addWidget(self.buttonText1)
        self.setLayout(layout)
        self.buttonText1.clicked.connect(self.onClick_ButtonText)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '注意',
                                     "您确定退出吗?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def onClick_ButtonText(self):
        count = self.get_count()
        if count > 0:
            # 1.获取编辑框1的内容
            self.title = self.textEdit1.toPlainText().replace(" ", "").replace("(","")\
                .replace(")", "").replace("，", "").replace("。", "").replace("？","")\
                .replace("！", "").replace("（", "").replace("）", "").replace(",","")\
                .replace("\n", "").replace("\t", "").replace("-", "").replace("_", "")


            if self.title!="":
                self.textEdit2.setPlainText("答案搜索中，请稍后")
                url = "http://106.52.197.16:8080/chaoxing_war/topicServlet?action=query&q=" + self.title
                html = get(url=url, headers=headers).text
                # 4.json格式化获取答案
                code = int(loads(html)["code"])
                self.title = str(loads(html)["question"]).replace("#", "-----")
                self.answer = str(loads(html)["data"]).replace("#", "-----")
                #有答案，不一定对，
                if code == 1 and self.answer !='见群里我发的图片':
                    self.textEdit2.setPlainText(self.answer)
                    self.textEdit1.setPlainText(self.title)
                    self.mysql_connect()

                # 没答案
                else:
                    self.answer = "暂未找到答案"
                    self.textEdit2.setPlainText(self.answer)

            else:
                self.textEdit2.setPlainText("老铁，编辑框1中您还没输入要查询的题目呢，别浪费查询次数了哦")

        else:
            self.textEdit2.setPlainText("抱歉，当前您的次数已用完，暂无法查询，请联系管理员获取，祝您使用愉快")

    # 保存答案
    def mysql_connect(self):
        db = pymysql.connect(host= " ", user="root", password="  ", database="info", port=3306)
        cursor = db.cursor()
        sql = "insert into tiku2(question,answer) values (%s,%s)"
        question = self.title
        answer = self.answer
        try:
            cursor.execute(sql, (question, answer))
            db.commit()
        except:
            db.rollback()
        finally:
            cursor.close()
            db.close()

    # 获取姓名
    def return_name(self):
        name = ui.lineEdit.text()
        return name

    # 获取剩余次数
    def get_count(self):
        Miyao = self.return_name()
        if Miyao != "":
            db = pymysql.connect(host= " ", user="root", password="  ", database="info", port=3306)
            cursori = db.cursor()
            cursorj = db.cursor()
            sql3 = "update userinfo set has_count = has_count -1 where name = %s "
            sql4 = "select has_count from userinfo where name = %s"
            try:
                cursori.execute(sql3, Miyao)
                cursorj.execute(sql4, Miyao)
                result = int(cursorj.fetchone()[0])
                db.commit()
                return result
            except:
                db.rollback()
            finally:
                cursori.close()
                cursorj.close()
                db.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui_hello = QTextEditDemo()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
