# Security Testing Overview
## Tests
There will be 3 tests that need carried out in order to ensure that everything is in order:
#### - Test string validation for the keywords and location prompts
#### - Testing to make sure the general check catches errors correctly and displays correct prompts

### String Validation:
This is to ensure that the input_valid_str() function works correctly, not allowing any digits or special characters (besides the + sign). The only inputs allowed are letters, capital or otherwise, and the aforementioned + sign. Spaces are not allowed.

### General Check:
This function is designed as a way to check to make sure the external module functions, as well as some other functions operate properly, and if they don't, it allows the program to nto crash, and instead throw an error console to the window.
