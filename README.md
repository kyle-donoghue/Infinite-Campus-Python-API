# Infinite Campus API written in Python3
This project was made because of my want for a fast and easy API for Infinite Campus. This project is based off of @j-koreth 's Infinite-Campus-API-2 (https://github.com/j-koreth/Infinite-Campus-API-2)

## Current Progress
I am currently finished with this project. I cleaned up the code to the best of my abilities, but forgive me for the lack of comments. Feel free to expand upon 
this code or even convert it to a different language [ please credit me though :) ].

## Usage
All scripts can be run by normal `python script.py` or by `chmod +x script.py` then `./script.py`.

`campus.py` returns all your current grades in the console based on semester choice. It also has a saved login feature that can be used with rawGrades.py.

`rawGrades.py` is a command-line interface for accessing your grades; it spits out the raw dictionary-based or xml grades for your own application.

```(rawGrades.py -u <username> -p <password> -i <district-id> -c <optional: uses existing save file> -x <optional: spits out xml instead of default dictionary)```

## Dependencies
The Infinite Campus Python API uses a few dependencies which can all be obtained through pip. These include: `ast`, `xmltodict`, `requests`, `collections`, & `getpass`.
