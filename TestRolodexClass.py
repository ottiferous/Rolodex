import unittest
from RolodexClass import Rolodex

class MockRegexGroup():
   """ pretends to be regex group matches """
   def __init__(self):
      self.numbers = []
   
   def __iter__(self):
      return iter(self.numbers)
         
   def assign(self, data):
      """ sets the mock data """
      self.numbers = data
   
   def group(self, index):
      """ return the index of array at number """
      return self.numbers[index] if index < len(self.numbers) else None
      

class TestRolodexClass(unittest.TestCase):
   """ Rolodex Test Case """
         
   def setUp(self):
      """ creates a new class objcet for testing """
      print 'Creating a class object'
      self.TRolodex = Rolodex()
   
   def test_get_data(self):
      """ ensure file contents are loaded correctly into a string """
      print "checking Rolodex:get_data('test.in')"
      testFileContents = ['There\n', 'are\n', '3 lines']
      self.assertEqual(self.TRolodex.get_data('test.in'), testFileContents)
   
   def test_extract_info(self):
      """ ensure regex pulls correct info from line """

      test_lines_of_info = [
         "Abbey Goode, driftwood, 97148, 488 084 5794",
         "Skywalker, Luke, (555)-555-5555, gray, 70646",
         "GLaDOS, Computer, 73149, 4549346454, pink",
         "Gordon, Freeman, 39358, 489634 9504, orange",
         "Linda, Blair, (4634)-118-2451, red, 07256",
         "Hand, Robert, (054)-813-60330, green, 47784",
         "Lee, Bruce, 087.853.4995, black, 44359"
      ]
      self.TRolodex.extract_info(test_lines_of_info)
      error_num = self.TRolodex.len_of_errors()
      self.assertEqual(error_num, 1)
      
   def test_normalize_phone(self):
      """ attempt to normalize different formats of valid phone numbers """

      test_phones = ["488 084 5794", "(555)-555-5555", "4549346454", "489634 9504"]
      expected_result = ["488-084-5794", "555-555-5555", "454-934-6454", "489-634-9504"]
      
      phone = MockRegexGroup()
      phone.assign(test_phones)
      result = []
      for each in phone:
         result.append(self.TRolodex.normalize_phone(each))
      
      self.assertEqual(result, expected_result)
      
   def test_add_info(self):
      """ checks that the values are assigned """
      
      self.TRolodex.add_info("12345", ["Wilford", "Brimley"], "123-456-7890", "silver")
      
      self.assertEqual(self.TRolodex.len_of_entry(), 1)
      self.assertEqual(self.TRolodex.entry[0]["firstname"], "Wilford")
      self.assertEqual(self.TRolodex.entry[0]["lastname"], "Brimley")
      self.assertEqual(self.TRolodex.entry[0]["zipcode"], "12345")
      self.assertEqual(self.TRolodex.entry[0]["phonenumber"], "123-456-7890")
      self.assertEqual(self.TRolodex.entry[0]["color"], "silver")
      
if __name__ == '__main__':
   unittest.main()