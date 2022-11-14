# Description

The purpose of this project is to take the interest of students on working/leading a 
project, form teams given customizable constraints, and return a document containing
the results.

# Requirements

The CSV file containing the interests of the students must contain the following 3 columns (names of the columns don't have to be the same, but must serve the same purpose)

- Name
- Interested
- Interested in Leading

Example of acceptable CSV input file

```
Timestamp,Name,Random Question?,Interested?,Leader

2022/11/10 5:45:46 PM PST,Breach,Yes,Blu;Red,Red
2022/11/10 6:45:46 PM PST,Cypher,Yes,Blu;Gre,Blu;Gre
2022/11/10 7:45:46 PM PST,Raze,No,Red;Gre;Yel,Blu;Red;Yel
```

It's important that the answers in the Interested?,Leader columns for every student are separated by semicolons

Downloading CSV file directing from Google Form will produce an
acceptable file

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

findAllProjects() finds all projects that have >0 interest by analyzing inputMatrix


## Step 3)

A preference matrix is made with addStudents() where each row is a student and each
column is a specific project. 

Each element represents the level of interest a student has towards a project:
- 0 = no interest
- 1 = interested
- leaderValue + 1 = interested in leading

Leadervalue is set to be a number > total number of students in order to differentiate
between students and leaders. 

To find total unique people interested in project, the total interest can be modded by the leader value.


## Step 4)

Teams are assigned based on constraints given using assignPlayersToProjects().

The current method prioritizes projects with just enough interest to make a team and each
team created is guaranteed to have 1 leader.


## Step 5)

Using the results from Step 5, a CSV file is created with createCSVfile() that nicely
organizes the different teams and their projects in a CSV file.

getStudentInfo() is used to generate each student row for the CSV file based on the columns
from the inputMatrix. This is meant to be used to include contact information.
