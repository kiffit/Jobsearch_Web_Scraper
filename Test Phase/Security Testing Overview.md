# Security Testing Overview
## Tests
There will be 3 tests that need carried out in order to ensure that everything is in order:
#### - Test string validation for the keywords and location prompts
#### - Testing to make sure the general check catches errors correctly and displays correct prompts
#### - Testing to make sure the CSV code has the correct failsafes in case anything goes wrong

### String Validation:
This is to ensure that the input_valid_str() function works correctly, not allowing any digits or special characters (besides the + sign). The only inputs allowed are letters, capital or otherwise, and the aforementioned + sign. Spaces are not allowed.

### General Check:
This function is designed as a way to check to make sure the external module functions, as well as some other functions operate properly, and if they don't, it allows the program to nto crash, and instead throw an error console to the window.

### CSV Files
Most security issues with the CSV file would be code based, with allowing user input to be directly added, with no sanitatization and/or directly in the lines with the file open. These issues can be prevented pretty easily with proper coding practices. However, we can test the failsafes on the opening and closing of the file to ensure that the data does not accidentily get corrupted from them.
