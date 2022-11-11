"""
DESCRIPTION

The following code reads a CSV file and creates a preference matrix 
based on what projects a student is interested in working on or interested in leading

Preferences is a 2d list where rows represent students and columns represent
project and the elements within represent a students interest towards a project

studentAssociations and projectAssociations are dicts that map student name
to row index and project name to column index in the preference matrix
"""

import csv

def getFileMatrix(fileName):
    """
    INPUT
    fileName of csv file, should be in same directory as this file

    OUTPUT
    2d list of values read from csv file
    """
    with open(fileName,"r") as csvfile:
        csvreader = csv.reader(csvfile)

        matrix = []

        for row in csvreader:
            matrix.append(row)
        
        return matrix

def getHeaderAssociation(matrix):
    """
    INPUT:
    2d list representing csv file

    OUTPUT:
    returns dict mapping headerNames to their columnIndex in the matrix
    """
    dict = {}
    for index,column in enumerate(matrix[0]):
        dict[column] = index
    return dict

def findAllProjects(matrix,headerAssociation,interestColumnName,leaderColumnName):
    """
    INPUT:
    matrix: 2d list of csv file
    headerAssociation: dict mapping headerNames to corresponding columnIndex
    interestColumnName: name of column to look for project interest
    leaderColumnName: name of column to look for project leader interest

    OUTPUT:
    returns sorted list of all unique projects that have any interest
    """
    interestColumnIndex = headerAssociation[interestColumnName]
    leaderColumnIndex = headerAssociation[leaderColumnName]
    
    interestedProjectsSet = set()

    for row in matrix[1:]:
        interestProjects = row[interestColumnIndex]
        interestProjectsList = interestProjects.split(";")

        leaderProjects = row[leaderColumnIndex]
        leaderProjectsList = leaderProjects.split(";")

        for projectName in interestProjectsList + leaderProjectsList:
            interestedProjectsSet.add(projectName)
    
    result = list(interestedProjectsSet)
    result.sort()
    return result

def makeProjectAssociation(projectNames):
    """
    INPUT
    list of projectNames

    OUTPUT
    dict mapping projectNames to columnIndex for creating preference matrix
    """
    projectAssociations = {}
    index = 0

    for projectName in projectNames:
        projectAssociations[projectName] = index
        index += 1
    
    return projectAssociations

def addStudents(matrix,projectAssociations,headerAssociations,leaderValue,interestColumnName,leaderColumnName,nameColumnName):
    """
    INPUT
    matrix: 2d list of csv file
    leaderValue: value added to interested leaders for a certain project

    OUTPUT
    preferences: 2d list where each student represents a student and each column represents a project.
    0 = no interest, 1 = interest, leaderValue + 1 = interested in leading project
    studentAssociations: Dict mapping student names to the corresponding row index in preferences
    """
    studentAssociations = {}
    studentIndex = 0

    totalProjects = len(projectAssociations.keys())

    nameColumnIndex = headerAssociations[nameColumnName]
    interestColumnIndex = headerAssociations[interestColumnName]
    leaderColumnIndex = headerAssociations[leaderColumnName]

    preferences = []

    for studentRow in matrix[1:]:
        personSummary = [0] * totalProjects

        studentAssociations[studentRow[nameColumnIndex]] = studentIndex
        studentIndex += 1

        interestProjects = studentRow[interestColumnIndex]
        leaderProjects = studentRow[leaderColumnIndex]

        interestProjectsList = interestProjects.split(";")
        leaderProjectsList = leaderProjects.split(";")

        for studentProject in interestProjectsList:
            personSummary[projectAssociations[studentProject]] = 1
        
        for leaderProject in leaderProjectsList:
            personSummary[projectAssociations[leaderProject]] = leaderValue + 1

        preferences.append(personSummary)
    
    return preferences, studentAssociations


# USER INPUT

CSV_FILENAME = "testCSVprocess.csv"
INTEREST_COLUMN_NAME = "Interested?"
LEADER_COLUMN_NAME = "Leader?"
NAME_COLUMN_NAME = "Name"
LEADER_VALUE = 10000

# RUN USER CODE

RUN_USER_CODE = True

if RUN_USER_CODE:
    matrix = getFileMatrix(CSV_FILENAME)
    headerAssociations = getHeaderAssociation(matrix)
    allProjects = findAllProjects(matrix,headerAssociations,INTEREST_COLUMN_NAME,LEADER_COLUMN_NAME)
    projectAssociations = makeProjectAssociation(allProjects)
    preferences, studentAssociations = addStudents(
        matrix,projectAssociations,headerAssociations,LEADER_VALUE,INTEREST_COLUMN_NAME,LEADER_COLUMN_NAME,NAME_COLUMN_NAME
    )

    print(f"student Associations: {studentAssociations} \n")
    
    print(f"preferences:")
    for row in preferences:
        print(f"{row}")

# TEST

testCsvFileName = "testCSVprocess.csv"
nameColumnName = "Name"
interestColumnName = "Interested?"
leaderColumnName = "Leader?"
leaderValue = 10000

testMatrix = getFileMatrix(testCsvFileName)

headerAssociations = getHeaderAssociation(testMatrix)
assert(len(headerAssociations) == 5)
assert(headerAssociations[nameColumnName] == 1)
assert(headerAssociations[interestColumnName] == 3)
assert(headerAssociations[leaderColumnName] == 4)

allProjects = findAllProjects(testMatrix,headerAssociations,interestColumnName,leaderColumnName)
assert(allProjects == ["Blu","Gre","Red","Yel"])

projectAssociations = makeProjectAssociation(allProjects)
assert(len(projectAssociations.keys()) == 4)
assert(projectAssociations["Blu"] == 0)
assert(projectAssociations["Gre"] == 1)
assert(projectAssociations["Red"] == 2)
assert(projectAssociations["Yel"] == 3)

interestMatrix, studentAssociations = addStudents(
    testMatrix,projectAssociations,headerAssociations,leaderValue,interestColumnName,leaderColumnName,nameColumnName
)

assert(interestMatrix == [
    [1,             0,              leaderValue+1,  0           ],
    [leaderValue+1, leaderValue+1,  0,              0           ],
    [leaderValue+1, 1,              leaderValue+1,  leaderValue+1]
])

assert(len(studentAssociations.keys()) == 3)
assert(studentAssociations["Breach"] == 0)
assert(studentAssociations["Cypher"] == 1)
assert(studentAssociations["Raze"] == 2)
