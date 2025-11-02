# Browser Compatibility Issues

If the app works on one laptop/browser but not another, here are common issues and fixes:

## Common Browser-Specific Issues

### 1. CORS Preflight OPTIONS Requests

**Symptom:** Network errors, especially on Safari or Firefox
**Cause:** Some browsers are stricter about CORS preflight requests
**Fix:** Already implemented - backend now explicitly allows OPTIONS requests

### 2. Browser Extensions Blocking Requests

**Symptom:** Network errors or requests failing silently
**Common culprits:**

- Ad blockers (uBlock Origin, AdBlock Plus)
- Privacy extensions (Privacy Badger, Ghostery)
- Security extensions
- VPN extensions

**Fix:**

1. Disable extensions temporarily to test
2. Add the site to extension whitelist
3. Use incognito/private mode to test without extensions

### 3. Browser Security Settings

**Symptom:** CORS errors, blocked requests
**Check:**

- Browser security/privacy settings
- Mixed content (HTTPS/HTTP) blocking
- Third-party cookie blocking

**Fix:**

- Ensure both frontend and backend use HTTPS (they do on Render)
- Check if cookies/localStorage are blocked
- Check browser console for specific security errors

### 4. HTTPS Mixed Content

**Symptom:** Some requests work, others fail
**Cause:** Browser blocking HTTP requests from HTTPS page
**Fix:** Already handled - both frontend and backend use HTTPS on Render

### 5. Cached/Cookie Issues

**Symptom:** Authentication fails or weird behavior
**Fix:**

1. Clear browser cache and cookies for the site
2. Try incognito/private mode
3. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### 6. Network/Firewall Issues

**Symptom:** Timeouts or connection refused
**Cause:**

- Corporate firewall
- VPN blocking requests
- Network restrictions

**Fix:**

- Try different network (mobile hotspot, different WiFi)
- Disable VPN temporarily
- Check if corporate firewall blocks Render domains

## Testing Steps for Different Browser

1. **Open Browser Console (F12)**

   - Go to Console tab
   - Look for errors
   - Go to Network tab
   - Try sending a message
   - Check if requests appear and their status

2. **Check Network Tab:**

   - Are requests being made?
   - What's the status code?
   - Any CORS errors in red?
   - Click on failed requests to see details

3. **Test Backend Directly:**
   - Open: `https://your-backend-url.onrender.com/api/health`
   - Should see: `{"status":"healthy"}`
   - If this fails, backend is the issue
   - If this works, frontend/network is the issue

## Browser-Specific Considerations

### Safari

- Stricter CORS policies
- May block third-party cookies by default
- **Fix:** Check Safari privacy settings → "Prevent cross-site tracking"

### Firefox

- Privacy-focused defaults
- May block tracking cookies
- **Fix:** Check Firefox privacy settings

### Chrome/Edge

- Generally works well
- Check extensions first
- Check if "Block third-party cookies" is enabled

## Quick Fix Checklist

When someone reports network errors:

1. ✅ **Check Browser Console (F12)**

   - What specific error appears?
   - Copy the error message

2. ✅ **Test Backend Health Endpoint**

   - Open: `https://your-backend-url.onrender.com/api/health`
   - Does it work?

3. ✅ **Try Incognito/Private Mode**

   - Rules out extensions and cache issues

4. ✅ **Check Network Tab**

   - Are requests being made?
   - What's the response status?

5. ✅ **Check Browser/OS**

   - What browser and version?
   - What operating system?
   - Any VPN or proxy?

6. ✅ **Try Different Browser**
   - If Chrome fails, try Firefox
   - If Firefox fails, try Chrome
   - Helps identify browser-specific issues

## Most Common Fixes

1. **Disable Browser Extensions** - Especially ad blockers
2. **Clear Cache and Cookies** - Fresh start
3. **Check CORS Configuration** - Verify `FRONTEND_URL` matches exactly
4. **Try Incognito Mode** - Rules out local issues
5. **Test on Different Network** - Rules out firewall issues
