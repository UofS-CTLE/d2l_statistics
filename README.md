# d2l_statistics
The d2lstat.py script is a script that could be run to calculate statistics about Desire 2 Learn usage for a given semester. 
The script relies upon three files: 
The D2L Usage data that comes from Desire 2 Learn
The list of Full Time Faculty members
The list of part time faculty members

All of these files need to be opened in LibreOffice Calc and then saved as .csv files with Pipes(these things -->("|")) as the delimiter of the .csv file

 The script can be run in the following wayas an example:
 python3 d2lstat.py usage.csv full.csv part.csv 2018_Fall 1319

The script is written in python so that is why we put python3.
d2lstat.py is the name of the script.
Everything that comes after the name of the script are parameters that are passed into the script.
The first parameter is usage.csv. This is the name of the usage file that comes from Desire 2 Learn.
full.csv is the name of the file that contains a listing of all full time faculty.
part.csv is the name of the file that contains a listing of all part time faculty.
2018_Fall is the semester of interest. It is very important that this string be written exactly as it appears in the cells under the "Course Offering Code" column of the usage.csv file. The semester string should be written in the same format that the semester is written in in the beginning of each of the course offering codes pertaining to that semester. 
1319 is the number of courses that are being taught in the semester that you are running the script for. This number will be given to you, it comes from the Registrar's office. This number will change based on the semester and it is used in the report that the script produces. 

After the script runs, given that it ran successfully, there will be a .pdf file in the directory that the script is in. This will be the report of the Desire 2 Learn statistics.