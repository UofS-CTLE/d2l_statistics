# d2l_statistics
d2lstat.py is a script to calculate statistics about Desire 2 Learn usage for a given semester.

The script relies upon three files: 

* The D2L Usage data that comes from Desire 2 Learn.
* The list of Full Time Faculty members.
* The list of part time faculty members.

All of these files need to be opened in LibreOffice Calc and then saved as .csv files with Pipes ("|") as the delimiter of the .csv file

The script can be run in the following way:

`python3 d2lstat.py usage.csv full.csv part.csv 2018_Fall 1319`

Everything that comes after the name of the script are parameters that are passed into the script:

The first parameter is usage.csv. This is the name of the usage file that comes from Desire 2 Learn.

full.csv is the name of the file that contains a listing of all full time faculty.

part.csv is the name of the file that contains a listing of all part time faculty.

2018_Fall is the semester of interest. This **must** be entered exactly as it appears in the cells under the "Course Offering Code" column of the usage.csv file.

1319 is the number of courses that are being taught in the semester that you are running the script for. This number is provided by the Registrar's Office. This number will change based on the semester and it is used in the report that the script produces. 

After the script runs, given that it ran successfully, there will be a .pdf file containing the stats report in the directory that the script is in.