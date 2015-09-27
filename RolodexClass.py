# Creates a class to ingest, hold, and output (JSON) address entries

import re
import json

class Rolodex():
   """ object to keep track of customer information """
   
   def __init__(self):
      """ create primary data objects """
      self.entry = []
      self.errors = []
      
      # precompile the regex for better performance as the count of entries goes up
      self.phone_regex = re.compile(r', (\d{3} \d{3} \d{4})|(\(\d{3}\)-\d{3}-\d{4})')
      self.color_regex = re.compile(r', ([^A-Z][a-z]+)')
      self.names_regex = re.compile(r'([A-Z][a-z.]+)')
      self.zipcode_regex = re.compile(r', (\d{5})')

            
   def get_data(fname = 'data.in'):
      """ read data from filename """
      with open('data.in') as f:
         lines = f.readlines()
      return lines

   
   def extract_info(self, lines_of_info):
      """ use regex to pull data from each line in large string object """
      
      linenum = 0
      for line in lines_of_info:
         
         zipcode = self.zipcode_regex.search(line)
         names = self.names_regex.findall(line)
         phone = self.phone_regex.search(line)
         color = self.color_regex.search(line)
         
         # if all objects were found we have a valid entry
         if all([zipcode, names, phone, color]):
            self.add_info(zipcode, names, phone, color)
         else:
            self.errors.append(linenum)
         
         linenum += 1

   def add_info(self, zipcode, names, phone, color):
      """ takes regex objects and returns a dictionary object """
      self.entry.append({
         "firstname" : " ".join(names[:-1]),
         "phonenumber" : phone.group(),
         "zipcode" : zipcode.group(1),
         "color" : color.group(1),
         "lastname" : names[-1]
      })
      
   def build_rolodex(self, dict_entry_array, errors_array):
      """ combines the two dictionary objects into a single dictionary object """
      return { "entries" : dict_entry_array, "errors" : errors_array }
   
   def sort_on_key(self, key_to_sort = "lastname"):
      """ returns a sorted version of dictionary based on key_to_sort """
      return sorted(self.entry, key=lambda k: k[key_to_sort])
   
   def output_JSON(self):
      """ return JSON object built from build_rolodex """
      return json.dumps(
         self.build_rolodex(self.sort_on_key(), self.errors), 
         sort_keys=True, indent=2)
      

# Actually run the code
if __name__ == "__main__":
   
   rolo = Rolodex()
   lines = rolo.get_data()
   rolo.extract_info(lines)
   
   print rolo.output_JSON()
   
   