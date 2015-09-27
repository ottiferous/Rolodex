import re
import json

fname = 'data.in'

# grab all lines of the file as an array
with open(fname) as f:
   lines = f.readlines()

entry, errors = [], []
linenum = 0

for line in lines:
   
   # use re.compile since we will be using the regex's a lot
   
   # 5 digits and always preceded by a comma
   zipcode = re.search(r', (\d{5})', line)
   # 123 456 7890 pattern or (123) 456-7890 pattern preceded by comma
   phone = re.search(r', (\d{3} \d{3} \d{4})|(\(\d{3}\)-\d{3}-\d{4})', line)
   # finds all capitalized words in line and the '.' char (returns list)
   names = re.findall(r'([A-Z][a-z.]+)', line)
   # always lower case and preceded by comma
   color =  re.search(r', ([^A-Z][a-z]+)', line)
      
   if all([phone, names, color, zipcode]):
         entry.append({
            "color"        : color.group(1),
            "firstname"    : " ".join(names[:-1]),
            "lastname"     : names[-1],
            "phonenumber"  : phone.group(1),
            "zipcode"      : zipcode.group(1)
         })
   else:
      errors.append(linenum)
      
   linenum += 1

final = { "entries" : entry, "errors" : errors }

# output should eventually be alphabetized by lastname, firstname
# try creating a list of the sorted dict like they do here:
# http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
print json.dumps(final, sort_keys=True, indent=2)