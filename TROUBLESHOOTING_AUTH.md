# Troubleshooting Authentication Issues

## Current Issue: "Authentication failed" Error

If you're getting "Authentication failed" errors after setting up Auth0, follow these steps:

### Step 1: Verify the Auth0 Action is Set Up Correctly

1. Go to **Actions** → **Flows** → **Login** in Auth0 Dashboard
2. Check that your "Add Email to Token" action appears in the flow diagram
3. Make sure it's between "Login" and "Complete"
4. Verify it's deployed (not in draft mode)

### Step 2: Check the Action Code

Make sure your action code is:

```javascript
exports.onExecutePostLogin = async (event, api) => {
  if (!event.user.email) {
    console.log("WARNING: User does not have an email address");
    return;
  }

  if (event.authorization) {
    api.idToken.setCustomClaim("email", event.user.email);
    api.accessToken.setCustomClaim("email", event.user.email);
    console.log("Email added to tokens:", event.user.email);
  } else {
    console.log("No authorization context - tokens not modified");
  }
};
```

### Step 3: **IMPORTANT - Get a Fresh Token**

**You MUST log out and log back in after creating the action!**

Old tokens won't have the email claim - you need a fresh token:

1. **Log out** of your application completely
2. Clear your browser cache/localStorage if needed
3. **Log back in** - this will generate a NEW token with email included

### Step 4: Check Backend Logs

After logging back in, try sending a message and check your backend terminal. You should see:

```
DEBUG: Auth0 token claims: ['sub', 'aud', 'iat', 'exp', 'email', ...]
DEBUG: Looking for email in token. Sub: auth0|xxxxx
DEBUG: Email found in token: True
DEBUG: Email value: user@example...
```

If you see:

```
ERROR: Invalid or missing email in token.
ERROR: Available claims in token: ['sub', 'aud', 'iat', 'exp']
```

This means the action isn't working or you're using an old token.

### Step 5: Verify Auth0 Configuration

Check these settings:

1. **Frontend (`frontend/src/index.js`)**:

   - Make sure `audience` is set: `audience: process.env.REACT_APP_AUTH0_AUDIENCE`
   - Make sure `scope` includes email: `scope: "openid profile email"`

2. **Backend (`backend/.env`)**:

   - `AUTH0_DOMAIN` matches your Auth0 tenant domain
   - `AUTH0_API_AUDIENCE` matches your API identifier exactly (e.g., `https://promptly-api`)
   - `AUTH0_ALGORITHMS=RS256`

3. **Auth0 Dashboard**:
   - Your API exists and has the correct identifier
   - Your Application has the API authorized
   - The action is in the Login flow

### Step 6: Test the Token Manually

1. After logging in, open browser console
2. In your React app, you can check the token (temporarily):
   ```javascript
   const { getAccessTokenSilently } = useAuth0();
   getAccessTokenSilently().then((token) => {
     // Decode token at jwt.io or use a library
     console.log("Token:", token);
   });
   ```
3. Go to [jwt.io](https://jwt.io) and paste the token
4. Check the "Payload" section - does it have an `email` field?

### Common Issues and Fixes

#### Issue: Action not in flow

- **Fix**: Go to Actions → Flows → Login, click "+", add your action, click "Apply"

#### Issue: Action not deployed

- **Fix**: Open the action, click "Deploy" button

#### Issue: Still using old token

- **Fix**: Log out completely, clear browser data, log back in

#### Issue: Wrong audience

- **Fix**: Check that `REACT_APP_AUTH0_AUDIENCE` in frontend matches `AUTH0_API_AUDIENCE` in backend exactly

#### Issue: Action not running

- **Fix**: Check Auth0 logs (Monitoring → Logs) to see if action executed
- Check for errors in the action execution logs

### Quick Debug Checklist

- [ ] Action is created and deployed
- [ ] Action is added to Login flow
- [ ] Clicked "Apply" on the Login flow
- [ ] Logged out of application
- [ ] Logged back in (got fresh token)
- [ ] Backend logs show email in token
- [ ] Frontend has correct `audience` and `scope` settings
- [ ] Backend `.env` has correct `AUTH0_API_AUDIENCE`

If all these are checked and it still doesn't work, check the backend terminal output for the detailed error messages.
