Markdown based html generator.
Generation requires: HTML template and markdown template.
Additional meta-extensions allow you to add metaprogramming to this process.

## Installation

```console
pip install mdhtmlgen
```

## Usage

```console
$ python -m mdhtmlgen --help
Usage: python -m mdhtmlgen [options]

Options:
  -h, --help            show this help message and exit
  -S SOURCE, --source=SOURCE
                        Markdown source filename (*.md)
  -H HTML, --html=HTML  HTML template filename (*.t)
  -t, --trace           Print diagnostic traces
  -o OUTPUT, --output=OUTPUT
                        Set output file
  -m MARKDOWN_EXT, --markdown-ext=MARKDOWN_EXT
                        Set markdown extension list, coma separated, e.g.
                        meta,toc,footnotes
  -d DATE_FMT, --date-fmt=DATE_FMT
                        Set date format, e.g. %d-%m-%Y %H:%M:%S
  -e EXT, --ext=EXT     Set extension list, e.g. meta,glob,filename,date
  -a PARAMS, --add=PARAMS
                        Add parameter in format name:value
  -g GIT_DIR, --git-dir=GIT_DIR
                        Set GIT directory location, e.g. /home/user/repo/.git```
