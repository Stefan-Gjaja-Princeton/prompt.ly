# Quick Fix: "Network Error" When Creating Conversation

## Immediate Checks on Render Dashboard

### 1. Check Frontend Environment Variable

Go to: **Render Dashboard → Frontend Service → Environment**

**Verify `REACT_APP_API_URL` is set:**

- Should be: `https://your-backend-url.onrender.com/api`
- **MUST include `/api` at the end**
- Replace `your-backend-url` with your actual backend service name

**If missing or incorrect:**

1. Click "Add Environment Variable"
2. Key: `REACT_APP_API_URL`
3. Value: `https://your-backend-url.onrender.com/api`
4. Click "Save Changes"
5. Wait for redeploy (2-5 minutes)

### 2. Check Backend Environment Variable

Go to: **Render Dashboard → Backend Service → Environment**

**Verify `FRONTEND_URL` is set:**

- Should be: `https://your-frontend-url.onrender.com`
- **No trailing slash!**
- Replace `your-frontend-url` with your actual frontend service name

**If missing or incorrect:**

1. Click "Add Environment Variable" or edit existing
2. Key: `FRONTEND_URL`
3. Value: `https://your-frontend-url.onrender.com`
4. Click "Save Changes"
5. Wait for redeploy (2-5 minutes)

### 3. Verify Backend is Running

**Test the backend directly:**

1. Open: `https://your-backend-url.onrender.com/api/health`
2. Should see: `{"status":"healthy"}`
3. If it times out or errors → Backend is down

**If backend is down:**

1. Go to Render Dashboard → Backend Service
2. Check "Events" or "Logs" tab for errors
3. Check that service shows "Live" status (green)
4. If red, click "Manual Deploy" or check logs for errors

### 4. Check Service URLs Match Exactly

**Get your actual URLs:**

- Frontend URL: From Render Dashboard → Frontend Service (shown at top)
- Backend URL: From Render Dashboard → Backend Service (shown at top)

**Then verify:**

- `REACT_APP_API_URL` in Frontend = `https://[backend-url]/api`
- `FRONTEND_URL` in Backend = `https://[frontend-url]` (no trailing slash)

## After Making Changes

1. **Wait for redeploy** (2-5 minutes)
2. **Hard refresh** your browser (Ctrl+Shift+R or Cmd+Shift+R)
3. **Clear browser cache** if needed
4. **Try again** - send a message

## Check Browser Console for Details

1. Open your deployed site
2. Press **F12** (open DevTools)
3. Go to **Console** tab
4. Look for error messages
5. You should now see more detailed errors that tell you exactly what's wrong

## Most Common Fix

**90% of the time, it's one of these:**

1. ✅ `REACT_APP_API_URL` not set or incorrect in Frontend
2. ✅ `FRONTEND_URL` not set or incorrect in Backend
3. ✅ Backend service is down or not deployed

## Still Not Working?

After making the changes above:

1. Wait for redeploy (5 minutes)
2. Hard refresh browser
3. Try in incognito/private mode
4. Check browser console (F12) for specific error
5. Test backend health endpoint directly in browser
