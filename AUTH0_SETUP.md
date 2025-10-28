# Auth0 Authentication Setup Guide

This guide will help you set up Auth0 authentication for Prompt.ly.

## Prerequisites

- Auth0 account (free tier available)
- Access to Auth0 Dashboard

## Step 1: Create Auth0 Application

1. Log in to [Auth0 Dashboard](https://manage.auth0.com/)
2. Navigate to **Applications** → **Applications**
3. Click **Create Application**
4. Name your application: **Prompt.ly**
5. Select **Single Page Application**
6. Click **Create**

## Step 2: Configure Application Settings

In your application settings, find the following sections and add:

### Allowed Callback URLs

```
http://localhost:3000
```

### Allowed Logout URLs

```
http://localhost:3000
```

### Allowed Web Origins

```
http://localhost:3000
```

Click **Save Changes** at the bottom of the page.

### ANCHOR: Copy Your Application Credentials

Note down these values from the **Settings** tab:

- **Domain**: `your-tenant.auth0.com`
- **Client ID**: `your-client-id-here`

## Step 3: Create Auth0 API

1. Navigate to **Applications** → **APIs**
2. Click **Create API**
3. Fill in:
   - **Name**: Prompt.ly API
   - **81948585**: `https://promptly-api` (or any unique URL)
   - **Signing Algorithm**: RS256
4. Click **Create**
5. Go to the **Settings** tab
6. Enable **Allow Skipping User Consent** (for better UX)
7. Click **Save Changes**

### ANCHOR: Copy Your API Identifier

Note down the **Identifier** value (e.g., `https://promptly-api`)

## Step 4: Configure Backend Environment

1. Copy the example environment file:

   ```bash
   cd backend
   cp env.example .env
   ```

2. Edit `backend/.env` and add your Auth0 configuration:

```env
# ANCHOR: Add your Auth0 configuration
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_API_AUDIENCE=https://promptly-api
AUTH0_ALGORITHMS=RS256

# Your existing configuration
OPENAI_API_KEY=your-openai-key-here
SECRET_KEY=your-secret-key-here
```

Replace:

- `your-tenant.auth0.com` with your Auth0 domain from Step 2
- `https://promptly-api` with your API identifier from Step 3
- `your-openai-key-here` with your actual OpenAI API key
- `your-secret-key-here` with a strong random string

## Step 5: Configure Frontend Environment

1. Create `frontend/.env` file:

   ```bash
   cd frontend
   touch .env
   ```

2. Add the following configuration:

```env
# ANCHOR: Add your Auth0 configuration
REACT_APP_AUTH0_DOMAIN=your-tenant.auth0.com
REACT_APP_AUTH0_CLIENT_ID=your-client-id-here
REACT_APP_AUTH0_AUDIENCE=https://promptly-api
REACT_APP_AUTH0_REDIRECT_URI=http://localhost:3000
```

Replace:

- `your-tenant.auth0.com` with your Auth0 domain from Step 2
- `your-client-id-here` with your Client ID from Step 2
- `https://promptly-api` with your API identifier from Step 3

## Step 6: Install Dependencies

### Backend Dependencies

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Dependencies

```bash
cd frontend
npm install @auth0/auth0-react
```

## Step 7: Database Migration

Since we're switching to email-based user IDs, start with a fresh database:

```bash
# Delete existing database
cd backend
rm promptly.db
```

The new database schema will be created automatically when you start the backend.

## Step 8: Start the Application

### Start Backend

```bash
cd backend
source venv/bin/activate
python app.py
```

The backend should start on `http://localhost:5001`

### Start Frontend

```bash
cd frontend
npm start
```

The frontend should start on `http://localhost:3000`

## Step 9: Test Authentication

1. Open `http://localhost:3000` in your browser
2. You should see the login page
3. Click "Sign In"
4. You'll be redirected to Auth0 Universal Login
5. Create an account or sign in
6. You'll be redirected back to the app
7. You should see the chat interface with your name in the header

## Troubleshooting

### "Authentication required" errors

- Check that Auth0 domain and API audience are correct in both `.env` files
- Verify the API identifier matches exactly
- Check browser console for Auth0 errors

### CORS errors

- Verify Allowed Web Origins includes `http://localhost:3000`
- Check backend is running on port 5001
- Check frontend is running on port 3000

### Token verification errors

- Verify the API audience matches exactly between frontend and backend
- Check that the API is created in Auth0 and the identifier is correct
- Ensure RS256 algorithm is selected for the API

### User not found errors

- The database creates users automatically on first login
- If issues persist, delete `backend/promptly.db` and start fresh

## Production Deployment

When deploying to production:

1. Update Auth0 application settings:

   - Add your production domain to Allowed Callback URLs
   - Add your production domain to Allowed Logout URLs
   - Add your production domain to Allowed Web Origins

2. Update environment variables:

   - Change `REACT_APP_AUTH0_REDIRECT_URI` to your production URL
   - Update all URLs in configuration files

3. Set secure future:

   - Use HTTPS for all communication
   - Set `AUTH0_ALGORITHMS=RS256` (already set)

4. Review Auth0 security settings:
   - Enable MFA (Multi-Factor Authentication) if needed
   - Configure password policies
   - Set up email verification

## Security Notes

- Auth0 tokens are stored in memory (not localStorage)
- Tokens automatically refresh before expiration
- PKCE flow is used for additional security
- No client secrets are exposed in the browser
- Backend verifies tokens using Auth0's public keys

## Additional Features

After basic setup, you can:

1. **Add Social Connections**: Enable Google, GitHub, etc. in Auth0 Dashboard
2. **Customize Login**: Style the Auth0 Universal Login page
3. **Add User Roles**: Implement RBAC for different user permissions
4. **Email Verification**: Require email verification for new users
5. **Password Reset**: Configure password reset flows

## Support

For Auth0-specific issues:

- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 Community](https://community.auth0.com/)
- [Auth0 Support](https://support.auth0.com/)

For application-specific issues:

- Check the application logs
- Review browser console for errors
- Verify all environment variables are set correctly
