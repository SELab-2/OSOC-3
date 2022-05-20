# User Manual

In this file, we describe how the selection tool is meant to be used by the end users. This is divided in the different parts of the website.


## Logging in

After you have registered yourself and have been approved by one of the administrators of the selection tool, you can log in to the website.

There are different ways to log in, depending on the way in which you have registered yourself. **Please note: you can only log in through the method you have registered yourself with.**

### Email

1. Fill in your email address and password in the corresponding fields.
2. Click the "Log in" button.

### GitHub

1. Click the "Log in" button with the GitHub logo.


## Logging out

To log out, click on the **Log Out** button on the top right of the page.


## Managing Users (Admin-only)

This section is for admins. It contains all features to manage users. A user is someone who uses the tool (this does not include students). A user can be coach of one or more editions. He can only see data and work (making suggestions...) on these editions. A user can be admin of the tool. An admin can see/edit/delete all data from all editions and manage other users. This role is only for fully trusted people. An admin doesn't need to be coach in an edition to participate in the selection process.

The management is split into two pages. The first one is to manage coaches of the currently selected edition. The other is to manage admins (these are not linked to a specific edition). Both pages can be found in the **Users** tab in the navigation bar.

### Coaches

The coaches pages is used to manage all coaches of the current selected edition. The page consists of three main parts.

#### Invite a user

At the top left, you can invite someone via an invite link. You can choose between creating an email to the person or copying the link. The new user can use this link to make an account. Once the person is registered, you can accept (or reject) him at the **Requests** section (see below).

1. Type the email address of the person you want to invite in the input field.
2. Click the **Send invite** button to create an email to the given address OR Use the dropdown of the button and click **Copy invite link** to copy the link. You can choose via which way you provide the new user the invite link.

#### Requests

At the top middle of the page, you find a dropdown labeled **Requests**. When you expand the dropdown, you can see a list of all pending user requests. These are all users who used an invite link to create an account, and haven't been accepted (or declined) yet.

**Note:** the list only contains requests from the current selected edition. Each edition has its own requests.

The list can be filtered by name. Each row of the table contains the name and email address of a person. The email contains an icon indicating whether the person registered via email or GitHub. Next to each row there are two buttons to accept or reject the person. When a person is accepted, he will automatically be added as coach to the current edition.

#### Coaches

At the centre of the page, you can find a list of all users who are coach in the current edition. As in the Requests list, each row contains the name and email address of a user. The list can be filtered by name.

Next to the email address, there is a button to remove the user as coach from the currently selected edition. Once clicked, you get two choices:

- **Remove from all editions**: The user will be removed as coach from all editions. If the user is not an admin, he won't be able to see any data from any edition anymore
- **Remove from {Edition name}**: The user will be removed as coach from the current selected edition. He will still be able to see data from all other editions where he is coach.

At the top right of the list, there is a button to add a user as coach to the selected edition. This can be used if a user of a previous edition needs to be a coach in the current edition. You can only add existing users via this button. Once clicked, you see a prompt to search for a user's name. After typing the name of the user, a list of users whose name contains the typed text will be shown. You can select the desired user, check if the email and register-method are correct and add him as coach to the current edition. A user who is added as coach will be able to see all data of the current edition and participate in the selection process.

### Admins

This page consists of a list of all users who are admin. An admin can see all editions and change all data (including deleting a whole edition). Each row in the list contains the name and email (including register-method) of every admin. The list can be filtered by name via the input field.

Next to the email address, there is a button to remove a user as admin. Once clicked, you get two choices:

- **Remove admin**: Remove the given user as admin. He will stay coach for editions where he was assigned to.
- **Remove as admin and coach**: Remove the given user as admin and remove him as coach from every edition. The user won't be able to see any data from any edition.

At the top right of the list, there is a button to add a user as admin. Once clicked, you see a prompt to search for a user's name. After typing the name of the user, a list of users whose names contain the typed text will be shown. You can select the desired user, check if the email and register-method are correct and add him as admin.

**Warning**: A user who is added as admin will be able to edit and delete all data. He will be able to add and remove other admins.


## Editions

This section contains all actions related to managing your editions.

### Viewing a list of available editions

In the navbar, you should see an **Editions** button. When clicked, this button brings you to "/editions", which we'll call the "Editions Page". Admins can see _all_ editions, coaches can only see the editions they're coach of.

This page lists all editions, and contains buttons for:

- [Creating new editions](#creating-a-new-edition-admin-only)
- [Deleting editions](#deleting-an-edition-admin-only)

### Creating a new edition (Admin-only)

In order to create new editions, head over to the Editions Page (see [Viewing a list of available editions](#viewing-a-list-of-available-editions)). In the top-right of the page, you should see a "+ Create Edition"-button.

- Click the "+ Create Edition"-button
- Fill in the fields in the form presented to you (only alphanumerical characters, dashes and underscores are allowed as the name for an edition)
- Click the "Submit"-button

You've now created a new edition to which you can add coaches, projects, and students.

### Deleting an edition (Admin-only)

In order to delete editions, head over to the Editions Page (see [Viewing a list of available editions](#viewing-a-list-of-available-editions)). Every entry in the list will have a "Delete Edition" on the right.

- Click the "Delete Edition"-button of the edition you want to delete
- Follow the on-screen instructions

**Warning**: Deleting an edition is a <u>**very dangerous operation**</u> and <u>**can not be undone**</u>. As none of the linked data can be viewed without an edition, this means that deleting an edition _also_ deletes:

- All projects linked to this edition
- All students linked to this edition

### Changing the current edition

We have made a component to quickly go to a page from a previous edition. In the navbar, there's a dropdown of which the label is the name of the currently selected edition.

_**Note**: This dropdown is hidden if you cannot see any editions, as it would be empty. If you are an admin, create a new edition. If you are a coach, wait for an admin to add you to an edition._

- Click the dropdown in the navbar to open it
- In the dropdown, click on the edition you'd like to switch to

You have now set another edition as your "current edition". This means that navigating through the navbar will show results for that specific edition.

### Making an edition read-only

Old editions can be made read-and-delete-only by clicking on the 'editable' label on the Editions page. This can be undone by clicking the label again.

## Projects

This section contains all actions related to managing projects.

### Viewing the grid of all projects

You can navigate to the "Projects page" by clicking the **Projects** button. Here you can see all the projects that belong to the current edition. In the short overview of a project you can see the partners, coaches and the number of students needed for this project.

You can also filter on project name and on the projects where you are a coach of. To filter on name enter a name in the search field and press enter or click the **Search** button. To filter on your own projects toggle the **Only own projects** switch.

When there are a lot of projects, the **Load more projects** button located at the bottom of the search results will get you more projects.

### Deleting a project (Admin-only)

To delete a project click the **trash** button located on the top right of a project card or next to the project name in the detailed project page. A pop up will appear to confirm your decision. Press **Delete** again to delete the project or cancel the delete operation.

### Conflicts

As coaches can suggest a student for multiple project, but a student can only work on one, conflicts can happen. To definitively confirm a student for a project, all conflicts involving that student will first need to be resolved.

To see an overview of all current conflicts, click on the green button at the top right of the "Projects page".


## Detailed view of a project

To get more in depth with a project click the title of the project. This will take you to the "Project page" of that specific project.

### Editing a project (Admin-only)

To edit a project, click on the pencil icon next to the project's name, now you can change all the attributes of the project.

### Suggesting a student for a project

To suggest a student for a project, drag the student from the list on the lefthand side to the skill you want to suggest the student for. A popup will appear asking for a motivation for the suggestion.

### Confirming a student for a project (Admin-only)

When it has been definitively decided that the student will work on this project, an admin can confirm the student for this project. This will not be possible if the student is currently also assigned to another project (=conflict).

When a student is confirmed, they cannot be added to another project anymore. 

### Removing a student from a project (Admin-only)

To remove a student from a project, click on the red trash icon on the top right of the student's card on the "Project page".

### Adding a skill to a project (Admin-only)

A skill contains a number of slots where students can be placed in to fulfill that skill for that project.

To add a new skill requirement to a project, click on the **Add new skill** button on the botton of the "Project page".

### Removing a skill from a project (Admin-only)

To remove a skill from a project, click on the red trash icon on the top right of the card of the skill on the "Project page".


## State history of a student (Admin-only)

A student can be at different stages throughout the selection process, at some stages, an email needs to be sent to the student to inform them of their state change (e.g. the student has been accepted/denied). 

To view a student's state history (i.e. all states the student has ever been in), navigate to the page with the student's details, and click on the "See State History" button.

The state history will be shown in a table, with the most recent state at the top.


## Overview of states (Admin-only)

To see the overview of states, click on "Students" in the navbar on top of the page, and then click on "State Overview"

The overview of the states is a table of all students of an edition, together with the most recent state that has been assigned to them.

This table needs to be manually maintained (i.e. when a new decision has been made about a student, someone has to update this list).

### Searching and Filtering

The overview table allows you to search for a particular student or filter based on one or more states.

To search for a student: type (the beginning of) a student's name in the search bar.

To filter based on email states: select one or more states from the list.

These two things (searching and filtering) can also be combined.

### Updating the state overview

When a new state is assigned to one or more students, the list needs to be updated. 

This can be done by selecting these students in the table, clicking on the "Set state of selected students", and choosing the new state from the dropdown.


## Students

### Viewing a student

To view the details of a student, click on the student's name in the list on the lefthand side.

### Making a suggestion for a student

Every coach can make a suggestion for a student, where they express whether they find the student interesting to use in their project or not.
To do this, scroll down on the student's detail page and click on the appropriate suggestion you want to make for that student. A popup will appear where you can enter an argumentation for this decision.

### Making a definitive decision for a student (Admin-only)

An admin can make a definitive decision for a student, by taking into account the multiple suggestions from the coaches. This is where an admin decides if a student is accepted into the programme or not.
To make a definitive decision, scroll down on the student's detail page and click on the **Confirm** button. A popup will appear where you can select the decision you want to make.

### Removing a student (Admin-only)

To remove a student, click on the red trash icon on the bottom of the student's page.

### Searching and filtering in the student's list

The student's list on the lefthand side can be searched through (by typing the name of the student in the search bar) and can also be filtered by multiple attributes:

- Roles: Only show students who have one of the selected roles
- Only alumni: Only show students who are alumni
- Students you've suggested for: Only show students for which you made a suggestion
- Only student coach volunteer: Only show students who indicated that they want to be a student coach

These filters can also be reset by clicking the red **Reset filters** button at the top of the student's list. 

