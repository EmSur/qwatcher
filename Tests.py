'''
Created on 1 May 2015

@author: U6019794
'''
import unittest  

from datetime import date, datetime
from qwatcher import _isWorktime

class Test(unittest.TestCase):


    def test_isWorktime_weekdays(self):
        date = datetime(2015, 4, 27, 12,0) # Monday
        Test.assertTrue(self, _isWorktime(date), "Monday 12:00 has failed to be recognized as ")

        date = datetime(2015, 4, 28, 12,0) # Tuesday
        Test.assertTrue(self, _isWorktime(date), "Tuesday 12:00 has failed to be recognized as ")        

        date = datetime(2015, 4, 29, 12,0) # Wednsday
        Test.assertTrue(self, _isWorktime(date), "Wednsday 12:00 has failed to be recognized as ")
                        
        date = datetime(2015, 4, 30, 12,0) # Thursday
        Test.assertTrue(self, _isWorktime(date), "Thursday 12:00 has failed to be recognized as " )  
                        
        date = datetime(2015, 5, 1, 12,0) # Friday
        Test.assertTrue(self, _isWorktime(date), "Friday 12:00 has failed to be recognized as "  )

        date = datetime(2015, 5, 2, 12,0) # Saturday
        Test.assertFalse(self, _isWorktime(date), "Saturday 12:00 has failed to be recognized as " ) 
                        
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()