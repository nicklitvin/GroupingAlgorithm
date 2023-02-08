import combined as C, os 

def runTests():
    testCsvFileName = "testCSVprocess.csv"
    testNameColumnName = "Name"
    testInterestColumnName = "Interested?"
    testLeaderColumnName = "Leader?"

    testMinTeamSize = 2
    testMaxTeamSize = 3
    testMaxTeamsPerProject = 1

    testOutputColumns = ["Name","Timestamp"]
    testOutputFilename = "testCSVResult.csv"

    try:
        os.remove(testOutputFilename)
        print("deleted existing output file")
    except:
        print("no output file exists before execution")

    testInputMatrix = C.getFileMatrix(testCsvFileName)
    testInputMatrixMinusHeaders = testInputMatrix[1:]

    testLeaderValue = C.getLeaderValue(testInputMatrixMinusHeaders)

    testHeaderNameToColumnIndex = C.getHeaderNameToColumnIndex(testInputMatrix)
    assert(len(testHeaderNameToColumnIndex) == 5)
    assert(testHeaderNameToColumnIndex[testNameColumnName] == 1)
    assert(testHeaderNameToColumnIndex[testInterestColumnName] == 3)
    assert(testHeaderNameToColumnIndex[testLeaderColumnName] == 4)

    testAllProjectList = C.findAllProjects(
        testInputMatrixMinusHeaders,testHeaderNameToColumnIndex,testInterestColumnName,testLeaderColumnName
    )
    assert(testAllProjectList == ["Blu","Gre","Red","Yel"])

    testProjectAssociations = C.makeProjectAssociations(testAllProjectList)
    testProjectNamesToProjectIndex = testProjectAssociations[0]
    testProjectIndexToProjectNames = testProjectAssociations[1]

    assert(len(testProjectNamesToProjectIndex.keys()) == 4)
    assert(testProjectNamesToProjectIndex["Blu"] == 0)
    assert(testProjectNamesToProjectIndex["Gre"] == 1)
    assert(testProjectNamesToProjectIndex["Red"] == 2)
    assert(testProjectNamesToProjectIndex["Yel"] == 3)

    assert(len(testProjectIndexToProjectNames.keys()) == 4)
    assert(testProjectIndexToProjectNames.get(0) == "Blu")
    assert(testProjectIndexToProjectNames.get(1) == "Gre")
    assert(testProjectIndexToProjectNames.get(2) == "Red")
    assert(testProjectIndexToProjectNames.get(3) == "Yel")

    testPreferences, testStudentNamesToRowIndex = C.addStudents(
        testInputMatrixMinusHeaders,testProjectNamesToProjectIndex,testHeaderNameToColumnIndex,testLeaderValue,
        testInterestColumnName,testLeaderColumnName,testNameColumnName
    )

    assert(testPreferences == [
        [1,                 0,                  testLeaderValue+1,  0           ],
        [testLeaderValue+1, testLeaderValue+1,  0,                  0           ],
        [testLeaderValue+1, 1,                  testLeaderValue+1,  testLeaderValue+1]
    ])

    assert(len(testStudentNamesToRowIndex.keys()) == 3)
    assert(testStudentNamesToRowIndex.get(0) == "Breach")
    assert(testStudentNamesToRowIndex.get(1) == "Cypher")
    assert(testStudentNamesToRowIndex.get(2) == "Raze")

    testSummary = C.summarizePreferences(testPreferences)
    assert(testSummary == [
        [3,testLeaderValue + 1],
        [1,testLeaderValue + 1 + 1],
        [2,2*(testLeaderValue + 1)],
        [0,2*(testLeaderValue + 1) + 1]
    ])

    testUnpopular, testProjectTeams, testSadPeople, testSadList = C.assignPlayersToProjects(
        testSummary, testPreferences, len(testStudentNamesToRowIndex.keys()), testMinTeamSize, 
        testMaxTeamSize, testMaxTeamsPerProject, testLeaderValue
    )

    assert(testUnpopular == [0,2,3])
    assert(len(testProjectTeams.keys()) == 1)

    testOnlyTeam = testProjectTeams[1][0]
    testOnlyTeam.sort()

    assert(testOnlyTeam == [1,2])
    assert(testSadPeople == 1)

    testResult = C.getStudentInfo(
        testInputMatrixMinusHeaders,0,
        testHeaderNameToColumnIndex,testOutputColumns
    )
    assert(testResult == '"Breach","2022/11/10 5:45:46 PM PST"')

    C.createCSVfile(
        testOutputFilename,testProjectTeams,testInputMatrixMinusHeaders,
        testProjectIndexToProjectNames,testHeaderNameToColumnIndex,testOutputColumns,
        testSadList
    )

    testResult = C.getFileMatrix(testOutputFilename)
    assert(testResult[0] == ["Gre"])
    assert(testResult[1] == ["Cypher","2022/11/10 5:45:49 PM PST"])
    assert(testResult[2] == ["Raze","2022/11/10 5:45:52 PM PST"])

    # testing csv conversion to matrix

    testInputMatrixMinusHeaders = [
        ["",""],
        ["red",""],
        ["","blu"],
        ["red, blu",""],
        ["","red, blu"],
        ["red, blu", "red,blu"],
        ["red;blu", "red;blu"]
    ]
    testInterestColumnName = "interest"
    testLeaderColumnName = "leader"
    testHeaderNameToColumnIndex = {testInterestColumnName:0,testLeaderColumnName:1}

    C.convertToProperCSV(testInputMatrixMinusHeaders,testHeaderNameToColumnIndex,testInterestColumnName,testLeaderColumnName)

    assert (testInputMatrixMinusHeaders == [
        ["",""],
        ["red",""],
        ["","blu"],
        ["red;blu",""],
        ["","red;blu"],
        ["red;blu", "red;blu"],
        ["red;blu", "red;blu"]
    ])

    # testing best splits

    assert(C.findBestSplit(21,5,7) == (7,0))
    assert(C.findBestSplit(16,5,7) == (5,1))
    assert(C.findBestSplit(10,5,8) == (5,0))
    assert(C.findBestSplit(3,3,4) == (3,0))

    # testing team assignment

    testPreferences = [
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

    testSummary = C.summarizePreferences(testPreferences)
    assert(testSummary == [[0,20004],[2,20005],[1,30003]])

    testNumberOfLeaders = 2
    testUnluckyProjects, testTeamsAssigned, testSadCount, testSadList = C.assignPlayersToProjects(
        testSummary,testPreferences,len(testPreferences),3,4,1,10000,testNumberOfLeaders
    )

    for projectNumber, teams in testTeamsAssigned.items():
        for team in teams:
            for i in range(testNumberOfLeaders):
                assert(testPreferences[team[i]][projectNumber] > 1)

    testNumberOfLeaders = 3
    testUnluckyProjects, testTeamsAssigned, testSadCount, testSadList = C.assignPlayersToProjects(
        testSummary,testPreferences,len(testPreferences),3,4,1,10000,testNumberOfLeaders
    )

    for projectNumber, teams in testTeamsAssigned.items():
        for team in teams:
            for i in range(testNumberOfLeaders):
                assert(testPreferences[team[i]][projectNumber] > 1)

    # testing team assignment bug

    testPreferences = [
        [10001, 0],
        [1,     0],
        [10001, 0],
        [10001, 0]
    ]

    testSummary = C.summarizePreferences(testPreferences)
    assert(testSummary == [[1,0],[0,30004]])

    testNumberOfLeaders = 2
    testUnluckyProjects, testTeamsAssigned, testSadCount, testSadList = C.assignPlayersToProjects(
        testSummary,testPreferences,len(testPreferences),3,3,1,10000,testNumberOfLeaders
    )

    assert(len(testSadList) == 1 and testSadList[0] == 3)

    for projectNumber, teams in testTeamsAssigned.items():
        for team in teams:
            for i in range(testNumberOfLeaders):
                assert(testPreferences[team[i]][projectNumber] > 1)

    # testing leaderValue generation

    testInputMatrixMinusHeaders = []

    for _ in range(259):
        testInputMatrixMinusHeaders.append([])

    testLeaderValue = C.getLeaderValue(testInputMatrixMinusHeaders)
    assert(testLeaderValue == 1000)

    print("tests passed")
    return