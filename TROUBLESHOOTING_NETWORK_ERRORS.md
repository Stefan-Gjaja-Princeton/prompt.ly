# Troubleshooting Network Errors on Render Deployment

If your friends are experiencing network errors when trying to send/receive messages, check these common issues:

## Quick Checklist

### 1. Frontend Environment Variable

**Check:** Is `REACT_APP_API_URL` set in your frontend service on Render?

1. Go to Render Dashboard → Your Frontend Service
2. Navigate to "Environment" tab
3. Verify `REACT_APP_API_URL` is set to: `https://your-backend-url.onrender.com/api`
   - Replace `your-backend-url` with your actual backend URL
   - **Important:** Include `/api` at the end!
   - Example: `https://promptly-backend-dcbp.onrender.com/api`

### 2. Backend Environment Variable

**Check:** Is `FRONTEND_URL` set in your backend service on Render?

1. Go to Render Dashboard → Your Backend Service
2. Navigate to "Environment" tab
3. Verify `FRONTEND_URL` is set to your frontend URL:
   - Example: `https://promptly-frontend-dcbp.onrender.com`
   - **Important:** No trailing slash!

### 3. Verify Backend is Running

**Check:** Can you access the backend health endpoint?

1. Open: `https://your-backend-url.onrender.com/api/health`
2. Should see: `{"status":"healthy"}`
3. If you get an error or timeout, the backend is not running

### 4. Check Browser Console

**Check:** What errors appear in the browser console?

1. Open your deployed site
2. Press `F12` (or right-click → Inspect)
3. Go to "Console" tab
4. Look for errors starting with:
   - `Network Error`
   - `CORS policy`
   - `Failed to fetch`
   - `401 Unauthorized`

## Common Issues and Fixes

### Issue: "Network Error" or "Failed to fetch"

**Cause:** Frontend can't reach backend or CORS is blocking

**Fix:**

1. Verify `REACT_APP_API_URL` is set correctly (see checklist #1)
2. Verify `FRONTEND_URL` is set correctly (see checklist #2)
3. Make sure both services are running (green status in Render dashboard)
4. If using free tier, backend may have spun down - wait 30 seconds and try again

### Issue: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Cause:** `FRONTEND_URL` not set or incorrect in backend

**Fix:**

1. Go to Backend Service → Environment
2. Set `FRONTEND_URL` to your exact frontend URL (no trailing slash)
3. Click "Save Changes" - this will trigger a redeploy
4. Wait for redeploy to complete

### Issue: "401 Unauthorized"

**Cause:** Auth0 token not being sent or invalid

**Fix:**

1. Check Auth0 settings - make sure your production URL is in:
   - Allowed Callback URLs
   - Allowed Logout URLs
   - Allowed Web Origins
2. Try logging out and logging back in
3. Check backend logs in Render dashboard for auth errors

### Issue: Backend Health Check Fails

**Cause:** Backend service is down or misconfigured

**Fix:**

1. Go to Render Dashboard → Backend Service
2. Check "Events" or "Logs" tab for errors
3. Verify `DATABASE_URL` is set (if using PostgreSQL)
4. Verify `OPENAI_API_KEY` is set
5. Try manually restarting the service

## How to Verify Everything is Set Up Correctly

### Step 1: Check Environment Variables

**Frontend Service:**

```bash
# Should be set to your backend URL + /api
REACT_APP_API_URL=https://promptly-backend-dcbp.onrender.com/api
```

**Backend Service:**

```bash
# Should be set to your frontend URL (no trailing slash)
FRONTEND_URL=https://promptly-frontend-dcbp.onrender.com

# Required for production
ENVIRONMENT=production
DATABASE_URL=<auto-set by Render>
OPENAI_API_KEY=<your-key>
AUTH0_DOMAIN=<your-domain>
AUTH0_API_AUDIENCE=<your-audience>
```

### Step 2: Test Backend Health

Open in browser: `https://your-backend-url.onrender.com/api/health`

Should return: `{"status":"healthy"}`

### Step 3: Test from Frontend

1. Open your deployed frontend
2. Open browser console (F12)
3. Try sending a message
4. Look for network requests to your backend URL

## Still Having Issues?

1. **Check Render Logs:**

   - Backend Service → Logs tab
   - Look for errors, especially around startup or requests

2. **Check Browser Network Tab:**

   - Open DevTools (F12) → Network tab
   - Try sending a message
   - Look for failed requests (red)
   - Click on failed requests to see error details

3. **Verify URLs Match:**

   - Frontend URL: What you see in the browser address bar
   - `FRONTEND_URL` in backend: Must match exactly
   - `REACT_APP_API_URL` in frontend: Must point to backend + `/api`

4. **Free Tier Spin-down:**
   - If using free tier, backend may spin down after 15 min inactivity
   - First request after spin-down takes ~30 seconds
   - Consider upgrading to paid plan for always-on service
