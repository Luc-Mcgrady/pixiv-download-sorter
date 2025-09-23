# Pixiv sort

Automatically renames and sorts images downloaded from pixiv with "save as image" in the browser into seperate folders, renaming them and creating new folders if part of a galery (detected if the second image in a galary exists)

usage:
```
python pixiv_sort.py [working directory (defaults to cwd)]
```

This will create 2 folders a "sorted" folder and a "done" folder, where the sorted folder will contain the sorted images and the done folder will contain the images with their original names in case they require re-sorting. These files will be hard linked instead of copied so no extra disk space will be taken.