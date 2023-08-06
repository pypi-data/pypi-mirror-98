# jfind
A very simple script to parse and search for values in a JSON file.

## Usage
Just run:
```bash
jfind FILE_NAME SEARCH_TERM
```
This will return the locations of all matches that contain the search term (case insensitive). Exact matches will be colored if your terminal supports it.

For example:
```bash
jfind hello.json hi
```
Output:
```
$ jfind hello.json hi
### SEARCH RESULTS ###
parent-key-1 -> value: hi there
parent-key-2 -> an-array -> 1 -> value: hi from a list element
Found 2 matches...
```

## Installation
Just run:
```bash
pip install jfind
```
Or:
```bash
python -m pip install jfind
```

## Author
Erick Durán. Copyright © 2021.

## License
Released under the GPL-3 License.
