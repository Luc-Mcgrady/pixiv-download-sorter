# Pixiv sort

Automatically renames and sorts images downloaded from pixiv with "save as image" in the browser into seperate folders. This tool is reliant on the files not having be renamed manually by the user. e.g. `86409548_p0.png` will be sorted. Files saved with any other filename format (including "master" files that are found when downloading the thumbnails of images (use "save link as" or click to fullscreen the image before saving.))

usage:
```
python pixiv_sort.py

options:
  -h, --help            show this help message and exit
  --src SRC             The folder containing your saved files
  --done DONE           Move sorted files to this folder with their original names
  --sorted SORTED       Where the files will moved and renamed
  --gallery-file GALLERY_FILE
                        Adds a blank file with the given name to every generated folder
```

This will save the renamed files into a given folder. To move the original files so that they do not need to be re-sorted if the program is re-run, use the "done" argument.

This will make a request to pixiv and webscrape the information from the server once for every gallary.