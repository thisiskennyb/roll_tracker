## Sign-Up
- When a user signs up a POST request is made to `localhost:8000/api/v1/accounts/register/signup` with the following fields:
```json
{
	"username": "maintest1",
	"password": "fishings1F!",
	"confirm_password": "fishings1F!",
	"email": "kennethbonnette@yahoo.com"

}
```
- When the POST request is made an email is sent to the user that contains a link. The user will remain inactive until the link is clicked. Clicking the link will direct the user to a react route that was made as their account is activated

## Sign-In
- For a user to sign in a POST request is made to `localhost:8000/api/v1/accounts/register/get-token` with the following fields:
```json
{
	"username": "maintest1",
	"password": "fishings1F!"
}
```
- A response with a token will be sent like the one below:
```json
{

"token": "390e8ee5a89577bbd0ae6039073242e2a2ea4ac1"

}
```


## Reset/Forgot Password
- To reset a forgotten password Django has created a built-in method to accomplish this that provide two different endpoints

- A POST request to `localhost:8000/password_reset/` must be made first with the users email address 
```json
{
	"email": "kennethbonnette@yahoo.com"
}
```
- An email will be sent to the specified email address that contains a link. The last part of the link is the reset_password_token that is needed for the next post request

ex. link:`http://localhost:5173/reset-password63baecd2474b730f7e55e1` reset_password_token:`63baecd2474b730f7e55e1` 

- Lastly make a POST request to `localhost:8000/password_reset/confirm/` with the reset_password_token and new password
```json
{
	"password":"Better55!",
	"token": "63baecd2474b730f7e55e1"
}
```


## Change Password
- To change a password a POST request must be made to `localhost:8000/api/v1/accounts/register/change_password/` with the following fields:
```json
{
	"old_password": "pk",
	"new_password": "jimboB69!"
}
```

