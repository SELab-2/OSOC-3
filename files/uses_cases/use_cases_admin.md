# Use Cases Admin

## Make project

An admin adds projects that the students will be making that summer.

| Make project ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. |
| Postconditions | The project is visible. <br> Students can be added to the project. |
| Actors| Admin |
| Description of steps | <ol><li>Navigate to the management page.</li><li>The user clicks on the button 'new project'</li><li>Fill in the details of the project.</li><li>Select a partner</li><li>The user clicks a "save" button</li></ol> |
| Alternative flow | The partner is not yet in the list of partners: <ul><li>add the partner</li></ul> The user cancels: <ul><li>The user goes back to the mangement page</li></ul> |

## Edit project

If there's a mistake and the information of a project is not correct.

| Edit project ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> re is a project created by an admin with incorrect information.|
| Postconditions | The changes are directly visible.|
| Actors| Admin |
| Description of steps | <ol><li>Navigate to the management page</li><li>The user clicks on a button 'edit'</li><li>Change the wrong details</li><li>The user clicks on a save edits button</li></ol> |
| Alternative flow | The user cancels: <ul><li>The user goes back to the mangement page</li></ul> |

## Remove project

When a partner changes their mind about one or more projects, an admin should remove the project.

| Remove project ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> There is a project created by an admin that the partner doesn't want to do anymore |
| Postconditions | The deleted project is not visible anymore <br> No more students can be added to the project <br> All students that where added on that project are free again to be set on an other project <br> All coaches set on that project, aren't anymore |
| Actors| Admin |
| Description of steps | <ol><li>Navigate to the management page</li><li>The user clicks on a 'delete project' button</li><li>The user gets a popup "are you sure?"</li><li>The user clicks on "yes"</li></ol> |
| Alternative flow | Cancel removal of project: <ul><li>click the cancel button on the popup</li><li>you return to the previous window, nothing changes</li></ul> |

## Approve new coaches

When a new user wants to join an admin has to approve him.

| Approve new coaches ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> There is at least one person who made a new account. |
| Postconditions | The user who is approved is out of the request list. <br> The user who made the request is a new coach. <br> The user who made the request is visible in the list of users. |
| Actors| Admin |
| Description of steps | <ol><li>the admin clicks on 'Accept'</li></ol> |
| Alternative flow | Deny coach:<ul><li>the admin clicks on 'Reject'</li><li>remove the coach from the tool</li></ul> |

## Change user status

If a coach is promoted to admin, an admin demoted to coach, a coach/admin doesn't want to be active anymore, or there was a simple misclick, the user's status has to change.

| Change user status ||
| --- | --- |
| Preconditions | The current user is logged in as an admin.<br>The other user has the status coach, admin or deactivated. |
| Postconditions | The changes are directly visible for all admins.<br>If the change involved with less access, and the other user is on a page he may not see anymore, he is redirected to the home page.<br>If the user is now not active anymore, he is signed out. |
| Actors| Admin |
| Description of steps | <ul><li>The user clicks on a combobox of another user</li><li>The user clicks on the new role of that other user</li></ul> |

## Remove data of a student

When a student doesn't want to be considered as a candidate for OSOC. They have to be deleted from the database.

| Remove data of a student ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> The student has informed an admin. |
| Postconditions | The student is not visible anymore <br> The student can't be added to any projects <br> The student is removed from all projects <br> All reviews of that student are deleted |
| Actors| Admin |
| Description of steps | <ol><li>Navigate to the student that needs to be removed</li><li>The user clicks on a button 'remove student'</li><li>The user get a popup "are you sure?"</li><li>The user clicks on "yes"</li></ol> |
| Alternative flow | Cancel removal of student data:<ul><li>The user clicks on cancel in the popup</li><li>You return to the previous page, nothing has changed</li></ul> |

## Remove student from project

if the student is no longer required in the project, the student needs to be removed

| Remove student from project ||
| --- | --- |
| Preconditions | The current user is logged in.<br> A student is assigned to a project. |
| Postconditions | The student is removed from the project, this is immediately visible. |
| Actors| Admin |
| Description of steps | <ol><li> navigate to the specific project </li><li> click on the "remove" button next to the student name</li><li> click the confirm button on the popup</li><li> the student disappears from the project</li></ol> |
| Alternative flow | Cancel removal of student from project: <ul><li> click the cancel button on the popup </li><li> you return to the previous window, nothing changes </li> </ul> |

## Definitive decision on student

Admins have to make a definitive decision whether or not students can start working at OSOC.

| Definitive decision on student ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> Coaches have made their suggestions for the student. |
| Postconditions | A decision for the student has been made. |
| Actors| Admin |
| Description of steps | <ol><li> Navigate to the student</li><li> Select a definitive status for the student</li><li> Click confirm</li></ol> |

## View sent emails

View a list of students showing what email has last been sent to them.

| View sent emails ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. |
| Postconditions | A list of students with their last received email is shown. |
| Actors| Admin |
| Description of steps | <ol><li>Click a "view all emails" button</li><li>The list of students is shown with the last email they got. The list is ordered as "most recently sent"</li></ol> |
| Alternative flow | Search a student by name/definitive decision status:<ul><li>only the search matches are shown</li></ul> See all emails send to student:<ul><li>Click on button "see all emails" of a student</li><li>A list of all the emails send to this student is show, orderd by "most recently send"</li></ul> |

## Send email to students

Different types of emails have to be sent in batches to students.

| Send email to students ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. |
| Postconditions | The selected type of email has been sent to the selected students.<br>This is visible on the overview. |
| Actors| Admin |
| Description of steps | <ol><li>navigate to the overview of sent emails</li><li>select the students you want to send an email to</li><li>click the button corresponding to the type of email you want to send</li></ol> |
| Alternative flow | The user cancels: <ul><li>No mails are sent</li><ul> |

## Create new edition

Every year, a new edition of OSOC has to be created with new projects, students and coaches.

| Create new edition ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. |
| Postconditions | A new edition of OSOC has been created, projects, coaches and students of that edition can be added. <br> All info of previous edition is set on read and remove only |
| Actors| Admin |
| Description of steps | <ol><li>Click the "Create new edition" button on the overview window.</li><li>Select the year of the edition</li><li>Confirm the creation of the new edition on the popup.</li></ol> |
| Alternative flow | Cancel creation of new edition:<ul><li>Click cancel on the popup window.</li></ul> |

## Delete edition

An edition might be deleted if it was created by mistake.

| Delete edition ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. |
| Postconditions | The current edition will be deleted. |
| Actors| Admin |
| Description of steps | <ol><li>Click the "Remove this edition" button on the overview window.</li><li>A popup with a warning is shown, confirm the deletion of the edition on the popup.</li></ol> |
| Alternative flow | Cancel deletion of edition:<ul><li>Click cancel on the popup window.</li><li>The screen goes back to the last edition</li></li>The last edition can be edited again</li></ul> |

## Invite new coach

New coaches are invited by admins

| Invite new coach ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> There is a new coach who is not already in the system |
| Postconditions | There is a email send to the new coach |
| Actors| Admin |
| Description of steps | <ol><li>Click "Invite new coach" button</li><li>Enters an email adres of the new coach</li><li>Click confirm</li></ol> |
| Alternative flow | There is no admin in the system: <ul><li>The server starts and print a register URL in the logs</li></ul> |

## Confirm project

Confirm all students who are assigned to that project.

| Confirm project ||
| --- | --- |
| Preconditions | The current user is logged in as an admin. <br> All students assigned to that project are students who will be working on that project <br> There are no conflicts of students for that project|
| Postconditions | All students assgined to that project who aren't a confirmed "yes", gets a confirmed "yes" <br> All students assigned to that project can be send an project info mail |
| Actors| Admin |
| Description of steps | <ol><li>Go to the project page</li><li>Click "Confirm project"</li><li>Confirm again</li></ol> |
| Alternative flow | The user cancels: <ul><li>The user goes back to that project page</li></ul> |
