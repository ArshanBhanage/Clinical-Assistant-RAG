# 🚀 Quick Deployment Checklist

## Before You Deploy

### ✅ Step 1: Package Your Indexes
```bash
./prepare-indexes.sh
```
This creates `clinical-ai-indexes.zip` (~293MB)

### ✅ Step 2: Choose Your Hosting Platform

#### Option A: Railway + Vercel (Recommended)
- **Backend**: Railway (handles volumes easily)
- **Frontend**: Vercel (free for hobby)
- **Cost**: ~$5-10/month

#### Option B: Render (Full Stack)
- **Both**: Render
- **Cost**: Free tier available

#### Option C: Docker (Self-hosted)
- **Requirements**: Docker, Docker Compose
- **Cost**: Server costs only

---

## 🎯 Railway Deployment (RECOMMENDED)

### Backend:
1. ✅ Go to https://railway.app
2. ✅ Sign up/Login with GitHub
3. ✅ New Project → Deploy from GitHub
4. ✅ Select `Clinical-Assistant-RAG` repo
5. ✅ Set root directory to `/backend`
6. ✅ Add environment variable:
   - `OPENROUTER_API_KEY` = your key
7. ✅ Deploy (wait for first build)
8. ✅ **Upload Indexes**:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Link to your project
   railway link
   
   # Create and attach volume
   railway volume create indexes
   railway volume attach indexes /app/indexes
   
   # Open shell and upload
   railway shell
   # In the shell, you can upload via scp or dashboard
   ```
9. ✅ Copy your backend URL (e.g., `https://clinical-ai.up.railway.app`)

### Frontend:
1. ✅ Go to https://vercel.com
2. ✅ Sign up/Login with GitHub
3. ✅ Import Project → Select `Clinical-Assistant-RAG`
4. ✅ Set root directory to `/frontend`
5. ✅ Add environment variable:
   - `NEXT_PUBLIC_API_URL` = your Railway backend URL
6. ✅ Deploy
7. ✅ Done! Visit your Vercel URL

---

## 🎯 Render Deployment

### Backend:
1. ✅ Go to https://render.com
2. ✅ New → Web Service
3. ✅ Connect GitHub repo
4. ✅ Settings:
   - Name: `clinical-ai-backend`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `./start.sh`
5. ✅ Add environment variable:
   - `OPENROUTER_API_KEY` = your key
6. ✅ Add Disk:
   - Name: `indexes`
   - Mount Path: `/opt/render/project/src/indexes`
   - Size: 1 GB
7. ✅ Deploy
8. ✅ Upload indexes:
   - Go to Shell tab
   - Upload `clinical-ai-indexes.zip`
   - Run: `unzip clinical-ai-indexes.zip`
9. ✅ Copy backend URL

### Frontend:
1. ✅ New → Static Site
2. ✅ Settings:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `.next`
3. ✅ Add environment variable:
   - `NEXT_PUBLIC_API_URL` = your backend URL
4. ✅ Deploy

---

## 🎯 Docker Deployment (Local/VPS)

### Prerequisites:
```bash
# Install Docker and Docker Compose
# Visit: https://docs.docker.com/get-docker/
```

### Deploy:
```bash
# 1. Ensure indexes are in backend/indexes/
ls backend/indexes/

# 2. Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your_key_here
EOF

# 3. Build and run
docker-compose up -d

# 4. Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## 🧪 Test Your Deployment

### 1. Test Backend Health:
```bash
curl https://your-backend-url.com/
```
Expected: `{"message": "Clinical AI Assistant API", ...}`

### 2. Test Query:
```bash
curl -X POST https://your-backend-url.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are COVID-19 symptoms?", "domain": "covid"}'
```

### 3. Test Frontend:
Visit your frontend URL and submit a query!

---

## 🐛 Troubleshooting

### ❌ "Index files not found"
**Fix**: Ensure indexes are uploaded to `/app/indexes` (Railway) or `/opt/render/project/src/indexes` (Render)

### ❌ CORS errors
**Fix**: Update `CORS_ORIGINS` in `backend/main.py`:
```python
CORS_ORIGINS = [
    "https://your-frontend.vercel.app",
    # ... add your domains
]
```

### ❌ Memory errors
**Fix**: Increase memory allocation (indexes + model = ~500MB RAM minimum)

### ❌ Slow first request
**Fix**: Use paid tier with "always on" to avoid cold starts

---

## 💰 Estimated Costs

| Platform | Backend | Frontend | Total/Month |
|----------|---------|----------|-------------|
| Railway + Vercel | $5-10 | Free | $5-10 |
| Render | Free/Starter | Free | $0-7 |
| Docker (VPS) | $5 | $5 | $5 |

---

## ✅ Post-Deployment

### Update CORS in backend/main.py:
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://your-app.vercel.app",  # ADD THIS
]
```

### Commit and push:
```bash
git add .
git commit -m "Configure for deployment"
git push origin main
```

---

## 🎉 You're Done!

Your Clinical AI Assistant is now live with:
- ✅ Pre-built FAISS indexes (no Landing AI needed)
- ✅ Retro dark theme UI
- ✅ 34,000+ indexed documents
- ✅ OpenRouter LLM integration

**Share your URL!** 🚀
