
# w terminalu
# python3.7 +
# python openImgv5-extractor.py --cname="nazwa klasy" --bboxf="nazwa pliku z boxami.csv" 
#                               --cdesf="nazwa pliku z nazwami klas i ich tagów.csv" 
#                               --to="nazwa pliku do ktorego zapiszemy dane o plikach zawierajacych szukana klase.csv"')
# np.
# python openImgv5-extractor.py --cname="Ant" --bboxf="validation-annotations-bbox.csv" --cdesf="class-descriptions-boxable.csv" --to="new.csv"')
#
# Chcesz wyszukac zdjecia zawierajace 2 klasy: X i Y ?
# python openImgv5-extractor.py --cname="X" --bboxf="a.csv" --cdesf="b.csv" --to="c.csv"')
# python openImgv5-extractor.py --cname="Y" --bboxf="c.csv" --cdesf="b.csv" --to="d.csv"')



import argparse
import csv
from shutil import copy2

class Extractor():
    def __init__(self):
        self.collect_program_arguments()
        
    def collect_program_arguments(self):
        parser = argparse.ArgumentParser(description='Writes names of images with given \
                                                        class to file\n \
                                                        [OUT] Prints out number of files containing class\n \
                                                        [OUT-FILE]file-name,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside\n\n\
                                                        usage example:\n\
                                                        \t\tpython openImgv5-extractor.py --cname="Ant" --bboxf="validation-annotations-bbox.csv" --cdesf="class-descriptions-boxable.csv" --to="NOWY.csv"')
        parser.add_argument("--cname", default="car", type=str, help="name of class to look for")
        parser.add_argument("--bboxf", type=str,
                            help="path to file with annotation boxes")
        parser.add_argument("--cdesf", type=str,
                            help="path to file with class names and labels")
        parser.add_argument("--to", type=str,
                            help="file name in which data of images with given class is stored")


        args = parser.parse_args()
        self.className = args.cname
        self.bboxFile  = args.bboxf
        self.cdesFile  = args.cdesf
        self.toFile    = args.to

    def ret_class_labelName(self):
        classLabelName = ""
        desName = 0 
        cName  = 1
        with open(self.cdesFile, newline='\n') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                if row[cName] == self.className:
                    classLabelName = row[desName]
                    break

        
        return classLabelName
        
    def files_with_labelName(self, labelName):
        listOfFiles = []
        with open(self.bboxFile, newline='\n') as csvfile:
            dictReader = csv.DictReader(csvfile, delimiter=',')
            for row in dictReader:
                if row["LabelName"] == labelName:
                    listOfFiles.append(row)

        return listOfFiles

    def write_found_files(self):
        labelName = self.ret_class_labelName()

        if labelName == "":
            print("{self.className} does not exist")
            exit()

        listOfFiles = self.files_with_labelName(labelName)
        print("No. of files with", self.className, "label " + str(len(listOfFiles)))

        with open(self.toFile, mode="w") as savedListOfFiles:
            csvWriter = csv.writer(savedListOfFiles, delimiter=',')
            #tags
            csvWriter.writerow(["ImageID","Source","LabelName","Confidence",
                                "XMin","XMax","YMin","YMax","IsOccluded","IsTruncated",
                                "IsGroupOf","IsDepiction","IsInside"
                            ])

            for row in listOfFiles:
                csvWriter.writerow([
                    row["ImageID"],row["Source"],row["LabelName"],row["Confidence"],
                    row["XMin"],row["XMax"],row["YMin"],row["YMax"],row["IsOccluded"],
                    row["IsTruncated"],row["IsGroupOf"],row["IsDepiction"],row["IsInside"]
                ])
                
    def save_extracted_imgs(self, toFolder, fromFolder, fileFormat=".jpg"):
        with open(self.toFile, newline='\n') as csvfile:
            des = toFolder
            dictReader = csv.DictReader(csvfile, delimiter=',')
            for row in dictReader:
                imgID = row["ImageID"]
                src = fromFolder + "/" + imgID + fileFormat
                try:
                    copy2(src, des)
                except FileNotFoundError:
                    pass

x = Extractor()
x.write_found_files()

# zapisz zdjęcia (z zapisanych id-ków z pliku toFile)
# zdjęcia do zapisania znajdują się w folderze fromFolder
# zdjęcia zostaną skopiowane do folderu toFolder
# format zdjęć fileFormat domyślnie ustawiony jest na .jpg
x.save_extracted_imgs("/home/login/zapisz-zdjecia", "/home/login/baza-zdjec", ".jpg")


