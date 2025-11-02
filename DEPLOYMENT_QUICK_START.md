# Quick Deployment Guide

## First-Time Setup

1. **Push code to Git:**

   ```bash
   git add .
   git commit -m "Configure for Render deployment"
   git push origin main
   ```

2. **Deploy on Render:**

   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your Git repo
   - Render will auto-detect `render.yaml` and set up everything

3. **Set Environment Variables in Render Dashboard:**

   **Backend Service:**

   - `OPENAI_API_KEY` = Your OpenAI key
   - `AUTH0_DOMAIN` = Your Auth0 domain
   - `AUTH0_API_AUDIENCE` = Your Auth0 API audience
   - `FRONTEND_URL` = Your frontend URL (set after frontend deploys)

   **Frontend Service:**

   - `REACT_APP_API_URL` = Your backend URL (e.g., `https://promptly-backend.onrender.com/api`)

4. **Update Auth0 Settings:**
   - Add your Render URLs to allowed callback/logout/origins

## Making Changes (Automatic Deployment)

Just push to main branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically:

- Detect the push
- Build and deploy your changes
- Show deployment status in dashboard

**No manual steps needed!**

## Environment Variables Reference

### Backend (`promptly-backend`)

- `DATABASE_URL` - Auto-set by Render (from PostgreSQL service)
- `OPENAI_API_KEY` - Your OpenAI API key
- `AUTH0_DOMAIN` - Your Auth0 domain
- `AUTH0_API_AUDIENCE` - Your Auth0 API audience
- `FRONTEND_URL` - Your frontend URL
- `ENVIRONMENT` - `production` (auto-set)
- `SECRET_KEY` - Auto-generated

### Frontend (`promptly-frontend`)

- `REACT_APP_API_URL` - Your backend API URL

## Troubleshooting

**Backend not starting?**

- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure `FRONTEND_URL` matches your actual frontend URL

**Frontend can't connect to backend?**

- Verify `REACT_APP_API_URL` is correct
- Check backend health endpoint: `https://your-backend.onrender.com/api/health`
- Ensure CORS is configured correctly

**Database issues?**

- Check that `DATABASE_URL` is set (auto-set by Render)
- Tables are created automatically on first run

## Full Documentation

See `RENDER_DEPLOYMENT.md` for complete setup instructions and troubleshooting.
