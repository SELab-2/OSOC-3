# Use Cases User

## Create account

A new user must create an account in order to use the tool.

| Create Account ||
| --- | --- |
| Preconditions | The user has never before created an account and is not known to the tool. <br> The user is invited by an admin  |
| Postconditions | The user has an account, but this is yet to be approved by an admin. <br>An email is sent to all admins to request approval. <br>Admins can see this in the manage users tab. |
| Actors| User |
| Description of steps | <ol><li>fill in name</li><li>fill in your email</li><li>fill in your password</li><li>confirm your password</li><li>click a "create account" button</li><li>a "hold on tight" window is shown</li><li>you receive an email once you've been verified</li></ol>|
| Alternative flow| The person is the first ot ever create an account <ul><li>automatically accept this user as an admin</li><li>the main window is shown instead of the "hold on tight" window</li></ul> Signup via Github/Google instead of filling in username/password: <ul><li>you click the login with Github/Google button</li><li>you give the tool access to your account</li></ul> |

## Login

Every time a recurring user returns, the user must be reauthenticated in order to use the tool.

| Login ||
| --- | --- |
| Preconditions | The user has previously created an account. |
| Postconditions | The user has acces to the tool. |
| Actors| User |
| Description of steps | <ol><li>fill in your name or email.</li><li>fill in your password.</li><li>click the login button.</li><li>the main window is shown, you have access to the tool.</li></ol>|
| Alternative flow| Password incorrect/user unknown: <ul><li>you get an error message saying your username/password combination is incorrect.</li></ul> Not yet verified:<ul><li>you get an error message saying your account has not been verified yet.</li></ul> Login via github instead of filling in username/password: <ul><li>you click the login with github button.</li></ul> |
