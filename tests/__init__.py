import unittest
import os
import string
import random
import threading
import subprocess

from modules.users import Users

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def celery_run() -> None:
            subprocess.run(['python3', '-m', 'celery', '-A', 'tasks.main', 'worker', '--concurrency=10', '--queues=high_priority'])
            return
        
        th = threading.Thread(target=celery_run)
        th.start()
        
    def __generate_random_string(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(7))
        
    def setUp(self):
        self.ref = None
        self.email = self.__generate_random_string() + '@gmail.com'
        
    def test_1_insert_user(self):
        with Users() as module:
            insert_user_response = module.insert_user(self.ref, self.email)
        
        response = insert_user_response.get('status') if isinstance(insert_user_response, dict) else 'error'
            
        self.assertTrue(response == 'success')
        
        if response == 'success':
            Test.ref = insert_user_response.get('user', {}).get('refferal', None)
        
    def test_2_repeat_insert_user(self):
        ref = Test.ref
        
        with Users() as module:
            insert_user_response = module.insert_user(ref, self.email)
        
        response = insert_user_response.get('status') if isinstance(insert_user_response, dict) else 'error'
            
        self.assertTrue(response == 'success')
        
    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
