# Use cases Coach
Here you will find all the use cases

## Review student

In this situation a coach will make a recommendation about a student based onto the students skills and motivation.

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

The student had to been approved by an OKBE employee

### Postconditions

The recommendation made by the coach is immediately visible to other users.

A student can be added to a project by a coach.

An admin will make the final decision.

### Actoren

The coach

### Description off steps

1. (If you want to review a specific student based on search criteria see the search for students use case)
2. First click on the student you want to review then you will be shown the information there is about that student.
3. (There might be real time reviews of other people than you can use to help make your own decisions)
4. After you looked at the student it’s time to make a recommendation. You can choose between “yes”, “maybe” or “no”. It is possible to argument why you made this decision so others can understand it.

## Add student to project

In this situation a coach will add a student to a specific project they seem fit for.

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

The student has received positive reviews from coaches

### Postconditions

The project choice made by the coach is immediately visible to other users.

The admin will confirm the assignment of the student and will send an email to the student and later send the contract.

### Actoren

The coach

### Description off steps

1. First you can search for a specific project or go to the project overview
2. (If you want to assign a specific student based on search criteria see the search for students use case)
3. Drag the student from the list of students to the chosen project.
4. Choose the role this student will have in the team and argument why this student is a good fit for this project
5. (Other users can in real time add other students to the same project and view your assignments)
6. Make sure there are no conflicts between students and projects.

## Change or remove review

In this situation a coach wants to change its recomendation they made about a student (typo or wrong student)

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

The student already recieved a review from the coach

### Postconditions

The changed recommendation made by the coach is immediately visible to other users.

A student can be added to a project by a coach based on the new review.

An admin will make the final decision.

### Actoren

The coach

### Description off steps

1. (If you want to change the review of a specific student based on search criteria see the search for students use case)
2. First click on the student you want to change the review for, click the edit recomendation button.
3. (There might be real time reviews of other people than you can use to help make your own decisions)
4. After you looked at the student for the second time it’s time to make your new recommendation. You can again choose between “yes”, “maybe” or “no”. It is possible to argument why you made this new decision so others can understand it.

## Search students

In this situation a coach tries to find specific students based on skills or other filters

### Preconditions

The current user (a coach) has created an account and is approved by an admin.

### Postconditions

The found students can be reviewed or added to projects

### Actoren

The coach

### Description off steps

1. First of all you may want to clear any previous filters set.
2. You can search based name, alumni, student coach, skills/roles or based on reviews of others
3. You can now review the student or assign the student to a project

# Create Account
## Description
A new user(admin or coach) must create an account in order to use the tool
## Preconditions
The user has never before created an account and is not known to the tool
## Postconditions
The user has an account, but this is yet to be approved by an admin
## Actors
Coach or Admin
## Description of steps
* fill in username/email (one of these or both?)
* fill in your password
* confirm your password
* click a "create account" button
* a "hold on tight" window is shown
* an email is sent to (all?) admins to request approval
* (you receive an email once you've been verified?)
## Description of alternative flows
The person is the first to ever create an account:
* automatically accept this user as an admin
* the main window is shown instead of the "hold on tight" window

Signup via github instead of filling in username/password:
* you click the login with github button
* you give the tool access to your account


# Login
## Description
Every time a recurring user(admin or coach) returns, the user must be reauthenticated in order to use the tool
## Preconditions
The user has previously created an account
The user might not have been verified by an admin
## Postconditions
The user has acces to the tool
## Actors
Coach or Admin
## Description of steps
* fill in username/email (one of these or both?)
* fill in your password
* click the login button
* the main window is shown, you have access to the tool
## Description of alternative flows
Password incorrect/user unknown:
* you get an error message saying your username/password combination is incorrect

Not yet verified:
* you get an error message saying your account has not been verified yet

Login via github instead of filling in username/password:
* you click the login with github button

## Make project

A admin adds projects that the students will be making that summer.

### Preconditions

* The user has created an account that is approved by an admin.
* The user has been made admin by another admin
* The user is on the 'mangement' page

### Postconditions

The project is visable
Students can be added to the project

### Actoren

An admin

### Description of steps

1. The user clicks on the button 'new project'
2. Fill in the details of the project.
3. If the partner is not already in a list of partners, add the partner
4. The user clicks a 'save' button

## Edit Project

If there's a mistake and the information of a project is not correct.

### Preconditions

* The user has created an account that is approved by an admin.
* The user has been made admin by another admin
* The user is on the 'mangement' page
* There is a project created by an admin with incorrect information

### Postconditions

The changes are directly visable.

### Actoren

An admin

### Description of steps

1. The user clicks on a button 'edit'
2. Change the wrong details
3. If the partner need to be removed, remove the partner and automaticly all the projects of this partner need to be removed
4. If the partner is wrong, and not in a list of partners, add the partner
5. If the information of the partner is wrong, change the information of the partner
6. The user clicks on a save edits button

## Remove a project

When a partner pull out with one or more projects, an admin should remove the project.

### Preconditions 

* The user has created an account that is approved by an admin.
* The user has been made admin by another admin
* The user is on the 'mangement' page
* There is a project created by an admin that the partner don't want to do anymore

### Postconditions

* The deleted project is not visible anymore
* There can't be added students to the delted project anymore
* All students that where added on that project are free again to be set on an other project
* All coaches set on that project, aren't anymore

### Actoren

An admin

### Description of steps

1. The user clicks on a 'delete project' button
2. The user get a pop up "are you sure"
3. The user clicks on "yes"

## Approve new coaches

when a new user wants to join an admin has to approve him.

### Preconditions

* The user has created an account that is approved by an admin.
* The user has been made admin by another admin
* The user is on the 'mangement' page
* There is at least one person who made a new account

### Postconditions

* The user who is approved is out of the request list
* The user is on the 'mangement' page
* The user who made the request is a new coach
* The user who made the request is visible in the list of users

### Actoren

An admin

### Description off steps

1. the admin clicks on 'approve'

## Deny new coaches

when a new user wants to join an admin has to approve him.

### Preconditions

* The user has created an account that is approved by an admin.
* The user is on the 'mangement' page
* The user has been made admin by another admin
* The user is on the 'mangement' page
* There is at least one person who made a new account

### Postconditions

* The user who is denied is out of the request list

### Actoren

An admin

### Description off steps

1. the admin clicks on 'deny'

## Change user status

If a coach is promoted to admin, an admin demoted to coach, a coach/admin don't want to be active anymore, or there was a simple misclick, the user's status has to change

### Preconditions

* The user has created an account that is approved by an admin.
* The user is on the 'mangement' page
* The user has been made admin by another admin
* The other user has the status coach, admin or deactivated

### Postconditions

* The changes are directly visible for all admins
* If the change involved with less access, and the other user is on a page he may not see anymore, he is redirected to the home page
* If the user is now not active anymore, he is signed out

### Actoren

An admin

### Description of steps

1. The user clicks on a combobox at another user
2. The user clicks on the new role of that other user

## Remove data of a student

When a student don't wants to be in the concidered as a candidate for OSOC. They have to be deleted from the database

### Preconditions

* The user has created an account that is approved by an admin.
* The user has been made admin by another admin
* The student has informed an amdin
* The user is on the page where he sees all info of that student

### Postconditions

* The student is not visible anymore
* The student can't be added to any projects
* The student is removed from all projects
* All reviews of that student are deleted

### Actoren

An admin

### Description of steps

1. The user clicks on a button 'remove student'
2. The user get a pop up "are you sure"
3. The user clicks on "yes"
