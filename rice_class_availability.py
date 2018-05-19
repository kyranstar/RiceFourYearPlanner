# Written by Kyran Adams
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.pool import ThreadPool
import pandas as pd
import itertools
import numpy as np

TIMEOUT = 20
CORES = 64

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
    num_tries = 5
    for i in range(num_tries):
        try:
            url = create_url(keywords, term, year)
            # download html
            html = urlopen(url, None, TIMEOUT).read().decode('utf-8')
            # parse html
            soup = BeautifulSoup(html, "lxml")
            tab = soup.find("table", {"class": "table table-condensed"})
            tbody = tab.find("tbody")
            tr = tbody.find("tr")
            
            # Documents with one child here mean an empty listing, so no classes offered
            offered = len(tr.findChildren()) != 1
            #print("%s %d:%s offered: %s" % (keywords, year, term, str(offered)))
            return 1 if offered else 0
        # catch everything but keyboard interrupt
        except KeyboardInterrupt:
            raise
        except Exception as e:
            #print(traceback.format_exc())
            print("Attempt %d/%d: Exception looking up class %s" % (i+1, num_tries, keywords))
        if i == num_tries-1:
            print("FAILED for class %s" % keywords)
            return -1


def add_new_entries(datatable, filename, yearrange):
    """
    Given an old datatable, this adds new columns and rows corresponding to new
    semesters and classes.
    """
    # Read class name from each line in file
    with open("data/" + filename) as f:
        full_classnames = set([line.strip() for line in f.readlines() if len(line.strip()) > 0])
    
    # Add new columns with nan values
    full_sems = itertools.product(yearrange, ["fall", "spring", "summer"])
    for (year, sem) in full_sems:
        semstr = "%d:%s" % (year, sem)
        if not semstr in datatable.columns:
            datatable[semstr] = [np.nan] * len(datatable.index)
    
    # Add new rows with nan values
    for classname in full_classnames:
        if not classname in datatable.index:
            datatable.loc[classname] = [np.nan] * len(datatable.columns)


def file_class_offerings(filename, yearstart, yearend, tsvfile):
    """
    Takes a list of classnames, and saves the times the class was 
    offered in the range of years to a file. If the tsvfile already contains
    some data, it does not recompute it. Takes a little bit because networks are 
    slow.
    
    Arguments:
        filename: Name of text file containing class names on each line.
        yearstart: Start year in year range.
        yearend: End year in year range. If outside 
            the range of available years on the website, it will give weird 
            results.
        tsvfile: file name which the program will write a tab seperated 
            value format of the data to.
    """
    # check if some data already exists so we don't do extra work
    try:
        datatable = pd.read_table("data/" + tsvfile)
    except IOError:
        datatable = pd.DataFrame()
        datatable['Class name'] = []
    datatable.set_index('Class name', inplace=True)
    
    yearrange = range(yearstart, yearend+1)
    add_new_entries(datatable, filename, yearrange)
    
    # Run the program
    pool = ThreadPool(CORES)
    results = {}
    
    for column in datatable.columns:
        if column == "Class name":
            continue
        results[column] = {}
        nan_indices = [i for i, x in enumerate(datatable[column].isnull()) if x]
        # also update error values
        nan_indices.extend([i for i, x in enumerate(datatable[column]==-1.0) if x])
        classes = list(datatable.index)
        nan_rows = [classes[i] for i in nan_indices]
        year = int(column.split(":")[0])
        term = column.split(":")[1]
        for classname in nan_rows:
            results[column][classname] = pool.apply_async(was_class_offered, args=(classname, term, year))

    for column in results.keys():
        for classname in results[column].keys():
            datatable.at[classname, column] = results[column][classname].get()

    # Write to TSV file
    print("Writing tsv to data/%s" % tsvfile)
    datatable.reset_index(inplace=True)
    datatable.rename(columns={'index':'Class name'}, inplace=True)
    datatable.sort_values('Class name', inplace=True)
    datatable.to_csv("data/" + tsvfile, sep="\t", index=False)
    