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