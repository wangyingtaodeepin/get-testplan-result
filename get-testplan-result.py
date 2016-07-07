#!/usr/bin/env python
# coding=utf-8

import xmlrpc.client
import json
import os

testplanid = os.getenv("testplanid")
buildid    = os.getenv("buildid")
TESTLINKAPIKEY = os.getenv("TESTLINKAPIKEY")
SERVER_URL = os.getenv("SERVER_URL")

userinfo = {}
userinfo["zhaofangfang"] = 34
userinfo["wangyanli"] = 17
userinfo["capricon"] = 23
userinfo["wangyingtao"] = 28

if None == testplanid or None == buildid or None == TESTLINKAPIKEY or None == SERVER_URL:
    print("Can not get the value of the params: testplanid or buildid.")
    exit(1)

class TestlinkAPIClient:
    def __init__(self, devKey):
        self.server = xmlrpc.client.ServerProxy(SERVER_URL)
        self.devKey = devKey

    def getInfo(self):
        return self.server.tl.about()

    def getProjects(self):
        return self.server.tl.getProjects(dict(devKey=self.devKey))

    def getPlaninfo(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestPlanByName(dictargs)

    def getBuildsForTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getBuildsForTestPlan(dictargs)

    def getTestcaseForTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestCasesForTestPlan(dictargs)

    def getTestCaseIDByName(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestCaseIDByName(dictargs)

    def createTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.createTestPlan(dictargs)

    def addTestCaseToTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.addTestCaseToTestPlan(dictargs)

    def getTestSuitesForTestPlan(self, dictargs):
        dictargs["devKey"] = self.devKey
        return self.server.tl.getTestSuitesForTestPlan(dictargs)

# substitute your Dev Key Here
client = TestlinkAPIClient(TESTLINKAPIKEY)

def getPlanResult(testplanid, assignedto_int):
    planargs = {}
    planargs["testplanid"] = testplanid
    planargs["assignedto"] = assignedto_int
    planargs["buildid"] = buildid
    plantestcases = client.getTestcaseForTestPlan(planargs)
    jsondata = {}
    jsondata['testcasedetail'] = []
    templist = []
    num_pass = 0
    num_fail = 0
    num_block = 0
    num_not_run = 0
    if plantestcases == '':
        return None

    for k in plantestcases.keys():
        templist.append(plantestcases[k][0])

        if 'p' == plantestcases[k][0]['exec_status']:
            num_pass = num_pass + 1
        elif 'f' == plantestcases[k][0]['exec_status']:
            num_fail = num_fail + 1
        elif 'b' == plantestcases[k][0]['exec_status']:
            num_block = num_block + 1
        elif 'n' == plantestcases[k][0]['exec_status']:
            num_not_run = num_not_run + 1

    templist.sort(key=lambda x:x['tcase_name'])

    jsondata['test_status_all'] = num_pass + num_fail + num_block + num_not_run
    jsondata['test_status_passed'] = num_pass
    jsondata['test_status_failed'] = num_fail
    jsondata['test_status_blocked'] = num_block
    jsondata['test_status_not_run'] = num_not_run
    jsondata['testcasedetail'] = templist

    return jsondata

alldata = {}
for k in userinfo.keys():
    data = getPlanResult(testplanid, userinfo[k])
    if data != None:
        alldata[k] = data

if not alldata:
    with open('tcase_detail.json', "w") as f:
        f.close()
    print("alldata is Null.")
    exit(1)

jsonstr = json.dumps(alldata, sort_keys=True, indent=4)
with open('tcase_detail.json', "w") as f:
    f.write(jsonstr)
    f.close()
