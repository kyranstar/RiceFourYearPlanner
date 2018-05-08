# Written by Kyran Adams, 05/06/2018
import argparse
from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
from multiprocessing.pool import ThreadPool

TIMEOUT = 20
CORES = 16

def create_url(keywords, term, year):
    """
    Creates a URL for the rice course schedule system for a given query.
    Arguments:
        keywords: A string for the keywords, like "MATH 331".
        term: The term to look at; either "fall", "spring", or "summer".
        year: The year to look at.
    """
    # clean up input
    keywords = keywords.strip()
    term = term.lower().strip()
    # The system works on academic years, so fall shows up under the next year
    if term == "fall":
        year += 1
    # url template
    base = "https://courses.rice.edu/admweb/!SWKSCAT.cat?p_action=QUERY&p_term=%d%d0&p_ptrm=&p_crn=&p_onebar=%s&p_mode=AND&p_subj_cd=&p_subj=&p_dept=&p_school=&p_spon_coll=&p_df=&p_insm=&p_submit="
    # map terms to numbers
    term_num = {"fall":1, "spring":2, "summer":3}[term]
    # replace spaces with + in name
    keywords = keywords.replace(" ", "+")
    return base % (year, term_num, keywords)

def was_class_offered(keywords, term, year):
    """
    Checks whether a class was offered in a specific term.
    Arguments:
        keywords: the class, like "MATH 331"
        term: The term to look at.
        year: The year to look at.
    """
    url = create_url(keywords, term, year)
    # download html
    html = urlopen(url, None, TIMEOUT).read().decode('utf-8')
    # parse html
    soup = BeautifulSoup(html, "lxml")
    tab = soup.find("table", {"class": "table table-condensed"})
    tbody = tab.find("tbody")
    tr = tbody.find("tr")
    
    # Documents with one child here mean an empty listing, so no classes offered
    return len(tr.findChildren()) != 1
    
def class_offerings(keywords, years):
    """
    Gives the number of times that a class has been offered in each term in the
    years range.
    Arguments:
        keywords: The class
        years: A range of years to look at, like range(2012, 2018)
    """
    counts = {"fall":0, "spring":0, "summer":0}
    
    for term in ["fall", "spring", "summer"]:
        for year in years:
            # Try this a few times in case of a network error
            num_tries = 5
            for i in range(num_tries):
                try:
                    if was_class_offered(keywords, term, year):
                        counts[term] += 1
                    break
                # catch everything but keyboard interrupt
                except KeyboardInterrupt:
                    raise
                except:
                    print("Attempt %d/%d: Exception looking up class %s" % (i+1, num_tries, keywords))
                if i == num_tries-1:
                    print("FAILED for class %s" % keywords)
                    return {"fall":-1, "spring":-1, "summer":-1}
    print("%s: Fall: %d, Spring: %d, Summer: %d" % (keywords, 
                                                        counts["fall"], 
                                                        counts["spring"], 
                                                        counts["summer"]))
    return counts

def write_tsv(filename, results_dict):
    with open(filename, 'w') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t',lineterminator='\n')
            writer.writerow(["Class name", "Fall", "Spring", "Summer"])
            for classname, offerings in sorted(results_dict.items()):
                writer.writerow([classname, offerings["fall"], offerings["spring"], offerings["summer"]])

def file_class_offerings(filename, yearstart, yearend, tsvfile):
    """
    Takes a list of classnames, and prints the number of times the class was 
    offered in the range of years. Takes a little bit because networks are 
    slow.
    
    Command Line Arguments:
        - Name of text file containing class names on each line.
        - Start year in year range. If not given, defaults to 2012.
        - End year in year range. If not given, defaults to 2018. If outside 
            the range of available years on the website, it will give weird 
            results.
        - Optional file name, which the program will write a tab seperated 
            value format of the data to.
    Examples:
        # Run the program on a bunch of classes from 2012-2018
        $ python rice_class_availibility.py classes.txt
        # Run the program on classes.txt from 2014-2018
        $ python rice_class_availibility.py classes.txt -yearstart 2014 -yearend 2018
        # Run the program and put output in out.txt
        $ python rice_class_availibility.py classes.txt -yearstart 2014 -yearend 2018 -tsvfile out.txt
    """
    
    fname = "data/" + filename
    # Read class name from each line in file
    with open(fname) as f:
        content = f.readlines()
    # strip and remove empty lines
    content = [x.strip() for x in content if len(x.strip()) > 0]
    yearrange = range(2012,2018+1)
    if yearstart != None and yearend != None:
        yearrange = range(yearstart, yearend)
        
    # Run the program
    pool = ThreadPool(CORES)
    results = {}
    for idx, classname in enumerate(content):
        results[classname] = pool.apply_async(class_offerings, args=(classname, yearrange))
    results = {k: v.get() for (k, v) in results.items()}
    
    # Write to TSV file if specified
    if tsvfile != None:
        print("Writing tsv to data/%s" % tsvfile)
        write_tsv("data/" + tsvfile, results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The name of the file to read in data",type=str)
    parser.add_argument("-yearstart", help="The year to start looking at, defaults to 2012", type=int)
    parser.add_argument("-yearend", help="The year to end looking at, defaults to 2018", type=int)
    parser.add_argument("-tsvfile", help="File to output tab seperated value format to", type=str)
    args = parser.parse_args()
    file_class_offerings(args.filename, args.yearstart, args.yearend, args.tsvfile)