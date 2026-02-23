# PythonMetadataAdder

A little python script I made to aid in adding the three kinds of metadata I care about to a file.
These are the artist, album, and genre tags.
If you want to add more feel free.
I use a dictionary and based on the name of the key is what's added as an argument for ffmpeg.
I would use exiftool, but as of now there isn't support for writing to mp3 files it can only read.
This script I also made to only works for .mp3 files as that's what I use.
The script also only works on Linux as I'm using the /tmp directory for ffmpeg's temp file.

## Options

- -a, --artist ARTIST
    Add the artist you want.
    Keep in mind if there is a spaced needed to surround in quotes.

- -b, --album ALBUM
    Add the album you want.
    Keep in mind if there is a spaced needed to surround in quotes.

- -g, --genre GENRE
    Add the genre you want.
    Keep in mind if there is a spaced needed to surround in quotes.

- -h, --help
    Bring up the help menu.

- -d, --directories DIRECTORY \[DIRECTORIES ...\]
    Give a list of directories to go through.
    This is useful for bulk adding the metadata to everything inside which includes subdirectories.
    As an example, if you have a directory named Rock you can then add the genre of rock to everything inside down to the lowest directory.

- -f, --files FILE \[FILES ...\]
    Give a list of files to add the metadata for.

## Example Usage

`python3 addmeta.py -g "A Genre" -f ./file1.mp3 /home/user/Something/file2.mp3 -d ../ADir /home/user/Music`

`python3 addmeta.py -a Goofy -b "Big Funnies" -g Comedy -f ../FunnyGuy.mp3`
