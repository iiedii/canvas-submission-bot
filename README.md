# Canvas Student Score Submission Bot

My college is using *[Canvas system](https://www.canvaslms.com/)* to manage student records. As a teaching assistant, it was a headache for me to upload scores with comments for 300+ students in my course. Canvas did provide a method to batch upload scores by an Excel table, however it doesn't include comments. In the end, I developed this submission bot to automate the process of uploading both the score and comments for each student. It was welcomed by lecturers and other teaching assistants.

## Important Notes

This project was done by emulating a browser's submitting process. I analyzed the communication between the browser and server when a user was submitting scores. Due to the nature of this hack, the code is subject to the version of Canvas system used by my college. It may not work on the current version. If it doesn't work, usually the problem lies in the update of the user authentication process. You might want to look into that part if you are trying to apply this code directly.

[![Python version](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/download/releases/2.7/)
![Maintenance](https://img.shields.io/badge/maintained%3F-no-red.svg)

-------------------------------------------------

## Setup

It's fairly simple. All code is inside the single file [CanvasAutoSubmit.py](CanvasAutoSubmit.py). Just make sure you have the *[requests](https://pypi.org/project/requests/)* and *[bs4](https://pypi.org/project/beautifulsoup4/)* installed. Then you need to config [CanvasAutoSubmit.ini](CanvasAutoSubmit.ini).

### An example of *CanvasAutoSubmit.ini*

```
{
    "TA_Password": "xxxxxxxx",
    "ScoreAndCommentFile": "D:\\Documents\\TA\\CS1103\\gather_to_upload.tsv",
    "CourseID": "7740",
    "TA_UserID": "xxxxxxxx",
    "SubmitNRecordsOnly": 3,
    "AssignmentID": "15567",
    "SubmitScoreOrComment": -1
}
```

### Note the following settings:

```
"SubmitScoreOrComment": -1    # set -1 will upload both scores and comments, 1 for comments only, 2 for scores only
"SubmitNRecordsOnly": 3       # for testing purpose, try 3 to only upload records for 3 students. Otherwise, -1 to upload all
```

### An example of *ScoreAndCommentFile*

Each line is a student record.

The format: {student_name}\t{canvas_id}\t{total_score}\t{comment}

The comments must be encoded by URL encoding. A handy tool to generate this file is provided **[HERE](tools/gather_to_upload.py)**. It takes the Excel table file that can be downloaded from the Canvas system as input. This tool is for reference only. Change it on your need.

```
CHAN  X X	60893	4.5	Nice%20work.%0A-----------------------------------%0AUse%20of%20an%20image%3A%201.0%0AUse%20of%20a%20custom%20font%3A%201.0%0AUse%20of%20loops%3A%201.0%0ACreativity%3A%201.5%0A-----------------------------------%0ATotal%3A%204.5
CHAU  X X	46465	3.0	No%20custom%20font.%20Improper%20indentations.%0A-----------------------------------%0AUse%20of%20an%20image%3A%201.0%0AUse%20of%20a%20custom%20font%3A%200.0%0AUse%20of%20loops%3A%201.0%0ACreativity%3A%201.5%0AReadability%3A%20-0.5%0A-----------------------------------%0ATotal%3A%203.0
FU  X	59101	4.5	Nice%20art%20work.%0A-----------------------------------%0AUse%20of%20an%20image%3A%201.0%0AUse%20of%20a%20custom%20font%3A%201.0%0AUse%20of%20loops%3A%201.0%0ACreativity%3A%201.5%0A-----------------------------------%0ATotal%3A%204.5
ITTIX  X	45955	0.0	No%20submission.%0A-----------------------------------%0A-----------------------------------%0ATotal%3A%200.0

```

-------------------------------------------------

## Pay Attention

1. DO NOT change the format in the .ini file! For example, when you edit:
   ```
    "TA_Password": "xxxxxxxx",
   ```
   just carefully replace those xxxxxxxx without touching the "":
   ```
    "TA_Password": "iamyourpassword",
   ```

2. DOUBLE CHECK your assignment ID! Otherwise you are in a **RISK of OVERLAPPING an existing assignment**!

3. ALWAYS REMEMBER: your password is stored in plain text in the .ini file!

4. Wait until you see "Job done." to ensure it finishes submitting. On error, check the log file.
