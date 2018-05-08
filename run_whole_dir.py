import argparse
import os
import rice_class_availability

def main():
    """
    Runs rice_class_availability on every List file in the data directory.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-yearstart", help="The year to start looking at, defaults to 2012", type=int)
    parser.add_argument("-yearend", help="The year to end looking at, defaults to 2018", type=int)
    args = parser.parse_args()
    
    files = os.listdir("data")
    files = list(filter(lambda x: "List" in x, files))
        
    files = files[files.index("PSYCList2018.txt"):]
    
    for idx, file in enumerate(files):
        output = file[:4] + "Offerings2018.txt"
        rice_class_availability.file_class_offerings(file, args.yearstart, args.yearend, output)
        print("Finished %d/%d files" % (idx, len(files)))
    

if __name__ == "__main__":
    main()
