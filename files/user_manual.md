# User Manual

In this file, we describe how the selection tool is meant to be used by the end users. This is divided in the different parts of the website.

## Logging in

After you have registered yourself and have been approved by one of the administrators of the selection tool, you can log in to the website.

There are different ways to log in, depending on the way in which you have registered yourself. **Please note: you can only log in through the method you have registered yourself with.**

## Email
1. Fill in your email address and password in the corresponding fields.
2. Click the "Log in" button.

## GitHub
1. Click the "Log in" button with the GitHub logo.

## Google
1. Click the "Log in" button with the Google logo.



## Admins

This section is for admins. It contains all features to manage users. A user is someone who uses the tool (this does not include students).  A user can be coach of one or more editions. He can only see data and work (making suggestions...) on these editions.  A user can be admin of the tool. An admin can see/edit/delete all data from all editions and manage other users. This role is only for fully trusted people. An admin doesn't need to be coach from an edition to participate in the selection process.

The management is split into two pages. The first one is to manage coaches of the currently selected edition. The other is to manage admins. Both pages can be found in the **Users** tab in the navigation bar.

### Coaches

The coaches pages is used to manage all coaches of the current selected edition. The page consists of three main parts.

#### Invite a user

At the top left, you can invite someone via an invite link. You can choose between creating an email to the person or copying the link. The new user can use this link to make an account. Once the person is registered, you can accept (or reject) him at the **Requests** section (see below).

1. Type the email address of the person you want to invite in the input field.
2. Click the **Send invite** button to create an email to the given address OR Use the dropdown of the button and click **Copy invite link** to copy the link. You can choose via which way you provide the new user the invite link.

#### Requests

At the top middle of the page, you find a dropdown labeled **Requests**. When you expand the dropdown, you can see a list of all pending user requests. These are all users who used an invite link to create an account, and haven't been accepted (or declined) yet. 

Note: the list only contains requests from the current selected edition. Each edition has its own requests.

The list can be filtered by name. Each row of the table contains the name and email address of a person. The email contains an icon indicating whether the person registered via email, GitHub or Google. Next to each row there are two buttons to accept or reject the person. When a person is accepted, he will automatically be added as coach to the current edition.

#### Coaches

A the centre of the page, you can find a list of all users who are coach in the current edition. As in the Requests list, each row contains the name and email address of a user. The list can be filtered by name.

Next to the email address, there is a button to remove the user as coach from the currently selected edition. Once clicked, you get two choices:

- **Remove from all editions**: The user will be removed as coach from all editions. If the user is not a coach, he won't be able to see any data from any edition anymore
- **Remove from {Edition name}**: The user will be removed as coach from the current selected edition. He will still be able to see data from any other edition wherefrom he is coach.

At the top right of the list, there is a button to add a user as coach to the selected edition. This can be used if a user of a previous edition needs to be a coach in the current edition. You can only add existing users via this button. Once clicked, you see a prompt to search for a user's name. After typing the name of the user, a list of users whose name contains the typed text will be shown. You can select the desired user, check if the email and register-method are correct and add him as coach to the current edition. A user who is added as coach will be able to see all data of the current edition and participate in the selection process.

### Admins

This page consists of a list of all users who are admin. An admin can see all editions and change all data (including deleting a whole edition). Each row in the list contains the name and email (including register-method) of every admin. The list can be filtered by name via the input field.

Next to the email address, there is a button to remove a user as admin. Once clicked, you get two choices:

- **Remove admin**: Remove the given user as admin. He will stay coach for editions whereto he was assigned
- **Remove as admin and coach**: Remove the given user as admin and remove him as coach from every edition. The user won't be able to see any data from any edition.

At the top right of the list, there is a button to add a user as admin.  Once clicked, you see a prompt to search for a user's name. After typing  the name of the user, a list of users whose names contain the typed text will be shown. You can select the desired user, check if the email and register-method are correct and add him as admin.

**Warning**: A user who is added as admin will be able to edit and delete all data. He will be able to add and remove other admins.
