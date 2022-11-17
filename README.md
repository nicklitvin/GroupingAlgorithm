# Description

The purpose of this project is to take the interest of students on working/leading a 
project, form teams given customizable constraints, and return a document containing
the results.

**match.py** randomly generates student input and forms groups based on custom arguments (no CSV file required)

**combined.py** takes in CSV input, processes it, and outputs result

# Requirements

The CSV file containing the interests of the students must contain the following 3 columns (names of the columns don't have to be the same, but must serve the same purpose)

- Name
- Interested
- Interested in Leading

Example of acceptable CSV input file exported directly from Google Form: (testCSVprocess.csv)

```
Timestamp,Name,Random Question?,Interested?,Leader

2022/11/10 5:45:46 PM PST,Breach,Yes,Blu;Red,Red
2022/11/10 6:45:46 PM PST,Cypher,Yes,Blu;Gre,Blu;Gre
2022/11/10 7:45:46 PM PST,Raze,No,Red;Gre;Yel,Blu;Red;Yel
```

Example of acceptable CSV input file exported from Google Sheets after import from Google Form:
(same as file above except combined values such as "Blu;Red" are written as "Blu, Red")

```
Timestamp,Name,Random Question?,Interested?,Leader

2022/11/10 5:45:46 PM PST,Breach,Yes,"Blu, Red",Red
2022/11/10 6:45:46 PM PST,Cypher,Yes,"Blu, Gre","Blu, Gre"
2022/11/10 7:45:46 PM PST,Raze,No,"Red, Gre, Yel","Blu, Red, Yel"
```

# How to Run

- Place your CSV file in the same directory as **combined.py**

- Edit input/output file names, team constraints, and output format in **combined.py**  under **#USER INPUT**

- Run the following code in the terminal

```
py ./combined.py
```

# How the code works

## Step 1)

The CSV file is transformed into a 2d list with getFileMatrix(), call it inputMatrix


## Step 2)

convertToProperCSV() is called on inputMatrix to change elements with multiple values so that they are separated by semicolons as opposed to commas and spaces if not already in that form

## Step 3)

findAllProjects() finds all projects that have >0 interest by analyzing inputMatrix


## Step 4)

A preference matrix is made with addStudents() where each row is a student and each
column is a specific project. 

Each element represents the level of interest a student has towards a project:
- 0 = no interest
- 1 = interested
- leaderValue + 1 = interested in leading

Leadervalue is set to be a number > total number of students in order to differentiate
between students and leaders. 

To find total unique people interested in project, the total interest can be modded by the leader value.


## Step 5)

Teams are assigned based on constraints given using assignPlayersToProjects().

The current method prioritizes projects with just enough interest to make 1 team followed by the
more popular projects.


## Step 6)

Using the results from Step 5, a CSV file is created with createCSVfile() that nicely
organizes the different teams and their projects in a CSV file.

getStudentInfo() is used to generate each student row for the CSV file based on the columns
from the inputMatrix. This is meant to be used to include contact information.
