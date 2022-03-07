# Use Cases Coach

## Review student

In this situation a coach will make a recommendation about a student based onto the students skills and motivation.

| Review student ||
| --- | --- |
| Preconditions | The current user (a coach) has created an account and is approved by an admin. <br> The student has been approved by an OKBE employee. (can legally work and is in timezone) |
| Postconditions | The recommendation made by the coach is immediately visible to other users.|
| Actors| Coach |
| Description of steps | <ol><li>Navigate to student</li><li>First click on the student you want to review then you will be shown the information there is about that student.</li><li>You can see the reviews of other coaches</li><li>Click on a button make review</li><li>You can choose between “yes”, “maybe” or “no”. It is possible to argument why you made this decision so others can understand it.</li></ol>|
| Alternative flow| The coach cancels the review: <ul> <li>You return to the user info, nothing changes</li> </ul> |

## Add student to project

In this situation a coach will add a student to a specific project they seem fit for.

| Add student to project ||
| --- | --- |
| Preconditions | The current user (a coach) has created an account and is approved by an admin |
| Postconditions | The project choice made by the coach is immediately visible to other users. <br> Admins can confirm the assignment of the student and can send an email to the student and later send the contract. |
| Actors| Coach |
| Description of steps | <ol> <li> You can search for a specific project or go to the project overview. </li> <li> You can search a student based on search criteria </li> <li> Push a button "Add to project".</li> <li>Choose the role this student will have in the team and argument why this student is a good fit for this project.</li> <li>Make sure there are no conflicts between students and projects.</li> </ol> |

## Change or remove review

In this situation a coach wants to change its recommendation they made about a student (typo or wrong student).

| Change or remove review ||
| --- | --- |
| Preconditions | The current user (a coach) has created an account and is approved by an admin. <br> The student already received a review from the coach. |
| Postconditions | The changed recommendation made by the coach is immediately visible to other users.|
| Actors| Coach |
| Description of steps | <ol> <li> Navigate to the student you want to change the review for.</li> <li>Click the edit recommendation button. </li> <li>There might be real time reviews of other people than you can use to help make your own decisions. </li> <li>After you looked at the student for the second time it’s time to make your new recommendation. You can again choose between “yes”, “maybe” or “no”. It is possible to argument why you made this new decision so others can understand it.</li> </ol> |
| Alternative flow| The coach cancels the change of the review: <ul> <li>You return to the user info, nothing changes.</li> </ul> The coach clicks on delete review: <ul><li>The users clicks on "delete review" and confirms it.</li><li>The review is not visible anymore</li></ul> |

## Search students

In this situation a coach tries to find specific students based on skills or other filters.

| Search students ||
| --- | --- |
| Preconditions | The current user (a coach) has created an account and is approved by an admin.|
| Postconditions | The found students can be reviewed or added to projects.|
| Actors| Coach |
| Description of steps | <ol> <li>First of all you may want to clear any previous filters set.</li> <li>You can search based on name, alumni, student coach, skills/roles, practical information, availability or based on reviews of others. </li> <li>Click on a student.</li> </ol> |

## Remove student from project

If the student is no longer required in the project, the student needs to be removed

| Remove student from project ||
| --- | --- |
| Preconditions | The current user is logged in. <br> A student is assigned to a project. |
| Postconditions | The student is removed from the project, this is immediately visible. |
| Actors| Coach |
| Description of steps | <ol><li>navigate to the specific project</li><li>click on the "remove" button next to the student name</li><li>click the confirm button on the popup</li><li>the student disappears from the project</li></ol> |
| Alternative flow | Cancel removal of student from project:<ul><li>click the cancel button on the popup</li><li>you return to the previous window, nothing changes</li></ul> |

## See all conflicts

A quick look to see all students who are assigned to 2 or more projects

| See all conflicts ||
| --- | --- |
| Preconditions | The user is logged in. |
| Postconditions | See all students who are in 2 or more projects and what projects they are in <br> They can be deleted from a project |
| Actors| Coach |
| Description of steps | <ol><li>Go to the project overview</li><li>Click a "see all conflicts button"</li></ol> |
| Alternative flow | No conflicts: <ul><li>A messaged is show "There are no conflicts at this moment"</li></ul> |
