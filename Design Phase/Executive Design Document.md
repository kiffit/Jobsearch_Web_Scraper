## Executive Design Document
#### Things to consider
- Classes
- Objects
- Data formats
- User interactions
- Data Flows
- Process Information
- Data Sink Formatting and Information

#### Design
- There will be no classes we will use a main driver and just the resourceful libraries that we have found to complete the project at hand. Since there is no other classes, there will also be no object oriented programming at all.
- Main entities will be the user and the external HTML code that we'll be formatting.
- The main processes will be the program itself and things to help with the CSV file such as the input validations, the CSV formatter, the python libraries, and the command line prompt.
- As for data formats, we will be working with HTML and CSV files for the report that is given by the program. Our interactions with the user will be limited to the command line prompt as we hope this makes it easier for our coding phase of the project. With the only inputs being parameters such as keywords.
- Our data flows would include various things such as, checking user input, scanning the keywords given, forwarding HTML requests through the BeautifulSoup library, inputting and forwarding to format those requests, and outputting a beautiful formatted output.
  - For processing information, it would just be the process of taking the HTML requests in a raw form, putting it through BeautifulSoup and formatting it, and outputting a clean formatted CSV file.
  - Our only data sinks would be the CSV files itself which holds all the data that we're formatting and the user input parameters will be put into a data sink list to go through. 

#### Overall Goal
Overall, what we hope to achieve in the end goal is a simple to use python command line input output type of web scrapper. We hope that the user inputs keywords as parameters which will be used to scrape 3+ known job listing websites and remove any duplications. We'll focus more on working with the CSV file to make it look nice to make the user interface look appealing and we hope to have no errors whatsoever.
