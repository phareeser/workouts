# Workouts

__Workouts__ manages sport workouts imported from external sources like ***Garmin Connect***
1. Import workouts from Garmin Connect, CSV or JSON
   Just unknown (new) workouts are being imported
2. Store them in a SQLite database
3. Export to CSV or JSON
4. Handle duplicate workouts

Examples:
- ''workouts.py import -s garmin -gu [garmin user] -gp [garmin password] workouts.db'' imports from Garmin Connect to workouts.db
- ''workouts.py import -s csv -f [CSV import file] workouts.db'' imports from a CSV file to workouts.db
- ''workouts.py show workouts.db'' lists all stored workouts
- ''workouts.py check'' performs a database check for duplicate workouts (several rules like same time, same sports)

## Use Cases

1. Evaluation of your workouts
   - supported by a database you are able to create own evaluations 
   - without the need to subscribe to professional sport workouts evaluation portals
2. Identification of duplicate workouts
   - e.g. when your Garmin account is connected to other services like Zwift, Garmin will show two workouts for the same session. **workouts** detects those duplicates  

## Authors

* **Martin Reese** - *Initial work* - [PhaReeseR](https://github.com/PhaReeseR)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Getting Started

__Workouts__ contains a **/lib** directory, containing all files needed for the functionality, while **workouts.py** is a command line tool.

### Prerequisites

__Workouts__ is developed and tested with Python 3.8 

Required packages for the library **/lib**:
- logging
- sqlalchemy
- requests
- re
- json
- csv 
- datetime
- abc

Required packages for unit and integration tests
- unittest
- os

Required packages for the command line tool **workouts.py**:
- logging
- argparse
- datetime

## Acknowledgments
My motivation for this project was to learn Python. I have previously implemented the same functionality with Ruby.  
  
Besides the 
* https://www.python.org 
site I have learned very much from  
* https://github.com/petergardfjall/garminexport

## ToDo|s:
- Handle timezones
- Import details
- Import GPX
- Import other personal data history (weight, FTP)
