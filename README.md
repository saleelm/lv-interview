# lv-interview

# Task-1
Write a small project to verify testcase A and Testcase B on ASG . 
#### ``` Note: ASG stands for AWS Auto Scaling groups.```
## Pass/Assertion Criteria:

####Testcase:- A
 * 1- ASG desire running count should be same as running instances. if mismatch fails
 * 2- if more than 1 instance running on ASG, then ec2 instance should on available and distributed on multiple availibity zone. 
 * 3- SecuirtyGroup, ImageID and VPCID should be same on ASG running instances. Do not just print.
 * 4- Findout uptime of ASG running instances and get the longest running instance.

####Testcase:- B
 * Find the Scheduled actions of as which is going to run next and calcalate elapsed in hh:mm:ss from current time.
 * Calculate total number instances lunched and terminated on current day.


## Expectation from your project:
 * Validation of above pass criteria in your project
 * Handling of Edge case and Empty reponse
 

# Further important instruction:

##  Don't: :no_entry_sign:
* Please do not check-in your received Access key ID and Secret access key. You can look at an example share on sample.py[https://github.com/csingh-livevox/lv-interview/blob/main/sample.py] for how to do it without expose/hardcoding into your project.

## Do's: :tick:
* Please use python and/or its any test framework
* Please use modular coding to do the same.
* Once done, please host the code on your public repo on github and share the link.
https://github.com/youruser_name/livevox-assignment-task-1                                                           

``` Good Luck, Happy Coding !```
