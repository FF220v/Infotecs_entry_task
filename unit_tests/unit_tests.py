import sys
sys.path.insert(1,'./Server/modules')
import unittest
from urllib import request
from server import Server, ServerProc
from time import sleep

class Tests(unittest.TestCase):
    #test if factorization function can factorize
    def test_factorization(self):
        server = Server()
        
        test_1 = server.factorize(2)
        test_2 = server.factorize(3)
        test_3 = server.factorize(4)
        test_4 = server.factorize(12345)

        self.assertTrue(test_1 == [2])
        self.assertTrue(test_2 == [3])
        self.assertTrue(test_3 == [2,2])
        self.assertTrue(test_4 == [3, 5, 823])

    #test if server able to response
    def test_server(self):
        server_proc = ServerProc(host = 'localhost', port = 8080)
        server_proc.start()
        sleep(1)
        try:
            id_ = request.urlopen(url = 'http://localhost:8080/auth',timeout = 3).read().decode('utf-8')
        except:
            id_ = 'incorrect'
        server_proc.terminate()
        try:
            os.remove('./serverLog.txt')
        except:
            pass
        self.assertTrue(id_=='hello')

if __name__ =='__main__':
   unittest.main()