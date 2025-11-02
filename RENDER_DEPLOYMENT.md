# Render Deployment Guide for Prompt.ly

This guide will help you deploy Prompt.ly to Render, including the PostgreSQL database, backend API, and frontend.

## Prerequisites

1. A [Render](https://render.com) account (free tier works)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Your Auth0 configuration ready
4. Your OpenAI API key

## Step-by-Step Deployment

### Option 1: Automated Deployment with render.yaml (Recommended)

This is the easiest method - Render will automatically detect and configure everything from the `render.yaml` file.

1. **Push your code to Git**

   ```bash
   git add .
   git commit -m "Configure for Render deployment"
   git push origin main
   ```

2. **Create a New Blueprint on Render**

   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will automatically detect `render.yaml` and configure all services

3. **Set Environment Variables**
   Render will prompt you to set these environment variables. You'll need:

   **For Backend:**

   - `OPENAI_API_KEY` - Your OpenAI API key
   - `AUTH0_DOMAIN` - Your Auth0 domain (e.g., `dev-pdecvsnuz3rv2bef.us.auth0.com`)
   - `AUTH0_API_AUDIENCE` - Your Auth0 API audience (e.g., `https://promptly-api`)
   - `FRONTEND_URL` - Your frontend URL (e.g., `https://promptly-frontend.onrender.com`)
   - `SECRET_KEY` - Will be auto-generated, but you can set a custom one

   **For Frontend:**

   - `REACT_APP_API_URL` - Your backend URL (e.g., `https://promptly-backend.onrender.com/api`)

4. **Deploy**

   - Click "Apply" to create all services
   - Wait for deployment to complete (5-10 minutes for first deploy)

5. **Update Auth0 Settings**
   - Once deployed, update your Auth0 application settings:
     - **Allowed Callback URLs**: Add your frontend URL + callback path (e.g., `https://promptly-frontend.onrender.com/callback`)
     - **Allowed Logout URLs**: Add your frontend URL (e.g., `https://promptly-frontend.onrender.com`)
     - **Allowed Web Origins**: Add your frontend URL (e.g., `https://promptly-frontend.onrender.com`)
     - **Allowed Origins (CORS)**: Add your frontend URL (e.g., `https://promptly-frontend.onrender.com`)
   - Update your Auth0 API settings:
     - **Allowed Origins**: Add your backend URL (e.g., `https://promptly-backend.onrender.com`)

### Option 2: Manual Service Creation

If you prefer to set up services manually:

#### 1. Create PostgreSQL Database

1. Go to Render Dashboard → "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `promptly-database`
   - **Database**: `promptly`
   - **User**: `promptly_user`
   - **Plan**: Starter (Free tier available)
3. Click "Create Database"
4. **Save the Internal Database URL** - you'll need it for the backend

#### 2. Create Backend Service

1. Go to Render Dashboard → "New +" → "Web Service"
2. Connect your Git repository
3. Configure:

   - **Name**: `promptly-backend`
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: Starter (Free tier available)

4. **Set Environment Variables:**

   - `DATABASE_URL` - Copy from your PostgreSQL database (Internal Database URL)
   - `ENVIRONMENT` - `production`
   - `DEBUG` - `false`
   - `PORT` - `10000` (Render sets this automatically, but good to have)
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `AUTH0_DOMAIN` - Your Auth0 domain
   - `AUTH0_API_AUDIENCE` - Your Auth0 API audience
   - `AUTH0_ALGORITHMS` - `RS256`
   - `FRONTEND_URL` - Your frontend URL (set after frontend is deployed)
   - `SECRET_KEY` - Generate a secure random string

5. Click "Create Web Service"

#### 3. Create Frontend Service

1. Go to Render Dashboard → "New +" → "Static Site"
2. Connect your Git repository
3. Configure:

   - **Name**: `promptly-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Plan**: Free

4. **Set Environment Variables:**

   - `REACT_APP_API_URL` - Your backend URL (e.g., `https://promptly-backend.onrender.com/api`)

5. Click "Create Static Site"

#### 4. Update Backend FRONTEND_URL

After frontend is deployed:

1. Go to your backend service on Render
2. Navigate to "Environment"
3. Update `FRONTEND_URL` to your frontend URL (e.g., `https://promptly-frontend.onrender.com`)
4. Click "Save Changes" - this will trigger a redeploy

## Post-Deployment Configuration

### 1. Update Auth0 Settings

After deployment, update your Auth0 dashboard:

1. **Application Settings** (for your SPA):

   - **Allowed Callback URLs**:
     ```
     http://localhost:3000/callback,https://promptly-frontend.onrender.com/callback
     ```
   - **Allowed Logout URLs**:
     ```
     http://localhost:3000,https://promptly-frontend.onrender.com
     ```
   - **Allowed Web Origins**:
     ```
     http://localhost:3000,https://promptly-frontend.onrender.com
     ```
   - **Allowed Origins (CORS)**:
     ```
     http://localhost:3000,https://promptly-frontend.onrender.com
     ```

2. **API Settings**:
   - **Allowed Origins**:
     ```
     http://localhost:5001,https://promptly-backend.onrender.com
     ```

### 2. Test Your Deployment

1. Visit your frontend URL
2. Try logging in with Auth0
3. Create a conversation
4. Send a message and verify AI responses work

## Continuous Deployment

Render automatically deploys when you push to your main branch. To deploy changes:

1. Make your changes locally
2. Commit and push:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```
3. Render will automatically detect the push and start a new deployment
4. Monitor the deployment in the Render dashboard

## Troubleshooting

### Backend Issues

**Database Connection Errors:**

- Verify `DATABASE_URL` is set correctly in backend environment variables
- Check that the database service is running
- Ensure you're using the "Internal Database URL" (not external)

**API Not Responding:**

- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure `FRONTEND_URL` matches your actual frontend URL

**CORS Errors:**

- Verify `FRONTEND_URL` in backend matches your actual frontend URL
- Check Auth0 CORS settings

### Frontend Issues

**Cannot Connect to Backend:**

- Verify `REACT_APP_API_URL` is set correctly
- Check that backend URL is accessible (try visiting `/api/health`)
- Ensure backend CORS settings allow your frontend URL

**Auth0 Login Issues:**

- Check Auth0 application settings (callback URLs, logout URLs, etc.)
- Verify Auth0 domain and audience match your backend configuration
- Check browser console for errors

### Database Issues

**Tables Not Created:**

- Check backend logs during startup
- The database tables are created automatically on first run
- You can manually trigger initialization by restarting the backend service

## Environment Variables Summary

### Backend (`promptly-backend`)

| Variable             | Description                  | Example                                  |
| -------------------- | ---------------------------- | ---------------------------------------- |
| `DATABASE_URL`       | PostgreSQL connection string | Auto-set by Render                       |
| `ENVIRONMENT`        | Environment mode             | `production`                             |
| `DEBUG`              | Debug mode                   | `false`                                  |
| `PORT`               | Server port                  | `10000` (auto-set)                       |
| `OPENAI_API_KEY`     | OpenAI API key               | `sk-proj-...`                            |
| `AUTH0_DOMAIN`       | Auth0 domain                 | `dev-xxx.us.auth0.com`                   |
| `AUTH0_API_AUDIENCE` | Auth0 API audience           | `https://promptly-api`                   |
| `AUTH0_ALGORITHMS`   | JWT algorithm                | `RS256`                                  |
| `FRONTEND_URL`       | Frontend URL                 | `https://promptly-frontend.onrender.com` |
| `SECRET_KEY`         | Flask secret key             | Auto-generated                           |

### Frontend (`promptly-frontend`)

| Variable            | Description     | Example                                     |
| ------------------- | --------------- | ------------------------------------------- |
| `REACT_APP_API_URL` | Backend API URL | `https://promptly-backend.onrender.com/api` |

## Free Tier Limitations

- **Database**: 90 days free, then $7/month
- **Web Services**: Spins down after 15 minutes of inactivity (wakes up on first request)
- **Static Sites**: Always on, unlimited bandwidth

## Upgrading from Free Tier

If you need better performance:

- Upgrade database to paid plan ($7/month) for persistent storage
- Upgrade web service to paid plan ($7/month) for always-on availability

## Support

If you encounter issues:

1. Check Render logs in the dashboard
2. Verify all environment variables are set correctly
3. Check Auth0 configuration matches your deployed URLs
4. Test API endpoints directly (e.g., `https://your-backend.onrender.com/api/health`)
