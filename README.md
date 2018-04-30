# Infinite Campus API written in Python3
This project was made because of my want for a fast and easy API for Infinite Campus. This project is based off of @j-koreth 's Infinite-Campus-API-2 (https://github.com/j-koreth/Infinite-Campus-API-2)

## Current Progress
Yes, I am very well aware this code is messy and repeats everywhere. I am working on functionality first, then I will go back and make it more oop-like; do not 
worry. Currently, you can see all your grades and save a login for future reference. Once this project is complete or mostly complete, I will go back and comment 
my code for easier understanding.

## Usage
All scripts can be run by normal `python script.py` or by `chmod +x script.py` then `./script.py`.

`campus.py` returns all your current grades in the console based on semester choice. It also has a saved login feature that can be used with rawGrades.py.

`rawGrades.py` is a command-line interface for accessing your grades; right now, all it does is make sure everything connects properly.

```(rawGrades.py -u <username> -p <password> -i <district-id> -c <optional: uses existing save file>)```

## Dependencies
The Infinite Campus Python API uses a couple dependencies which can all be obtained through pip. These include: `ast`, `xmltodict`, `requests`, `collections`, & `getpass`.
