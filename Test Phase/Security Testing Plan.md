# Security Testing Plan
The 2 areas that need testing were:
- input_valid_str()
- general_check()

## String Validation:
To test to make sure the string validation is working properly we will create a function that loops through all the restricted characters (all non alpha characters besides +) and see if the validation picks them up properly. Furthermore, we will be starting with the proper string "Data+Scientist", and replace a letter each time with the restricted character, moving further along the string, restarting once we get to the end in case different placements bug it out and allow it through.

## General Check:
In order to check to make sure this works we will create a function that feeds it a mix of functions that fail automatically and functions that work, ensure that general check catches everything that it needs to, throwing the designated errors as well.
