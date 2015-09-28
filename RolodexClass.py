#! /usr/bin/python
# created by: Andrew Marrone on September 27th, 2015 

import sys
import re
import json

class Rolodex():
   """ object to keep track of customer information """
   
   def __init__(self):
      """ create primary data objects """
      self.entry = []
      self.errors = []
      
      # precompile expressions for better performance as the count of entries increases
      self.phone_regex = re.compile(r', (\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}')
      self.color_regex = re.compile(r', ([^A-Z][a-z]+)')
      self.names_regex = re.compile(r'([A-Z][a-z.]+)')
      self.zipcode_regex = re.compile(r', (\d{5})')

   def len_of_entry(self):
      """ return the number of entries in entry """
      return len(self.entry)
   
   def len_of_errors(self):
      """ returns the number of entries in error """
      return len(self.errors)
   
   def get_data(self, fname="data.in"):
      """ read data from filename """
      with open(fname) as f:
         lines = f.readlines()
      return lines
   
   def extract_info(self, lines_of_info):
      """ use regex to pull data from each line in large string object """
      linenum = 0
      for line in lines_of_info:
         
         zipcode = self.zipcode_regex.search(line)
         names = self.names_regex.findall(line)
         color = self.color_regex.search(line)
         phone = self.phone_regex.search(line)
                  
         # make sure all entries were found on a line before processing
         if all([zipcode, names, phone, color]):
            phone_string = self.normalize_phone(phone.group())
            self.add_info(zipcode.group(1), names, phone_string, color.group(1))
         else:
            self.errors.append(linenum)
         
         linenum += 1
         
   def normalize_phone(self, phone):
      """ returns normalized phone number in xxx-xxx-xxxx format """
      n = re.sub("[^0-9]", "", phone)
      return n[:3] + "-" + n[3:6] + "-" + n[6:]
      
   def add_info(self, zipcode, names, phone, color):
      """ takes regex objects and returns a dictionary object """
      self.entry.append({
         "firstname" : " ".join(names[:-1]),
         "lastname" : names[-1],
         "phonenumber" : phone,
         "zipcode" : zipcode,
         "color" : color
      })
      
   def build_rolodex(self, dict_entry_array, errors_array):
      """ combines the two dictionary objects into a single dictionary object """
      return { "entries" : dict_entry_array, "errors" : errors_array }
   
   def sort_on_keys(self, primary_sort = "lastname", secondary_sort = "firstname"):
      """ returns a sorted version of dictionary based on a primary and secondary key """
      return sorted(self.entry, key=lambda k: (k[primary_sort], k[secondary_sort]))
   
   def format_JSON(self):
      """ return JSON object built from build_rolodex """
      return json.dumps(
         self.build_rolodex(self.sort_on_keys(), self.errors), 
         sort_keys=True, indent=2)

   def write_file(self, out_file='result.out'):
      """ write contents to out_file """
      f = open(out_file, 'w+')
      f.write(self.format_JSON())
      

# Usage: python RolodexClass.py <filename_for_input>
if __name__ == "__main__":
   
   # input filename is optional
   if (sys.argv[:-1] is not None) and (len(sys.argv) > 1):
      filename = sys.argv[:-1]
   else:
      filename = 'data.in'
   
   rolo = Rolodex()
   lines = rolo.get_data(filename)
   rolo.extract_info(lines) 
   rolo.write_file()