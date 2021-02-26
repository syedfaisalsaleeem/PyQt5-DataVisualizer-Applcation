from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from helper import run_query

class TopLearningSection():
    def __init__(self):
        pass

    def is_paid_user(self):
        try:
            sql_query = f'''
                select * from user_info
            '''
            data = run_query(sql_query)
            if(data['package'][0] != "free" and data['package'][0] != "Free"):
                return True
            else:
                return False
        except:
            return False
    def setup(self,vbox):#widget,text
        self.vbox = vbox
        self.vbox.setContentsMargins(0,0,0,0)
        self.t1 = QWidget()
        self.t1.setFixedHeight(40)
        self.effect = QGraphicsDropShadowEffect(self.t1)
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(10)
        self.t1.setGraphicsEffect(self.effect)
        self.t1.setStyleSheet('background:#E0E2E7')
        self.vbox.addWidget(self.t1)
        self.hbox = QHBoxLayout()

        ## 2 min video tutorial button
        self.button = QPushButton("See 2 min video tutorial")
        self.button.setStyleSheet('''
        QPushButton
        {
            color:black;
            border:0;

        }
        QPushButton:hover
        {
            color: #4A76FD;
            
        }'''
            )
        self.button.clicked.connect(self.open_url)
        f = QFont('Arial')
        f.setPixelSize(18)
        f.setUnderline(True)
        self.button.setFont(f)
        self.hbox.addWidget(self.button)
        self.hbox.addStretch(1)
        check_user = self.is_paid_user()
        if(check_user==False):
            ##Upgrade button on top
            self.upgradebutton = QPushButton("Upgrade VizPick")
            self.upgradebutton.setStyleSheet('''
            QPushButton
            {
                color:black;
                border:0;

            }
            QPushButton:hover
            {
                color: #4A76FD;
                
            }'''
                )
            self.upgradebutton.clicked.connect(self.open_url)
            f = QFont('Arial')
            f.setPixelSize(18)
            f.setUnderline(True)
            self.upgradebutton.setFont(f)
            self.hbox.addWidget(self.upgradebutton)


        self.t1.setLayout(self.hbox)
    
    def setup1(self,vbox):#widget,text
        self.vbox = vbox
        # self.vbox.setContentsMargins(0,0,0,0)
        self.t1 = QWidget(self.vbox)
        self.t1.setGeometry(0,0,400,50)
        self.effect = QGraphicsDropShadowEffect(self.t1)
        self.effect.setOffset(0, 0)
        self.effect.setBlurRadius(10)
        self.t1.setGraphicsEffect(self.effect)
        self.t1.setStyleSheet('background:#E0E2E7')
        
        # self.vbox.addWidget(self.t1)
        self.hbox = QHBoxLayout()
        self.button = QPushButton("See 2 min video tutorial")
        self.button.setStyleSheet('''
        QPushButton
        {
            color:black;
            border:0;

        }
        QPushButton:hover
        {
            color: #4A76FD;
            
        }'''
            )
        self.button.clicked.connect(self.open_url)
        f = QFont('Arial')
        f.setPixelSize(18)
        f.setUnderline(True)
        self.button.setFont(f)
        self.hbox.addWidget(self.button)
        self.hbox.addStretch(1)
        self.t1.setLayout(self.hbox)

    def open_url(self):
        import webbrowser
        
        webbrowser.open('https://vizpick.com/videos/')
        