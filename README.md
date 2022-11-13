# comic-downloader

### Requirements:
- Python 3.7+

### How to use:
1. Right click the page/image & copy paste the first page's (image) url of comic to `source_reader.json` ➡️ `"source_url"` tag.
2. Look for the comic pages url pattern. 
    - In web its a common phenomena that the images/pages are in a particular manner (patter) for a given comic. Like these patterns could be `/naruto/page-01.jpg`, `/naruto/page-02.jpg` .. and so on.
    - Look for these patterns and replace the changing string/values with an `*` symbol.
    - Pattern replacing example:
        - `/page-1.jpg`, `/page-2.jpg` ... __=>__ `/page-*.jpg`
        - `/page-001.jpg`, `/page-002.jpg` ... __=>__ `/page-*.jpg`

example:
```json
"source_url" : "https://official-complete-2.eorzea.us/manga/Naruto/0692-*.png"
```
3. Provide padding value (pad_len) if required.
    - If the url patterns have 0 (zeros) in the beginning, then add proper padding lenght in `"pad_len"` tag, inside source_reader.json.
        - `/page-1.jpg, /page-2.jpg ...` __=>__  pad_len = 0
        - `/page-001.jpg, /page-002.jpg ...` __=>__  pad_len = 2
