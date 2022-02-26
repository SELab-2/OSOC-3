# Use cases Coach
Here you will find all the use cases

## Review student

In this situation a coach will make a recommendation about a student based onto the students skills and motivation.

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

The student has been approved by an OKBE employee. (can legally work and is in timezone)

### Postconditions

The recommendation made by the coach is immediately visible to other users.

### Actoren

The coach

### Description of steps

1. Navigate to student
2. First click on the student you want to review then you will be shown the information there is about that student.
3. (There might be real time reviews of other people than you can use to help make your own decisions)
4. After you looked at the student it’s time to make a recommendation. You can choose between “yes”, “maybe” or “no”. It is possible to argument why you made this decision so others can understand it.

## Add student to project

In this situation a coach will add a student to a specific project they seem fit for.

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

The coach is assigned to the project they want to add the student to.

### Postconditions

The project choice made by the coach is immediately visible to other users.

The admin will confirm the assignment of the student and will send an email to the student and later send the contract.

### Actoren

The coach

### Description of steps

1. First you can search for a specific project or go to the project overview
2. (If you want to assign a specific student based on search criteria see the search for students use case)
3. Drag the student from the list of students to the chosen project.
4. Choose the role this student will have in the team and argument why this student is a good fit for this project
5. (Other users can in real time add other students to the same project and view your assignments)
6. Make sure there are no conflicts between students and projects.

## Change or remove review

In this situation a coach wants to change its recommendation they made about a student (typo or wrong student).

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

The student already received a review from the coach.

### Postconditions

The changed recommendation made by the coach is immediately visible to other users.

### Actoren

The coach

### Description of steps

1. Navigate to the student you want to change the review for.
2. Click the edit recommendation button.
3. There might be real time reviews of other people than you can use to help make your own decisions
4. After you looked at the student for the second time it’s time to make your new recommendation. You can again choose between “yes”, “maybe” or “no”. It is possible to argument why you made this new decision so others can understand it.

## Search students

In this situation a coach tries to find specific students based on skills or other filters.

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

### Postconditions

The found students can be reviewed or added to projects.

### Actoren

The coach

### Description off steps

1. First of all you may want to clear any previous filters set.
2. You can search based on name, alumni, student coach, skills/roles, practical information, availability or based on reviews of others.
3. Click on a student.

## Create Account
### Description
A new user must create an account in order to use the tool.
### Preconditions
The user has never before created an account and is not known to the tool.
### Postconditions
The user has an account, but this is yet to be approved by an admin.
An is sent to all admins to request approval.
Admins can see this in the manage users tab.
### Actors
User
### Description of steps
* fill in name
* fill in your email
* fill in your password
* confirm your password
* click a "create account" button
* a "hold on tight" window is shown
* you receive an email once you've been verified
### Description of alternative flows
The person is the first to ever create an account:
* automatically accept this user as an admin
* the main window is shown instead of the "hold on tight" window

Signup via github instead of filling in username/password:
* you click the login with github button
* you give the tool access to your account


## Login
### Description
Every time a recurring user returns, the user must be reauthenticated in order to use the tool.
### Preconditions
The user has previously created an account.
The user might not have been verified by an admin.
### Postconditions
The user has acces to the tool.
### Actors
User
### Description of steps
* fill in email 
* fill in your password
* click the login button
* the main window is shown, you have access to the tool
### Description of alternative flows
Password incorrect/user unknown:
* you get an error message saying your username/password combination is incorrect

Not yet verified:
* you get an error message saying your account has not been verified yet

Login via github instead of filling in username/password:
* you click the login with github button

## Make project

An admin adds projects that the students will be making that summer.

### Preconditions

* The current user is logged in as an admin.

### Postconditions

The project is visible.
Students can be added to the project.

### Actoren

An admin

### Description of steps

1. Navigate to the management page.
2. The user clicks on the button 'new project'
3. Fill in the details of the project.
4. Select a partner
5. The user clicks a 'save' button

### Description of alternative flows
The partner is not yet in the list of partners
* add the partner

## Edit Project

If there's a mistake and the information of a project is not correct.

### Preconditions

* The current user is logged in as an admin.
* There is a project created by an admin with incorrect information.

### Postconditions

The changes are directly visible.

### Actoren

An admin

### Description of steps

1. Navigate to the management page
2. The user clicks on a button 'edit'
3. Change the wrong details
4. The user clicks on a save edits button

## Remove a project

When a partner changes their mind about one or more projects, an admin should remove the project.

### Preconditions 

* The current user is logged in as an admin.
* There is a project created by an admin that the partner doesn't want to do anymore

### Postconditions

* The deleted project is not visible anymore
* No more students can be added to the project
* All students that where added on that project are free again to be set on an other project
* All coaches set on that project, aren't anymore

### Actoren

An admin

### Description of steps

1. Navigate to the management page
2. The user clicks on a 'delete project' button
3. The user gets a popup "are you sure?"
4. The user clicks on "yes"

### Description of alternative flows
Cancel removal of project:
* click the cancel button on the popup
* you return to the previous window, nothing changes

## Approve new coaches

When a new user wants to join an admin has to approve him.

### Preconditions

* The current user is logged in as an admin.
* There is at least one person who made a new account.

### Postconditions

* The user who is approved is out of the request list.
* The user who made the request is a new coach.
* The user who made the request is visible in the list of users.

### Actoren

An admin

### Description of steps

1. the admin clicks on 'approve'

### Description of alternative flows
Deny coach:
1. the admin clicks on 'deny'
2. remove the coach from the tool


## Change user status

If a coach is promoted to admin, an admin demoted to coach, a coach/admin doesn't want to be active anymore, or there was a simple misclick, the user's status has to change.

### Preconditions

* The current user is logged in as an admin.
* The other user has the status coach, admin or deactivated.

### Postconditions

* The changes are directly visible for all admins.
* If the change involved with less access, and the other user is on a page he may not see anymore, he is redirected to the home page.
* If the user is now not active anymore, he is signed out.

### Actoren

An admin

### Description of steps

1. The user clicks on a combobox of another user
2. The user clicks on the new role of that other user

## Remove data of a student

When a student doesn't want to be considered as a candidate for OSOC. They have to be deleted from the database.

### Preconditions

* The current user is logged in as an admin.
* The student has informed an admin.

### Postconditions

* The student is not visible anymore
* The student can't be added to any projects
* The student is removed from all projects
* All reviews of that student are deleted

### Actoren

An admin

### Description of steps

1. Navigate to the student that needs to be removed
2. The user clicks on a button 'remove student'
3. The user get a popup "are you sure?"
4. The user clicks on "yes"

### Description of alternative flows
Cancel removal of student data:
1. The user clicks on cancel in the popup
2. You return to the previous page, nothing has changed

## Remove student from project
### Description
if the student is no longer required in the project, the student needs to be removed
### Preconditions
The current user is logged in.
A student is assigned to a project.
### Postconditions
The student is removed from the project, this is immediately visible.
### Actors
Coach/Admin
### Description of steps
* navigate to the specific project
* click on the "remove" button next to the student name
* click the confirm button on the popup
* the student disappears from the project
### Description of alternative flows
Cancel removal of student from project:
* click the cancel button on the popup
* you return to the previous window, nothing changes


## Definitive decision on student
### Description
Admins have to make a definitive decision whether or not students can start working at OSOC.
### Preconditions
The current user is logged in as an admin.
Coaches have made their suggestions for the student.
### Postconditions
A decision for the student has been made.
### Actors
Admin
### Description of steps
* Navigate to the student
* Select a definitive status for the student
* Click confirm



## View sent emails
### Description
View a list of students showing what email has last been sent to them.
### Preconditions
The current user is logged in as an admin.
### Postconditions
A list of students with their last received email is shown.
### Actors
Admin
### Description of steps
* Click a "view all emails" button
* The list of students is shown. The list is ordered as "most recently sent"
### Description of alternative flows
Search a student by name/definitive decision status:
* only the search matches are shown
