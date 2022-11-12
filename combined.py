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

def summarizePreferences(matrix):
    """
    INPUT
    matrix: 2d list containing preferences, students are rows, projects are columns
    vals > 0 imply interest

    OUTPUT
    Counts how many total students are interested in each project
    Sorts the projects by ascending interest
    Returns list where each element is [projectNum, numStudentsInterested]
    """
    summary = []

    for projectNum in range(len(matrix[0])):
        projectSummary = [projectNum,0]
        for studentNum in range(len(matrix)):
            if matrix[studentNum][projectNum] > 0:
                projectSummary[1] += matrix[studentNum][projectNum]
        summary.append(projectSummary)
    
    summary.sort(key = lambda x: x[1])
    return summary

def findBestSplit(count,minSize,maxSize):
    """
    INPUT:
    count: number of students to split
    minSize: smallest team size considered to make equal teams
    maxSize: teams cannot surpass this size

    OUTPUT:
    returns most distribution as tuple
    and remainder means that many teams will have an extra team member
    Priority is given to team sizes closer to maxSize
    """
    bestSize = None
    bestRemainder = None

    if count % maxSize == 0:
        return (maxSize,0)

    for size in range(minSize,maxSize)[::-1]:
        remainder = count % size
        if remainder == 0:
            return (size,0)
        elif not bestRemainder or remainder < bestRemainder:
            bestSize = size
            bestRemainder = remainder 
    
    return (bestSize,bestRemainder)

def assignPlayersToProjects(summary,preferences,studentCount,minTeamSize,maxTeamSize,maxTeamsPerProject,leaderValue):
    """
    INPUT
    summary: list of projects and students interested in ascending order
    preferences: 2d matrix of students showing what project each student is interested in
    studentCount: self-explanatory
    minTeamSize: minimum team size required otherwise project is not happening
    maxTeamSize: absolute max team size that must not be overcome

    OUTPUT
    tuple with the following information:
    unluckyProjects: list of projects that do not have any teams working on them
    projectsAssigned: dict that contains all projects, and the teams that will be working on them
    sadPlayerCount: number of people that have not been assigned to a team
    """

    # each index in peopleTaken represents person, 1 => person has project
    peopleTaken = [0] * studentCount
    unluckyProjects = []
    projectsAssigned = {}
    
    for currentSummaryI in range(len(summary)):
        projectSummary = summary[currentSummaryI]

        # no way team can be made if not enough interest (in general)
        if projectSummary[1] < minTeamSize:
            unluckyProjects.append(projectSummary[0])
        else:
            studentsReady = []
            leadersReady = []

            # find all students and leaders interested in project (and are available)
            for studentIndex in range(len(preferences)):
                if peopleTaken[studentIndex] == 0:
                    if preferences[studentIndex][projectSummary[0]] == 1: 
                        studentsReady.append(studentIndex)
                    elif preferences[studentIndex][projectSummary[0]] == leaderValue + 1:
                        leadersReady.append(studentIndex)

            # check if there is enough available people to make a team, otherwise project is not happening
            if len(studentsReady) + len(leadersReady) < minTeamSize % leaderValue:
                unluckyProjects.append(projectSummary[0])
                continue

            # find best combo
            groupMin, remainder = findBestSplit(
                len(studentsReady)+len(leadersReady),
                minTeamSize % leaderValue,
                maxTeamSize % leaderValue
            )
            
            # create teams containing 1 leader and the rest are students
            teamsCreated = []
            currentStudent = 0
            currentLeader = 0
            
            while currentLeader < len(leadersReady):
                newTeam = []
                newTeam.append(leadersReady[currentLeader])
                currentLeader += 1
                
                lastPlayer = currentStudent + groupMin - 1
                if remainder > 0:
                    lastPlayer += 1
                    remainder -= 1
                newTeam += studentsReady[currentStudent:lastPlayer]
                currentStudent = lastPlayer

                # if no students left, but there are more leaders left, convert them to students
                if len(newTeam) <= groupMin:
                    lastLeader = currentLeader + groupMin - len(newTeam) - 1
                    newTeam += leadersReady[currentLeader:lastLeader + 1]
                    currentLeader = lastLeader + 1

                teamsCreated.append(newTeam)
            
            # delete teams if too many
            teamsCreated = teamsCreated[:maxTeamsPerProject]

            # release last team if not enough members
            if len(teamsCreated[-1]) < minTeamSize % leaderValue:
                for studentIndex in teamsCreated[-1]:
                    peopleTaken[studentIndex] = 0
                teamsCreated.pop()

            # change status of students in project to taken
            for team in teamsCreated:
                for person in team:
                    peopleTaken[person] = 1
            
            projectsAssigned[projectSummary[0]] = teamsCreated

    sadPlayerCount = len(peopleTaken) - sum(peopleTaken)
    unluckyProjects.sort()
    
    return unluckyProjects,projectsAssigned,sadPlayerCount


# USER INPUT

CSV_FILENAME = "testCSVprocess.csv"
INTEREST_COLUMN_NAME = "Interested?"
LEADER_COLUMN_NAME = "Leader?"
NAME_COLUMN_NAME = "Name"

LEADER_VALUE = 10000
MIN_TEAM_SIZE = LEADER_VALUE + 2
MAX_TEAM_SIZE = LEADER_VALUE + 3
MAX_TEAMS_PER_PROJECT = 1

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
    studentCount = len(studentAssociations.keys())
    summary = summarizePreferences(preferences)
    unpopular, results, sadPeople = assignPlayersToProjects(
        summary,preferences,studentCount,MIN_TEAM_SIZE,MAX_TEAM_SIZE,MAX_TEAMS_PER_PROJECT,LEADER_VALUE
    )

    print(f"\nsummary \n {summary}")
    print(f"\nunpopularProjects: {unpopular}")
    print(f"results: {results}")
    print(f"sadPeople: {sadPeople}")

# TESTS

RUN_TESTS = False

if RUN_TESTS:
    testCsvFileName = "testCSVprocess.csv"
    testNameColumnName = "Name"
    testInterestColumnName = "Interested?"
    testLeaderColumnName = "Leader?"
    testLeaderValue = 10000
    testMinTeamSize = testLeaderValue + 2
    testMaxTeamSize = testLeaderValue + 3
    testMaxTeamsPerProject = 1

    testMatrix = getFileMatrix(testCsvFileName)

    headerAssociations = getHeaderAssociation(testMatrix)
    assert(len(headerAssociations) == 5)
    assert(headerAssociations[testNameColumnName] == 1)
    assert(headerAssociations[testInterestColumnName] == 3)
    assert(headerAssociations[testLeaderColumnName] == 4)

    allProjects = findAllProjects(
        testMatrix,headerAssociations,testInterestColumnName,testLeaderColumnName
    )
    assert(allProjects == ["Blu","Gre","Red","Yel"])

    projectAssociations = makeProjectAssociation(allProjects)
    assert(len(projectAssociations.keys()) == 4)
    assert(projectAssociations["Blu"] == 0)
    assert(projectAssociations["Gre"] == 1)
    assert(projectAssociations["Red"] == 2)
    assert(projectAssociations["Yel"] == 3)

    preferences, studentAssociations = addStudents(
        testMatrix,projectAssociations,headerAssociations,testLeaderValue,
        testInterestColumnName,testLeaderColumnName,testNameColumnName
    )

    assert(preferences == [
        [1,                 0,                  testLeaderValue+1,  0           ],
        [testLeaderValue+1, testLeaderValue+1,  0,                  0           ],
        [testLeaderValue+1, 1,                  testLeaderValue+1,  testLeaderValue+1]
    ])

    assert(len(studentAssociations.keys()) == 3)
    assert(studentAssociations["Breach"] == 0)
    assert(studentAssociations["Cypher"] == 1)
    assert(studentAssociations["Raze"] == 2)

    summary = summarizePreferences(preferences)
    assert(summary == [
        [3,testLeaderValue + 1],
        [1,testLeaderValue + 1 + 1],
        [2,2*(testLeaderValue + 1)],
        [0,2*(testLeaderValue + 1) + 1]
    ])

    unpopular, results, sadPeople = assignPlayersToProjects(
        summary, preferences, len(studentAssociations.keys()), testMinTeamSize, 
        testMaxTeamSize, testMaxTeamsPerProject, testLeaderValue
    )

    assert(unpopular == [0,2,3])
    assert(len(results.keys()) == 1)
    onlyTeam = results[1][0]
    onlyTeam.sort()

    assert(onlyTeam == [1,2])

    assert(sadPeople == 1)
