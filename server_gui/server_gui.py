import sys
from PyQt5 import QtWidgets
from logger import Logger
from server import ServerProc
import logging
import socket

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
        self.setMinimumSize(640,280)
        self.setWindowTitle('Infotecs task server')

        #Setting up logger text box
        self.logger = Logger.get_logger_by_name(__name__)
        self.logger.info('Initializing UI')
        log_text_box = QTextEditLogger(self)
        log_text_box.setFormatter(logging.Formatter(Logger.format_))
        logging.getLogger().addHandler(log_text_box)

        #Setting up elements of window
        self._button = QtWidgets.QPushButton(self)
        self._button.setText('Start server')
        self._button.setFixedSize(100,30)
        self._button_state = True

        self._port_text = QtWidgets.QTextEdit('8080')
        self._port_text.setFixedSize(125,25)
        self._port_label = QtWidgets.QLabel('Port: ')
        self._port_label.setFixedSize(30,30)

        #Placing elements on layouts to make them look cute
        main_layout = QtWidgets.QGridLayout()
        sub_layout = QtWidgets.QGridLayout()
        port_layout = QtWidgets.QHBoxLayout()

        port_layout.addWidget(self._port_label)
        port_layout.addWidget(self._port_text)

        sub_layout.addWidget(self._button,0,0)
        sub_layout.addLayout(port_layout,0,1)

        main_layout.addWidget(log_text_box.widget,0,0)
        main_layout.addLayout(sub_layout,1,0)
        self.setLayout(main_layout)

        #Setting button handler function
        self._button.clicked.connect(self.button_handler)
        
        self.logger.info('UI initialized.')

    def check_socket(self, port):
        '''Function to check if socket is ok to run server'''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',port))
        return result

    def closeEvent(self, event):
        '''Called when user press cross'''
        self.logger.info('User closed application.')
        try:
            #Terminating subprocess on closing application 
            self.server_proc.terminate()
            self.logger.info('Server shutting down...')
        except:
            pass
        event.accept()
        

    def button_handler(self):
        '''A function to start of stop server
        on a button click'''
        #Deactivating elements to avoid multiple press
        self._button.setEnabled(False)
        self._port_text.setEnabled(False)
        if self._button_state == True:
            self.logger.info('Starting server...')
            #Trying to run server on selected port
            try:
                port = int(self._port_text.toPlainText())
                port_ready = self.check_socket(port = port)
                #if port is not OK, server won't run
                if(port>1023 and port<49152 and port_ready != 0):
                    self.server_proc = ServerProc(host = 'localhost', port= port)
                    self.server_proc.start()
                    self._button.setText('Stop server')
                    self.logger.info('Server started. Print "localhost:'+str(port)+'" in browser to check')
                    self.logger.info('Check server logs in .\serverLog.txt')
                    self._port_text.setEnabled(False)
                    self._button_state = False
                else:
                    if port_ready == 0:
                        self.logger.error('Port is busy.')
                    self.logger.error('Can not start server on this port.')
                    self._button.setEnabled(True)
                    self._port_text.setEnabled(True)
                    return
            except:
                #handling any unforseen situations
                self.logger.error('Failed starting server.')
                self._port_text.setEnabled(True)
                self._button_state = True

        else:
            #shutting down server
            self.logger.info('Server shutting down...')
            self.server_proc.terminate()
            self._button_state = True
            self._button.setText('Start server')
            self._port_text.setEnabled(True)
        #making button pressable again
        self._button.setEnabled(True)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.show()
    app.exec()
