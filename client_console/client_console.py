import sys
from logger import Logger
import logging
from urllib import request

class Console():
    '''Mait UI class'''
    def __init__(self):
        self.logger = Logger.get_logger_by_name(__name__)
        self.connected = False
    def console_main(self):
        '''main method of console app'''
        print('Welcome to infotecs task server!')
        self.console_help()
        while True:
            print('\nWaiting for command:',end = '')        
            cmd = input().split()
            print('')
            if cmd[0] ==  'connect':
                try:
                   self.connect(cmd[1],cmd[2])
                except:
                    print(cmd[1])
                    print(cmd[2])
                    print('invalid input')
            elif cmd[0] == 'factors':
                try:
                    self.factors(int(cmd[1]))
                except:
                    print('invalid input')
            elif cmd[0] == 'exit':
                self.exit()
            elif cmd[0] == 'help':
                self.console_help()
            else:
                print('No such commmand. Try use "help" ')

    def connect(self, address, port):
        #Checking if port was specified
        if port == None:
            url = 'http://'+address
        else:
            url = 'http://'+address+':'+port
        #Trying to connect to server and ask for its id
        try:
            self.logger.info('Asking "'+url+'" for id')
            id_ = request.urlopen(url+'/auth',timeout = 1).read().decode('utf-8')
            #if id is correct loads the main page
            if id_ == 'hello':
                self.logger.info('id "'+id_+'" is correct. Connected to server.')
                self.connected = True
                self.url = url
            else:
                self.logger.info('id "'+id_+'" is incorrect.')
        except:
            self.logger.info('Can not connect to this adress')
    
    def factors(self, value):
        if self.connected == True:
            try:
                print(request.urlopen(self.url+'/console?value='+str(value),timeout = 1).read().decode('utf-8'))
            except:
                print('Unable to connect server. Please reconnect')
        else:
            print('Please connect to server first')
            self.connected = False

    def console_help(self):
        '''prints help info'''
        print('connect adress port - connects to server with adress "adress"\n\
                      on port "port"\n\
factors x - send value x to server to be prime factorized\n\
exit - exit client\n\
help - show this message')



if __name__ == '__main__':
    console = Console()
    console.console_main()