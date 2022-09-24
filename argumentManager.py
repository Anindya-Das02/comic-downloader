APP_AUTHOR = "Anindya Das"
GIT_REPO_URL = "https://github.com/Anindya-Das02/comic-downloader"
APP_VERSION = "v1.1"
APP_INFO = f"""Comic Downloader  ({APP_VERSION})
=========================
A simple python script to download your favourite Comics, Mangas & more. Easily create good quality pdfs.
Please read "How to use.md" from github for detailed instructions.

Created By: {APP_AUTHOR}
GitHub: {GIT_REPO_URL}"""
APP_HELP = f"""python(3) main.py <arg> 

Args List Below:
--------------------
--demo    | -d : see working demo of Comic Downloader. check how to use 'source_reader.json'
--help    | -h : see useful tags
--info    | -i : show app info, like author, git repo, etc.
--tags    | -t : see 'source_reader.json' tags & description
--version | -v : app version"""
APP_TAGS = """'source_reader.json' tags description & usage below:
{
    "source_url" : String (starting image url),
    "d_type" : String ["padded_incremental" | "pi" | "simple_incremental" | "si" ],
    "padded_incremental" : {
        "pad_len" : Integer (padding length, ex: 002 -> 2),
        "start_no" : Integer,
    },
    "total_pages" : Integer (total no. of pages to download),
    "file_name" : String (save pdf as),
    "img_extension" : String (image extension used in image url),
    "clean_up" : Boolean (remove imgs_* folder & its contents after pdf creation),
    "file_source" : String (file name with image urls)
}"""
APP_DEMO = """Working Demo:
[1]. Created a sample 'source_reader.json' file. Open the file in text editor. Play around, change its contents.
[2]. Run the 'main.py' python file. (Python version required 3.6+)
        run python file from IDE (or) by using below commands from terminal
        Windows:     python main.py
        Linux/MacOs: python3 main.py
[3]. pdf will be created & saved in downloads folder"""
SOURCE_READER_JSON_SAMPLE = '''{
    "source_url" : "https://official-complete-2.eorzea.us/manga/Naruto/0692-*.png",
    "d_type" : "padded_incremental",
    "padded_incremental" : {
        "pad_len" : 2,
        "start_no" : 1
    },
    "total_pages" : 16,
    "file_name" : "Naruto chapter-692",
    "img_extension" : "png",
    "clean_up" : true,
    "file_source" : null
}'''

class ArgumentManager:
    def __init__(self,arg) -> None:
        if arg == "--version" or arg == "-v":
            print(f"App version: {APP_VERSION}")
        elif arg == "--info" or arg == "-i":
            print(APP_INFO)
        elif arg == "--help" or arg == "-h":
            print(APP_HELP)
        elif arg == "--demo" or arg == "-d":
            with open("source_reader.json","w") as sf:
                sf.write(SOURCE_READER_JSON_SAMPLE)
            print(APP_DEMO)
        elif arg == "--tags" or arg == "-t":
            print(APP_TAGS)
        else:
            print(f'unknown commad: {arg}')
            print('use "--help" for more info')