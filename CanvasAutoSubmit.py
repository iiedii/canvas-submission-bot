# -*- coding: utf-8 -*-
'''
Canvas Auto Submission Bot
    - for usage, please look into the README.md file.

Repacked on Oct 28, 2015

@author: James Lu
'''

import urllib
import sys
import os
import json
from requests import session
from bs4 import BeautifulSoup
from time import sleep


# Settings
CourseID = ''
AssignmentID = ''
ScoreAndCommentFile = r''
SubmitScoreOrComment = -1    # set -1 will upload both scores and comments, 1 for comments only, 2 for scores only
SubmitNRecordsOnly = 3       # for testing purpose, try 3 to only upload records for 3 students. Otherwise, -1 to upload all
TA_UserID = ''
TA_Password = ''


# Parameters for internal use, don't change
MainUrl  = 'https://canvas.cityu.edu.hk/courses/' + CourseID + '/gradebook'     # no use
LoginPostUrl = 'https://canvas.cityu.edu.hk/login/ldap'
SettingsFile = 'CanvasAutoSubmit.ini'
LogFile = 'CanvasAutoSubmit.log'


def Main(argv):
    LoadSettings()
    CheckPaths()
    with session() as sUploadScore:
        print 'Logging in...'
        CanvasLogin(sUploadScore)

        # Get grade book page
        res = sUploadScore.get(MainUrl)
        assert res.status_code == 200    # code != OK
        #print res.text
        SetupPayloadField(res.text)

        # Upload comments
        UploadComments(sUploadScore)

    print '\nJob done.'
    print 'Press Enter to exit...'
    raw_input()



# ----------------------------------------------------------------
# Load or save global settings to file
def SaveSettings():
    wrappedSettings = {
        'CourseID': CourseID,
        'AssignmentID': AssignmentID,
        'ScoreAndCommentFile': ScoreAndCommentFile,
        'SubmitScoreOrComment': SubmitScoreOrComment,
        'SubmitNRecordsOnly': SubmitNRecordsOnly,
        'TA_UserID': TA_UserID,
        'TA_Password': TA_Password
    }
    json.dump(wrappedSettings, fp=open(SettingsFile, 'w'), indent=4)


def LoadSettings():
    wrappedSettings = json.load(open(SettingsFile))
    global CourseID, AssignmentID, ScoreAndCommentFile, SubmitScoreOrComment, SubmitNRecordsOnly, TA_UserID, TA_Password, MainUrl
    CourseID = wrappedSettings['CourseID']
    AssignmentID = wrappedSettings['AssignmentID']
    ScoreAndCommentFile = wrappedSettings['ScoreAndCommentFile']
    SubmitScoreOrComment = wrappedSettings['SubmitScoreOrComment']
    SubmitNRecordsOnly = wrappedSettings['SubmitNRecordsOnly']
    TA_UserID = wrappedSettings['TA_UserID']
    TA_Password = wrappedSettings['TA_Password']
    MainUrl = 'https://canvas.cityu.edu.hk/courses/' + CourseID + '/gradebook'



# ----------------------------------------------------------------
# Global vars for internal use, don't change
PayloadLogin = {
    'utf8': '✓',
    'authenticity_token': '',
    'redirect_to_ssl': '1',
    'pseudonym_session[unique_id]': '',
    'pseudonym_session[password]': ''
}

PayloadComment = {
    'comment[text_comment]': '',     # user defined
}

PayloadScore = {
    'submission[posted_grade]': '',  # user defined
}

PayloadScoreAndComment = {
    'submission[posted_grade]': '',  # user defined
    'comment[text_comment]': '',     # user defined
}

PayloadSubmitField = {
    '_method': 'PUT',
    'authenticity_token': '',
    'page_view_id': ''
}


def updateUserInfoForPayloadLogin():
    PayloadLogin['pseudonym_session[unique_id]'] = TA_UserID
    PayloadLogin['pseudonym_session[password]'] = TA_Password


def getAuthToken(htmlText, tokenIdx):
    soup = BeautifulSoup(htmlText, 'html.parser')
    tokenTags = soup.find_all(attrs={'name': 'authenticity_token'})
    #assert len(tokenTags) == 2
    #for tag in tokenTags:
        #print tag
    return tokenTags[tokenIdx]['value']


def getPageViewID(htmlText):
    soup = BeautifulSoup(htmlText, 'html.parser')
    tokenTags = soup.find_all(id='page_view_id')
    assert len(tokenTags) == 1
    return tokenTags[0].string


def genCommentPostUrl(courseID, assignmentID, studentID):
    url = 'https://canvas.cityu.edu.hk/api/v1/courses/%s/assignments/%s/submissions/%s?include[]=visibility' % (courseID, assignmentID, studentID)
    return url


def payload2Str(payload):
    listComment = []
    for (k, v) in payload.items():
        listComment.append(k + '=' + v)
    #print '&'.join(listComment)
    return '&'.join(listComment)


def CheckPaths():
    if not os.path.exists(ScoreAndCommentFile):
        print 'Oops... ScoreAndCommentFile not found!'
        raw_input()
        sys.exit()


def CanvasLogin(session):
    res = session.get(MainUrl)

    #print 'Return status:', res.status_code
    assert res.status_code == 200   # code = OK
    #print res.text

    PayloadLogin['authenticity_token'] = getAuthToken(res.text, 0)
    updateUserInfoForPayloadLogin()
    session.post(LoginPostUrl, data=PayloadLogin)


def SetupPayloadField(htmlText):
    PayloadSubmitField['authenticity_token'] = getAuthToken(htmlText, 0)
    try:
        PayloadSubmitField['page_view_id'] = getPageViewID(htmlText)
    except AssertionError:
        print 'Oops... login failed!'
        raw_input()
        sys.exit()


def setComment(commentText):
    PayloadScoreAndComment['comment[text_comment]'] = PayloadComment['comment[text_comment]'] = commentText

def setScore(score):
    PayloadScoreAndComment['submission[posted_grade]'] = PayloadScore['submission[posted_grade]'] = '%s' % score


def UploadComments(session):
    with open(LogFile, 'w') as foutLog:
        with open(ScoreAndCommentFile) as fin:
            lineID = 0
            for line in fin:
                lineID += 1
                splitLine = line.split('\t')
                assert len(splitLine) == 4

                studentName = splitLine[0]
                studentID = splitLine[1]
                score = splitLine[2]
                comment = urllib.unquote(splitLine[3])
                setComment(comment)
                setScore(score)
                print '%s: %s' % (lineID, studentName)

                payload = None
                if SubmitScoreOrComment <= 0:
                    payload = PayloadScoreAndComment.copy()
                elif SubmitScoreOrComment == 1:
                    payload = PayloadComment.copy()
                elif SubmitScoreOrComment == 2:
                    payload = PayloadScore.copy()
                else:
                    raise ValueError('Wrong value in setting: SubmitScoreOrComment.')

                if payload is not None:
                    payload.update(PayloadSubmitField)
                    session.post(genCommentPostUrl(CourseID, AssignmentID, studentID), data=payload)
                    foutLog.write('%s: %s (%s) -> submitted.\n' % (lineID, studentName, studentID))

                sleep(1)        # for safety, delay 1 sec between submissions
                if SubmitNRecordsOnly > 0:
                    if lineID == SubmitNRecordsOnly:
                        foutLog.write('%s records were submitted.\n' % SubmitNRecordsOnly)
                        break
            foutLog.write("All records were submitted.\n")




if __name__ == '__main__':
    Main(sys.argv[1:])
    pass
