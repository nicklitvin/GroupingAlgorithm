"""
DESCRIPTION

The following code splits students and leaders into teams
based on their preferences on projects while making sure 
that each team has 1 leader and has a specified size

It is assumed that each person taking the form can specify 
whether they are interested in the project or want to lead the 
project 

The approach to solving this problem is to form teams for a project
that has just enough interest to form a team since there are not 
that many different ways to make a team from these people

It is much harder for projects that could form 10 teams, there are too many
possibilities to consider

A consequence of this approach is that the most popular projects may
not have any team working on it depending on the user specifications

To run custom specifications, scroll to #USER-INPUT and change 
the values and make sure RUN_USER_CODE is set to True

If there are some other stuff showing up in the console, make
sure RUN_TESTS is set to False
"""

import math, random

def generatePreferences(projectCount,studentCount,preferencesNum,leaderChance):
    """
    INPUT
    projectCount,studentCount: self-explanatory
    preferencesNum: max number of unique preferences student can have

    OUTPUT
    2D list where each row represents a student and each column
    is the project number

    Possible values are 0,1,and LEADER_VALUE
    0 means student is not interested in a project
    1 means student is interested
    LEADER_VALUE means student wants to lead the project
    """
    studentPreferenceList = []

    # create 2d preference matrix
    for _ in range(studentCount):
        studentPreferenceList.append([0] * projectCount)
    
    # add preferences
    for studentIndex in range(len(studentPreferenceList)):
        preferncesToAdd = preferencesNum
        while preferncesToAdd > 0:
            projectLiked = math.floor(random.random() * projectCount)
            isLeader = True if random.random() < leaderChance else False
            
            if isLeader:
                studentPreferenceList[studentIndex][projectLiked] = 1
            else:
                studentPreferenceList[studentIndex][projectLiked] = LEADER_VALUE + 1
                
            preferncesToAdd -= 1
    
    return studentPreferenceList

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

def assignPlayersToProjects(summary,preferences,studentCount,minTeamSize,maxTeamSize,maxTeamsPerProject):
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
                    elif preferences[studentIndex][projectSummary[0]] == LEADER_VALUE + 1:
                        leadersReady.append(studentIndex)

            # check if there is enough available people to make a team, otherwise project is not happening
            if len(studentsReady) + len(leadersReady) < minTeamSize % LEADER_VALUE:
                unluckyProjects.append(projectSummary[0])
                continue

            # find best combo
            groupMin, remainder = findBestSplit(len(studentsReady)+len(leadersReady),minTeamSize%LEADER_VALUE,maxTeamSize%LEADER_VALUE)
            
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
            if len(teamsCreated[-1]) < minTeamSize % LEADER_VALUE:
                for studentIndex in teamsCreated[-1]:
                    peopleTaken[studentIndex] = 0
                teamsCreated.pop()

            # change status of students in project to taken
            for team in teamsCreated:
                for person in team:
                    peopleTaken[person] = 1
            
            projectsAssigned[projectSummary[0]] = teamsCreated

    sadPlayerCount = len(peopleTaken) - sum(peopleTaken)
    
    return unluckyProjects,projectsAssigned,sadPlayerCount


# USER INPUT

PROJECT_COUNT = 50
STUDENT_COUNT = 350
PREFENCES_NUM = 4
LEADER_VALUE = 10000
MIN_TEAM_SIZE = LEADER_VALUE + 5
MAX_TEAM_SIZE = LEADER_VALUE + 7
LEADER_CHANCE = 0.2
MAX_TEAMS_PER_PROJECT = 2

RUN_USER_CODE = True

if RUN_USER_CODE:

    preferences = generatePreferences(PROJECT_COUNT,STUDENT_COUNT,PREFENCES_NUM,LEADER_CHANCE)

    summary = summarizePreferences(preferences)

    unpopular, results, sadPeople = assignPlayersToProjects(summary,preferences,STUDENT_COUNT,MIN_TEAM_SIZE,MAX_TEAM_SIZE,MAX_TEAMS_PER_PROJECT)

    # print("preferences")
    # for row in preferences:
    #     print(row)
    print(f"\nsummary \n {summary}")
    print(f"\nunpopularProjects: {unpopular}")
    print(f"results: {results}")
    print(f"sadPeople: {sadPeople}")

# TESTS

RUN_TESTS = False

if RUN_TESTS:
    assert(findBestSplit(21,5,7) == (7,0))
    assert(findBestSplit(16,5,7) == (5,1))
    assert(findBestSplit(10,5,8) == (5,0))
    assert(findBestSplit(3,3,4) == (3,0))

    preferences = [
        [10001, 0,      0],
        [1,     0,      0],
        [0,     0,  10001],
        [10001, 0,      0],
        [0,     0,      1],
        [0,     10001,  0],
        [0,     10001,  0],
        [0,     0,  10001],
        [1,     0,      1],
        [0,     10001,  1]
    ]

    summary = summarizePreferences(preferences)
    assert(summary == [[0,20004],[2,20005],[1,30003]])

    unpopular, results, sadPeople = assignPlayersToProjects(summary,preferences,10,10004,10005,2)
    print(unpopular,results,sadPeople)
