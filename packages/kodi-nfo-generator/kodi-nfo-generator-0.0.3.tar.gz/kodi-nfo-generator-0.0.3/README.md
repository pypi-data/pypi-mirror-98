# kodi-nfo-generator
The **kodi-nfo-generator** is a simple Python-based command-line
tool that allows you to generate [.nfo](https://kodi.wiki/view/NFO_files/Movies) 
files for movies that [Kodi](https://kodi.tv/) can use for its library.

This tool is aimed at people that manually curate their movie databases, in order
to avoid using scrapers that may pull in the wrong information (or none at all).
All the user has to do is place an ID file alongside their movie files,
the default is `*.imdb`, containing the unique IMDB movie ID (or full IMDB movie URL).
The tool will then scour the movie directories for these files and pull in the
information and create the `.nfo` files in the same location.

## Installation

You can install the tool with pip as follows:

```
pip install kodi-nfo-generator
```

## Tools

### kodi-nfo-gen

The `kodi-nfo-gen` tool can be used for pulling in the information from the 
web using the IDs stored in the ID files.

The following parameters can be supplied to the tool:

```
usage: kodi-nfo-gen [-h] --dir DIR [--type {imdb}] [--recursive]
                    [--pattern GLOB] [--delay SECONDS]
                    [--preferred_language LANG]
                    [--fanart {none,download,use-existing}]
                    [--fanart_file FILE] [--dry_run] [--overwrite] [--verbose]
                    [--debug] [--interactive]

Generates Kodi .nfo files with information retrieved from IMDB using local
files with the unique IMDB movie ID.

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR             the directory to traverse (default: None)
  --type {imdb}         what type of ID the movie ID files represent, ie the
                        website they are from (default: imdb)
  --recursive           whether to traverse the directory recursively
                        (default: False)
  --pattern GLOB        the pattern for the files that contain the movie IDs
                        (default: *.imdb)
  --delay SECONDS       the delay in seconds between web queries (to avoid
                        blacklisting) (default: 1)
  --preferred_language LANG
                        the preferred language for the titles (ISO 639-1, see
                        https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
                        (default: en)
  --fanart {none,download,use-existing}
                        how to deal with fan-art (default: none)
  --fanart_file FILE    when downloading or using existing fanart, use this
                        filename (default: folder.jpg)
  --dry_run             whether to perform a 'dry-run', ie only outputting the
                        .nfo content to stdout but not saving it to files
                        (default: False)
  --overwrite           whether to overwrite existing .nfo files, ie
                        recreating them with freshly retrieved data (default:
                        False)
  --verbose             whether to output logging information (default: False)
  --debug               whether to output debugging information (default:
                        False)
  --interactive         for enabling interactive mode (default: False)
```


### kodi-nfo-export

Using the `kodi-nfo-export` tool, you can export your ID files in a CSV file, 
associating them with the directory that they were located in. The tool also
looks for `.nfo` files, in case you already have meta-data stored for your movies.  

The following parameters can be supplied to the tool:

```
usage: kodi-nfo-export [-h] --dir DIR [--recursive] [--type {imdb}]
                       [--pattern GLOB] --output CSV [--verbose] [--debug]
                       [--interactive]

Exports Kodi ID/.nfo files to CSV, associating directories with IDs.

optional arguments:
  -h, --help      show this help message and exit
  --dir DIR       the directory to traverse (default: None)
  --recursive     whether to traverse the directory recursively (default:
                  False)
  --type {imdb}   what type of ID the movie ID files represent, ie the website
                  they are from (default: imdb)
  --pattern GLOB  the pattern for the files that contain the movie IDs
                  (default: *.imdb)
  --output CSV    the CSV output file to store the collected information in
                  (default: None)
  --verbose       whether to output logging information (default: False)
  --debug         whether to output debugging information (default: False)
  --interactive   for enabling interactive mode (default: False)
```

## kodi-nfo-import

With the `kodi-nfo-import` tool, you can import IDs from a CSV file and create ID
files in your movie directory structure.

The following parameters can be supplied to the tool:

```
usage: kodi-nfo-import [-h] --input CSV --dir DIR [--type {imdb}] --col_id COL
                       --col_dir COL [--col_file COL] [--dry_run]
                       [--overwrite] [--verbose] [--debug] [--interactive]

Imports IDs from CSV, storing ID files in the associated directories.

optional arguments:
  -h, --help      show this help message and exit
  --input CSV     the CSV output file to store the collected information in
                  (default: None)
  --dir DIR       the top-level directory of the movies if relative
                  directories are used in the CSV file (default: None)
  --type {imdb}   what type of ID to create, ie what website the IDs are from
                  (default: imdb)
  --col_id COL    the column that contains the ID (name or 1-based index)
                  (default: None)
  --col_dir COL   the column that contains the directory (name or 1-based
                  index) (default: None)
  --col_file COL  the column that contains the file name (name or 1-based
                  index) (default: None)
  --dry_run       whether to perform a 'dry-run', ie only outputting the ID
                  file content to stdout but not saving them to files
                  (default: False)
  --overwrite     whether to overwrite any existing ID files or leave them be
                  (default: False)
  --verbose       whether to output logging information (default: False)
  --debug         whether to output debugging information (default: False)
  --interactive   for enabling interactive mode (default: False)
```

## Examples

For the following examples, we assume your movies are structured like this:

```
./mymovies
|
+- Metropolis
|  |
|  +- Metropolis.mp4
|  |
|  +- Metropolis.imdb   # content: tt0017136
|
+- Spies
|  |
|  +- Spies.mkv
|  |
|  +- Spies.imdb   # content: https://www.imdb.com/title/tt0019415/?ref_=nm_knf_i2
|
+- movies
   |
   +- Nosferatu.mp4
   |
   +- Nosferatu.imdb   # content: tt0013442
   |
   +- Sunrise.mp4
   |
   +- Sunrise.imdb   # content: tt0018455
```

### kodi-nfo-gen

And for each movie an `.imdb` file with either the unique IMDB ID
or the full IMDB URL is present.

Then you can the tool for generating the `.nfo` files like this:

```
kodi-nfo-gen \
  --dir ./mymovies \
  --recursive \
  --verbose
```

If you also want to download fan art (e.g., as `folder.jpg`), then 
you can use the following command-line:

```
kodi-nfo-gen \
  --dir ./mymovies \
  --recursive \
  --fanart download \
  --verbose
```  

### kodi-nfo-export

The following command-line exports all the movies from the `./mymovies` directory 
as a CSV file `./list.csv`:

```
kodi-nfo-export \
  --dir ./mymovies \
  --output ./list.csv \
  --recursive \
  --verbose
```

### kodi-nfo-import

Assuming this CSV file (`./list.csv`) containing movie IDs and their associated 
directories (and optional file name):

```
ID,File,Dir
tt0017136,,Metropolis
https://www.imdb.com/title/tt0019415/?ref_=nm_knf_i2,,Spies
tt0013442,Nosferatu,Movies
tt0018455,Sunrise,Movies
```

Then the following command-line imports the IMDB IDs from the CSV file using 
`./mymovies` as top-level directory for relative paths in the CSV file:

```
kodi-nfo-import \
  --input ./list.csv \
  --dir ./mymovies \
  --type imdb \
  --col_id 1 \
  --col_file 2 \
  --col_dir 3 \
  --verbose
```

**Note:** If a file name should not be present in the CSV, the import will then look 
for files in that directory (.nfo, .mp4, .mkv, .avi). If it cannot find such a file, 
it will use the base name of the directory (`Spies` and `Metropolis` in the above example 
directory structure).
