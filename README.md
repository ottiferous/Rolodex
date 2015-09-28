# Introduction

Included in this folder is the code to run the program 'RolodexClass.py', the sample input file included 'data.in' and the result of the code execution 'result.out'. Usage is `python RolodexClass.py` and can optionally take an argument in the form of a file name e.g. `python RolodexClass.py otherinput.in`.

The file 'TestRolodexClass.py' and 'test.in' are used for testing the Rolodex class. Usage is simply `python TestRolodexClass.py`

#Overview

The Rolodex class handles ingesting a csv formatted file and outputting a JSON object to a file.

Each line is parsed via a regular expression to extract properly ( or mostly properly ) formatted information such as names, zipcodes, phone numbers, and a color.

The criteria for each regex is as follows:

### Phone Regex
Will pull out phone numbers in the standard formats (xxx)-xxx-xxxx, xxx-xxx-xxxx, as well as handle an optional country code at the start +1 xxx-xxx-xxxx. The regex will work with any whitespace, dots, or dash characters. The most time was spent on this portion as phone numbers were used to determien whether a line was valid or not.

### Color Regex
Finds a combination of only letters that are not capitalized. In the sample data only people's names had capitalized letters so we look for one or more words with all lower case letters after a comma

### Zipcode Regex
Arguably the easiest regular expression - it looks for a field with 5 digits, and only 5 digits. It does not check for valid zipcode

### Names Regex
This looks for words that start with a capitalization, and can include a single non-letter character to allow for hyphenated names and middle initials being used. Some lines will have the name in a single field, while others have it in two separate fields. This is why the .findall() method is used to extract the names regardless of which field they are in.

Once the information is extracted, if any fields are missing from a line the line number (0th indexed) is added to the 'errors' tally and the program continues execution. If no information is missing, a helper method will cleanup the phone number ( normalizing it to the standard xxx-xxx-xxxx format ) and then assigns all fields to a dictionary object within the class.

### Outputting JSON
Once all of the data is ingested 4 methods work in tandem to construct a single large ditionary from the entries array and the errors array, that dictionary is sorted as a list and returned to be outputed as a JSON formatted object to 'result.out' unless another file is specified.

## Further Info
A git repository can be found at https://github.com/ottiferous/Rolodex for more insight into the creation process of this project.