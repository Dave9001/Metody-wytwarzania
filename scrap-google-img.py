# Wymaga google_images_download
# instalacja:
# wpisz w terminalu
# pip install google_images_download


import argparse
from google_images_download import google_images_download  

class ScrapGoogleImg():

    def __init__(self):
        self.collect_program_arguments()
        
    def collect_program_arguments(self):
        parser = argparse.ArgumentParser(description='Use flag --search="to search for what you want"\
                                                    Use flag --format="png", to download images in png format\
                                                    Use flag --size="large", to download large images\
                                                    Use flag --scrap_size=400, to download 400 images')
        parser.add_argument("--search", type=str, help="type what google should look for")
        parser.add_argument("--format", type=str, default='jpg',  help="image format")
        parser.add_argument("--size", type=str, default='medium', help="image format")
        parser.add_argument("--scrap_size", type=int, default=1,  help="number of images to download")

        args = parser.parse_args()
        self.searchFor = args.search
        self.format = args.format
        self.size = args.size
        self.scrap_size = args.scrap_size

    def download_images(self):
        response = google_images_download.googleimagesdownload()  
        print(self.searchFor)
        arguments = {"keywords": self.searchFor, 
                    "format": self.format, 
                    "limit": self.scrap_size, 
                    "print_urls":True, 
                    "size": self.size, 
                    "aspect_ratio": "panoramic"
                    } 
        try:
            response.download(arguments)   

        except FileNotFoundError:  
            arguments = {"keywords": self.searchFor, 
                        "format": self.format, 
                        "limit": self.scrap_size, 
                        "print_urls":True, 
                        "size": self.size
                        }

            try: 
                response.download(arguments)  
            except: 
                pass
        
        print("Download of" , self.searchFor, "[DONE]\n")


x = ScrapGoogleImg()
x.download_images()

