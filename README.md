# RiceCourseOfferings

A four-year planning tool for Rice University that tells you when courses are offered.

The program crawls the Rice course listing and, based on which semesters classes have been offered historically, highlights your four-year plan in red. 

The program is still rough. Some things to add:
* Credit hours
* GUI for updating
* Cleaner interface
* Grabbing most recent syllabus/class description
* Check time conflicts
* More descriptive errors than colors

## Data

All data is currently run on the 2012-2018 time period. It is located in the data directory. XXXXList2018.txt files have a list of courses offered in 2018 for that subject, and XXXXOfferings.txt are the results of running the program, the number of times each class in that subject has been offered from 2012-2018. 
The program should automatically update the data when File->Update Class Data is clicked.

### Installing

Steps:
* [Install python 3](https://www.python.org/downloads/)
* [Install beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* [Clone the repository](https://help.github.com/articles/cloning-a-repository/)
* Run! Type `python rice_class_availability.py -h` for instructions.

## Contact

Email me at: kpa1 (at) rice (dot) edu.

If you find errors in the data/program, please send me an email, create an issue in the Github project, or submit a pull request.