import os
import rice_class_availability

def main():
    """
    Runs rice_class_availability on every List file in the data directory.
    """
    
    files = os.listdir("data")
    files = list(filter(lambda x: "List" in x, files))
        
    #files = files[files.index("PSYCList2018.txt"):]
    
    for idx, file in enumerate(files):
        output = file[:4] + "Offerings.txt"
        rice_class_availability.file_class_offerings(file, 2012, 2018, output)
        print("Finished %d/%d files" % (idx, len(files)))
    

if __name__ == "__main__":
    main()
