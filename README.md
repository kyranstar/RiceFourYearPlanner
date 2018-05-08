# RiceCourseOfferings

A tool to crawl the Rice course listing and show historically which semesters classes had been offered. 
This program runs on a text file of course names, and outputs the number of times each of them have been offered in a certain year range for each semester.

## Data

All data is currently run on the 2012-2018 time period. It is located in the data directory. XXXXList2018.txt files have a list of courses offered in 2018 for that subject, and XXXXOfferings2018.txt are the results of running the program, the number of times each class in that subject has been offered from 2012-2018. 
To run on new data, copy the names of all classes into a text file, and run seperate.py on them. Move these files into the data directory, and then run run_whole_dir.py on them.

## Code Organization

* rice_class_availability.py: Takes a file, containing a list of class names, and creates a file that contains how many times they were offered.
* run_whole_dir.py: Runs rice_class_availability.py on every file that contains the substring "List" in the data directory.
* seperate.py: Takes a master file and seperates them into files with only one subject each.

### Installing

Steps:
* [Install python 3](https://www.python.org/downloads/)
* [Install beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [Clone the repository](https://help.github.com/articles/cloning-a-repository/)
* Run! Type `python rice_class_availability.py -h` for instructions.

## Contact

Email me at: kpa1 (at) rice (dot) edu.

If you find errors in the data/program, please send me an email, create an issue in the Github project, or submit a pull request.