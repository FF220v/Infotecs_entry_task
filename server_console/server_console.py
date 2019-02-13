import sys
from logger import Logger
from server import ServerProc
import logging
import socket
from time import sleep
#main class of console shell
class Console():
    '''Mait console shell class'''
    def __init__(self):
        #getting logger
        self.logger = Logger.get_logger_by_name(__name__)
        self.server_running_flag = False

    def console_main(self):
        '''main method of console app'''
        print('Welcome to infotecs task server!')
        self.console_help()
        while True:
            print('\nWaiting for command:',end = '')        
            cmd = input().split()
            print('')
            if cmd[0] ==  'start':
                try:
                    self.start_server(int(cmd[1]))
                except:
                    print('Cannot run server, smth went wrong')

            elif cmd[0] == 'stop':
                self.stop_server()
            elif cmd[0] == 'exit':
                self.exit()
            elif cmd[0] == 'help':
                self.console_help()
            else:
                print('No such commmand. Try use "help" ')

    def console_help(self):
        '''prints help info'''
        print('start xxxx - start server on port xxxx\n\
stop - stop server\n\
help - show this message\n\
exit - stop server and exit')
    
    def check_socket(self, port):
        '''Function to check if socket is ok to run server'''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',port))
        return result

    def stop_server(self):
        '''Called when user initiates server shutdown'''
        self.logger.info('User attempted to close server')
        try:
            #Terminating subprocess 
            self.server_proc.terminate()
            self.logger.info('Server shutting down...')
        except:
            self.logger.info('Server is not running')
        self.server_running_flag = False

    def exit(self):
        self.stop_server()
        sys.exit()


    def start_server(self,port):
        self.logger.info('Starting server...')
        #if server is not running yet
        if not self.server_running_flag:
                #Trying to run server on selected port
            try:
                port_ready = self.check_socket(port = port)
                #if port is not OK, server won't run
                if(port>1023 and port<49152 and port_ready != 0):
                    self.server_proc = ServerProc(host = 'localhost', port= port)
                    self.server_proc.start()
                    self.logger.info('Server started. Print "localhost:'+str(port)+'" in browser to check')
                    self.logger.info('Check server logs in serverLog.txt')
                else:
                    if port_ready == 0:
                        self.logger.error('Port is busy.')
                    self.logger.error('Can not start server on this port.')
                    return
                sleep(1)
                self.server_running_flag = True
            except:
                #handling any unforseen situations
                self.logger.error('Failed starting server.')
        else:
            print('Server is already running. Stop server first')

if __name__ == '__main__':
     console = Console()
     console.console_main()
    
