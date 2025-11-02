# 🚀 Deployment Guide - Clinical AI Assistant

## Overview
This guide helps you deploy the Clinical AI Assistant without re-ingesting documents. Your pre-built FAISS indexes will be used directly.

---

## 📦 Pre-Deployment Checklist

### ✅ What You Have:
- Pre-built FAISS indexes (293MB in `backend/indexes/`)
- Complete frontend (Next.js with retro dark theme)
- FastAPI backend with RAG pipeline
- No need for Landing AI credits

### ⚠️ Important Notes:
- **Indexes are NOT in GitHub** (293MB, too large)
- You'll upload indexes directly to the hosting platform
- Backend will load existing indexes on startup

---

## 🎯 Deployment Options

### **Option 1: Vercel (Frontend) + Railway (Backend)** ⭐ RECOMMENDED

#### **A. Deploy Backend to Railway**

1. **Create Railway Account**: https://railway.app/

2. **Create New Project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `Clinical-Assistant-RAG` repository
   - Select `backend` as root directory

3. **Add Environment Variables**:
   ```bash
   OPENROUTER_API_KEY=your_openrouter_key_here
   PORT=8000
   ```

4. **Upload Pre-built Indexes**:
   - Railway provides persistent volumes
   - After first deployment, use Railway CLI:
   ```bash
   railway login
   railway link
   railway volume create indexes
   railway volume attach indexes /app/indexes
   ```
   
   - Then upload your indexes:
   ```bash
   railway run rsync -avz backend/indexes/ /app/indexes/
   ```

5. **Update `backend/config.py`** (see changes below)

6. **Deploy**: Railway will auto-deploy

7. **Get Backend URL**: Copy your Railway backend URL (e.g., `https://your-app.up.railway.app`)

#### **B. Deploy Frontend to Vercel**

1. **Create Vercel Account**: https://vercel.com/

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import `Clinical-Assistant-RAG` repository
   - Select `frontend` as root directory

3. **Configure Build Settings**:
   - Framework Preset: `Next.js`
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Add Environment Variable**:
   ```bash
   NEXT_PUBLIC_API_URL=https://your-railway-backend-url.up.railway.app
   ```

5. **Deploy**: Vercel will auto-deploy

---

### **Option 2: Render (Full Stack)**

1. **Create Render Account**: https://render.com/

2. **Deploy Backend**:
   - New → Web Service
   - Connect GitHub repo
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variables:
     ```bash
     OPENROUTER_API_KEY=your_key
     PYTHON_VERSION=3.11
     ```

3. **Add Disk for Indexes**:
   - In service settings, add a disk
   - Mount path: `/opt/render/project/src/indexes`
   - Size: 1GB
   - Upload indexes via Render dashboard

4. **Deploy Frontend**:
   - New → Static Site
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `.next`
   - Add Environment Variable:
     ```bash
     NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
     ```

---

### **Option 3: Docker + Any Cloud Provider**

See `docker-compose.yml` (created below) for containerized deployment.

---

## 🔧 Required Code Changes

### 1. Update `backend/config.py` - Make paths deployment-friendly

I'll create this change automatically.

### 2. Create `backend/requirements.txt` if missing

Already exists.

### 3. Create startup script that checks for indexes

I'll create this automatically.

---

## 📤 Upload Indexes to Deployment

### Method 1: Direct Upload (Railway/Render Dashboard)
1. Zip your indexes: `cd backend && zip -r indexes.zip indexes/`
2. Upload via platform dashboard
3. Unzip on server

### Method 2: Railway CLI (Recommended for Railway)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and link
railway login
railway link

# Upload indexes
railway run bash
# Then in the shell:
mkdir -p /app/indexes
exit

# Copy files (run locally)
railway run rsync -avz backend/indexes/ /app/indexes/
```

### Method 3: Cloud Storage + Download on Startup
- Upload to AWS S3, Google Cloud Storage, or Dropbox
- Add download script in startup (see below)

---

## 🔒 Security Checklist

✅ `.env` file is in `.gitignore`
✅ API keys are environment variables
✅ Indexes are not in GitHub
✅ CORS is configured in `backend/main.py`

---

## 🧪 Test Deployment

After deployment:

1. **Test Backend**:
   ```bash
   curl https://your-backend-url.com/
   # Should return: {"message": "Clinical AI Assistant API", ...}
   ```

2. **Test Frontend**:
   - Visit your Vercel URL
   - Submit a query
   - Check if it connects to backend

3. **Test Query**:
   ```bash
   curl -X POST https://your-backend-url.com/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What are COVID-19 symptoms?", "domain": "covid"}'
   ```

---

## 💰 Cost Estimates

### Free Tier Options:
- **Vercel**: Free for hobby projects
- **Railway**: $5/month after free trial (includes 512MB RAM)
- **Render**: Free tier available (may be slow)

### Recommended:
- **Frontend (Vercel)**: Free
- **Backend (Railway)**: ~$5-10/month
- **Total**: ~$5-10/month

---

## 🐛 Troubleshooting

### Issue: "Index files not found"
**Solution**: Ensure indexes are uploaded to correct path and `config.py` points to right location.

### Issue: Backend timeout
**Solution**: Increase memory allocation (indexes are 293MB + model loading needs RAM).

### Issue: CORS errors
**Solution**: Update `CORS_ORIGINS` in `backend/main.py` with your frontend URL.

### Issue: Cold starts (slow first request)
**Solution**: Use Railway/Render paid tier with "always on" option.

---

## 📝 Quick Start Commands

### For Railway:
```bash
# Backend
cd backend
railway login
railway init
railway up
railway volume create indexes
railway volume attach indexes /app/indexes

# Upload indexes
zip -r indexes.zip indexes/
# Upload via dashboard
```

### For Vercel:
```bash
# Frontend
cd frontend
npm install
vercel login
vercel --prod
```

---

## 🎉 Done!

After deployment:
1. Your frontend will be at: `https://your-app.vercel.app`
2. Your backend will be at: `https://your-app.railway.app`
3. No Landing AI credits needed - uses pre-built indexes!

---

**Need help?** Check platform documentation:
- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Render Docs](https://render.com/docs)
