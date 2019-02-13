import sys
from PyQt5 import QtWidgets,QtWebEngineWidgets,QtCore
from logger import Logger
import logging
from urllib import request
#A class used to redirect logs to text field
class QTextEditLogger(logging.Handler):
    '''Class is used to redirect
    logs to text field'''
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class UI(QtWidgets.QWidget):
    '''Mait UI class'''
    def __init__(self, parent=None):
        #Initializing with parent class constructor
        super().__init__(parent)

        #Some window parameters
        self.setMinimumSize(640,350)
        self.setWindowTitle('Infotecs task client')

        #Setting up logger text box
        self.logger = Logger.get_logger_by_name(__name__)
        self.logger.info('Initializing UI')
        log_text_box = QTextEditLogger(self)
        log_text_box.setFormatter(logging.Formatter(Logger.format_))
        logging.getLogger().addHandler(log_text_box)
        log_text_box.widget.setFixedHeight(75)

        #Setting up elements of window
        self._button = QtWidgets.QPushButton(self)
        self._button.setText('Connect')
        self._button.setFixedSize(100,30)
        self._button_state = True

        self._port_text = QtWidgets.QTextEdit('8080')
        self._port_text.setFixedSize(125,25)
        self._port_label = QtWidgets.QLabel('Port: ')
        self._port_label.setFixedSize(30,30)

        self._host_text = QtWidgets.QTextEdit('localhost')
        self._host_text.setFixedSize(125,25)
        self._host_label = QtWidgets.QLabel('Host: ')
        self._host_label.setFixedSize(30,30)

        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.web_view.close()
    
        #Placing elements on layouts to make them look cute
        main_layout = QtWidgets.QGridLayout()
        sub_layout = QtWidgets.QGridLayout()
        port_layout = QtWidgets.QHBoxLayout()
        host_layout = QtWidgets.QHBoxLayout()

        port_layout.addWidget(self._port_label)
        port_layout.addWidget(self._port_text)
        
        host_layout.addWidget(self._host_label)
        host_layout.addWidget(self._host_text)

        sub_layout.addWidget(self._button,0,0)
        sub_layout.addLayout(port_layout,0,2)
        sub_layout.addLayout(host_layout,0,1)
        main_layout.addWidget(self.web_view,0,0)
        main_layout.addWidget(log_text_box.widget,1,0)
        main_layout.addLayout(sub_layout,2,0)
        self.setLayout(main_layout)

        #Setting button handler function
        self._button.clicked.connect(self.button_handler)
        self.logger.info('UI initialized.')

    def closeEvent(self, event):
        '''Called when user press cross'''
        self.logger.info('User closed application.')
        self.web_view.close()
        event.accept()
        
    #Handles connect button
    def button_handler(self):
        self._button.setEnabled(False)
        self._host_text.setEnabled(False)
        self._port_text.setEnabled(False)
        #Checking if port was specified
        port = self._port_text.toPlainText()
        if port == None:
            url = 'http://'+self._host_text.toPlainText()
        else:
            url = 'http://'+self._host_text.toPlainText()+':'+port
        #Trying to connect to server and ask for its id
        try:
            self.logger.info('Asking "'+url+'" for id')
            id_ = request.urlopen(url+'/auth',timeout = 1).read().decode('utf-8')
            #if id is correct loads the main page
            if id_ == 'hello':
                self.logger.info('id "'+id_+'" is correct. Openning server page...')
                self.web_view.setUrl(QtCore.QUrl(url))
            else:
                self.logger.info('id "'+id_+'" is incorrect.')
        except:
            self.logger.info('Can not connect to this adress')
        self._button.setEnabled(True)
        self._host_text.setEnabled(True)
        self._port_text.setEnabled(True)
       

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.show()
    app.exec()
