import json
import sys
import requests
import os
import shutil
import uuid
from PIL import Image

APP_VERSION = "v1.0"
APP_AUTHOR = "Anindya Das"
APP_REPO_URL = "https://github.com/Anindya-Das02"
APP_INFO = f"""Comic Downloader  ({APP_VERSION})
=========================
A simple python script to download your favourite Comics, Mangas & more. Easily create good quality pdfs.
Please read "How to use.md" from github for detailed instructions.

Created By: {APP_AUTHOR}
GitHub: {APP_REPO_URL}"""
APP_HELP = f"Please refer {APP_REPO_URL}"

class ArgumentManager:
    def __init__(self, arg) -> None:
        if arg == "--version" or arg == "-v":
            print(f"App version: {APP_VERSION}")
        elif arg == "--info" or arg == "-i":
            print(APP_INFO)
        elif arg == "--help" or arg == "-h":
            print(APP_HELP)

class ComicDownloader:

    def __init__(self) -> None:
        print("reading source_reader.json ...")
        self.fd = json.load(open("source_reader.json",'r'))
        self.source_url = self.fd['source_url']
        self.d_type = self.fd['d_type']
        self.total_pages = self.fd['total_pages']
        self.file_name = self.fd['file_name']
        self.img_extension = self.fd['img_extension']
        self.clean_up = self.fd['clean_up']

    def do_task(self) -> None:
        self.process_requirements()
        if self.fd["source_url"] == "<file_source>":
            self.file_source_download()
        else:
            self.download()
        self.create_pdf()
        self.clean_up_process()
        print("[E.N.D]")

    def process_requirements(self) -> None:
        # pdfs created will be stored in downloads folder
        # create downloads folder if not found
        if not os.path.isdir("downloads"):
            os.mkdir("downloads")

        # creating dir imgs-*/ to save (or) hold downloaded images
        uuid_string = str(uuid.uuid1().hex)
        self.target_dir = f"imgs_{uuid_string}"
        os.mkdir(self.target_dir)
        print("pre-download requirements completed!")
    
    def file_source_download(self):
        if "file_source" not in self.fd or self.fd["file_source"] == None or len(self.fd["file_source"].strip()) == 0:
            print(f"[ERROR] 'file_source' tag is empty or missing in source_reader.json")
            self.terminate_process()
        urls = []
        try:
            with open(self.fd['file_source'],'r') as source_file:
                urls.extend([line.strip("\n") for line in source_file.readlines()])
        except FileNotFoundError:
            print(f"[ERROR] file not found! File '{self.fd['file_source']}' does not exists in this folder!")
            self.terminate_process()
        print(f"fetching from {len(urls)}..")
        page_no = 1
        for url in urls:
            try:
                print(f"downloading {page_no}: {url}")
                data = self.fetch_image_data(url)
                self.write_bytes_to_file(data,page_no)
                print(f"downloading {page_no}: {url}")
            except:
                print("[ERROR] an error occured while downloading image (or) writing image file")
            page_no += 1

    def download(self) -> None:
        print("Initiating download..")
        print(f"{self.total_pages} images to download")
        if self.d_type.lower() in ("padded_incremental", "pi"):
            if "pad_len" not in self.fd['padded_incremental'] or "start_no" not in self.fd['padded_incremental']:
                print("[ERROR] required tag(s) 'pad_len' or 'start_no' missing in source_reader.json")
                print("[TRY] adding tag(s) 'pad_len', 'start_no' inside 'padded_incremental' tag")
                self.terminate_process()
            padding = self.fd['padded_incremental']['pad_len']
            page_start = self.fd['padded_incremental']['start_no']
            self.download_images_from_url(padding = padding, page_start = page_start)
        else:
            self.download_images_from_url()

    def write_bytes_to_file(self,data,page_no) -> None:
        page_name = f"{self.target_dir}/page-{page_no}.{self.img_extension}"
        with open(page_name,'wb') as image_file:
            image_file.write(data)

    def download_images_from_url(self, padding = 0, page_start = 1) -> None:
        total_page = self.total_pages
        for i in range(page_start,self.total_pages + 1):
            try:
                page_no = str(i).zfill(padding + 1)
                url = f"{self.source_url.replace('*', page_no)}"
                print(f"downloading [{i}/{total_page}]: {url}")
                img_data = self.fetch_image_data(url)
                self.write_bytes_to_file(img_data,page_no)
                print(f"download completed [{i}/{total_page}]")
            except:
                print("[ERROR] an error occured while downloading image (or) writing image file")
        print("Finished image downloading process..")
    
    def fetch_image_data(self,url:str = '') -> bytes :
        return requests.get(url).content

    def create_pdf(self) -> None:
        print("creating pdf..")
        img_list = [i for i in os.listdir(self.target_dir)]
        imgs_to_pdf_list = []
        for i in sorted(img_list):
            imgs_to_pdf_list.append(Image.open(f"{self.target_dir}/{i}").convert('RGB'))
        filename = f"{self.file_name}.pdf"
        imgs_to_pdf_list[0].save(f"downloads/{filename}",save_all=True, append_images=imgs_to_pdf_list[1:])
        print(f"'{filename}' created successfully")

    def clean_up_process(self,error_clean = False) -> None:
        if error_clean or self.clean_up:
            print("starting cleanup..")
            try:
                shutil.rmtree(self.target_dir)
                print("clean up completed!")
            except:
                print("[ERROR] error occured while clean up")
        else:
            print("cleanup skipped!")
        
    def terminate_process(self) -> None:
        # remove empty folder img-*/ on exception
        self.clean_up_process(error_clean = True)
        print("terminating...")
        exit(0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ArgumentManager(sys.argv[1])
        exit(0)
    ComicDownloader().do_task()