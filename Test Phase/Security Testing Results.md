# Security Testing Results

## String Validation
After testing each possible input besides the alphabet and the + sign, in all different possible spots, it appears that the string validation function is working correctly and as intended. This was tested using the check_input_valid() function in the test code. Testing a normal correct string vs all 47 other restricted characters, getting one True result (the correct string) and 47 False results (other restricted characters).

## General Check
After testing the function with both functions that raise exceptions and work correctly, it appears the general check function is working correctly and as intended. This was tested using the check_general_valid() functions. This was achieved by creating 2 vanilla functions, labeled good_func() and bad_func(), and creating a list with a specified amount of entries. The entries are determined randomly each time, with each entry having a random chance to either be the good func vs the bad func and ensuring that they matched.
