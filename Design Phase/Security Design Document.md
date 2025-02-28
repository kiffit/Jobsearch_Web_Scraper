# Security Design Document
## Assets to Consider
- CSV File Containing the completed job search queries
- Main executable program

## Threats to Assets
### CSV
- Improper Overwriting
- File Corruption

### Main Executable
- Malware
- Malicious Users
- Pages Being Scraped

## Security Measures
### CSV
- Open file with try and except to handle any errors with opening and corruption
- Prevent user from writing directly to the file
- Only open file when it becomes necessary to the program
- Close file as soon as it is no longer necessary in the program
- Try and except the writing to the file to help prevent some break cases that might write corrupted data

### Main Executable
- Try and except all input to handle, format, and validate all data correctly
- Try and except the opening of a website to prevent any issues with our program crashing or otherwise from the site being unable to load
- User given very limited access to limit any accidental or malicious problems cause by the user
- Clean, extract and format data from HTML to only pull data necessary to our program, limiting any issues with the data

## Security Summary
Overall, the security should be relatively easy for our project. We have limited interaction with the user, and our biggest concern is the websites we are scraping. As long as we sanitize all of our inputs, and correctly follow good techniques for opererating with a CSV file, we should not have much concern on the security side. However, the aforementioned security measures should help limit the concerns we do have.

### **[Click here to go back to Home](https://github.com/kiffit/waterfall-project)**
