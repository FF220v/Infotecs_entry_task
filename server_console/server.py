import sys
from bottle import Route, request, Bottle, run as runBottle
from multiprocessing import Process
from logger import Logger
import os


class Server(Bottle):
    '''Server module implements functions of web server
    which is able to interract with user via web page.
    It also has all needed functions for prime factorization
    of integer positive values built in'''

#Here we have big string constants which are сommonly used
    outputText = 'Output will be here'
    inputText = 'Input will be here'
    page_text = '<title>Infotecs task</title>\
            <b>Hello! This is page of infotecs python task solution!</b><p>\
            This application can prime factorize a given value<p>\
            <form action="/" method="post">\
            Input positive integer value: <input name="val" type="text" />\
            <input value="Send" type="submit" />\
            </form><p>'

    def __init__(self):
        '''initialization of logger'''
        Logger.def_logger_file('serverLog.txt')
        self.log = Logger.get_logger_by_name(__name__)
        self.log.info('Initializing server...')
        Bottle.__init__(self)
        
        #Binding route-methods to web page paths
        route_auth = Route(app = self, rule='/auth', method='GET',
             callback=self._auth_get, name='auth')

        route_get = Route(app = self, rule='/', method='GET',
             callback=self._index_get, name='index')

        route_post = Route(app = self, rule='/', method='POST',
             callback=self._index_post, name='index')
        
        route_console = Route(app = self, rule='/console', method='GET',
             callback=self._console_get, name='console')

        self.add_route(route_auth)
        self.add_route(route_get)
        self.add_route(route_post)
        self.add_route(route_console)

        #Parent constructor of Thread class. Setting run
        #function of bottle server as target

        self.log.info('Server initialized.')
        
    
    def factorize(self, val):
        '''Prime-factorizing function,
        Eratosphenes sieve algorithm implementation'''
        fac = 2
        factors = []
        while fac * fac <= val:
            while val % fac == 0:
                factors.append(fac)
                val = val / fac
            fac = fac + 1
        if val > 1:
            factors.append(int(val))
        return factors

    def _auth_get(self):
        '''Returns a special identifier, so client can be sure
        that it is correct server'''
        self.log.info('Somebody asked for id')
        return str('hello')

    def _index_get(self):
        '''This function will be executed on GET request to root path of web page
        Sends default page back to user'''
        self.log.info('Incoming GET request, sending default page...')
        return self.page_text+'Input: '+self.inputText+'<br>Output: '+self.outputText

    def _console_get(self):
        '''This function will be executed on GET request to console path'''
        self.log.info('Incoming console GET request, sending answer ...')
        val = request.GET.get('value', '').strip()
        try:
            self.log.info('Incoming console request, processing incoming data: '+val)
        except:
            self.log.info('Incoming console request, processing incoming data...')
        try:
            val = int(val)
            if val <= 1:
                raise IOError(' ')
            factors = self.factorize(int(val))
            self.log.info('Results calculated:'+str(factors)+', sending...')
            return 'Input:  '+str(val)+', \nOutput: '+str(factors)
        except:
            self.log.info('Something went wrong. Sending error page...')
            return 'Error! You sent incorrect value. Value must be positive integer > 1.'

    def _index_post(self):
        '''This function will be executed on POST request to root path of web page
          Sends page with processed data to user or error info'''
        val = request.forms.get('val')
        try:
            self.log.info('Incoming POST request, processing incoming data: '+val)
        except:
            self.log.info('Incoming POST request, processing incoming data...')
        try:
            val = int(val)
            if val <= 1:
                raise IOError(' ')
            factors = self.factorize(int(val))
            self.log.info('Results calculated:'+str(factors)+', sending...')
            return self.page_text+'Input:  '+str(val)+'<br>Output: '+str(factors)
        except:
            self.log.info('Something went wrong. Sending error page...')
            return self.page_text+'Input:  '+self.inputText+'<br>Output: '+\
                self.outputText+'<p>Error! You sent incorrect value. Value must be positive integer > 1.'

class ServerProc(Process):
    '''Special class, used to run bottle server in a dedicated process, so
    we are able to terminate it whenever we like'''
    def __init__(self,host,port):
        Process.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        server = Server()
        runBottle(app = server, host = self.host, port = self.port)

#If server is started as main function, simply starting the server
if __name__ == "__main__":
    server = Server()
    runBottle(app = server, host = 'localhost', port = 8080)
