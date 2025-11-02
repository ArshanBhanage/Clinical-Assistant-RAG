# 🚀 QUICK START - Deploy in 10 Minutes!

Your Clinical AI Assistant is ready to deploy with pre-built indexes (no Landing AI needed)!

## ✅ What's Ready:
- ✅ Pre-built FAISS indexes (293MB compressed to 112MB)
- ✅ Package ready: `clinical-ai-indexes.zip`
- ✅ Retro dark theme frontend
- ✅ Complete backend with RAG pipeline
- ✅ Docker & cloud deployment configs

---

## 🎯 Choose Your Deployment Path:

### Option 1: Railway + Vercel (10 min) ⭐ EASIEST
**Cost**: ~$5-10/month | **Setup**: Easiest | **Recommended**: Yes

1. **Backend (Railway)**:
   ```bash
   # Visit: https://railway.app
   # New Project → Deploy from GitHub → Select this repo
   # Root directory: /backend
   # Add env var: OPENROUTER_API_KEY=your_key
   # Deploy, then create volume for indexes
   ```

2. **Upload Indexes**:
   ```bash
   npm i -g @railway/cli
   railway login
   railway link
   # Use Railway dashboard to upload clinical-ai-indexes.zip
   # Or use volume mount and extract
   ```

3. **Frontend (Vercel)**:
   ```bash
   # Visit: https://vercel.com
   # Import repo → Root directory: /frontend
   # Add env var: NEXT_PUBLIC_API_URL=https://your-railway-url
   # Deploy
   ```

**Time**: ~10 minutes | **Done!** ✅

---

### Option 2: Docker (5 min) ⭐ FASTEST FOR LOCAL
**Cost**: Free locally | **Setup**: Requires Docker

```bash
# 1. Ensure Docker is installed
docker --version

# 2. Extract indexes (already in backend/indexes/)
# (Skip if indexes are already there)

# 3. Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your_key_here
EOF

# 4. Start everything
docker-compose up -d

# 5. Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

**Time**: ~5 minutes | **Done!** ✅

---

### Option 3: Render (15 min)
**Cost**: Free tier available | **Setup**: Medium

See `DEPLOYMENT_CHECKLIST.md` for detailed steps.

---

## 📋 Files You Have:

| File | Purpose |
|------|---------|
| `clinical-ai-indexes.zip` | Your pre-built indexes (112MB) |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step deployment guide |
| `DEPLOYMENT.md` | Detailed deployment documentation |
| `docker-compose.yml` | Docker deployment config |
| `backend/Dockerfile` | Backend container config |
| `frontend/Dockerfile` | Frontend container config |
| `backend/start.sh` | Backend startup script |
| `prepare-indexes.sh` | Re-package indexes if needed |

---

## 🔑 Required Environment Variables:

### Backend:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key
```

### Frontend:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url
```

Get OpenRouter API key: https://openrouter.ai/keys (free tier available)

---

## 🧪 Test Your Deployment:

### 1. Backend Health Check:
```bash
curl https://your-backend-url/
```

### 2. Test Query:
```bash
curl -X POST https://your-backend-url/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are COVID-19 symptoms?", "domain": "covid"}'
```

### 3. Frontend:
Visit your frontend URL and ask a question!

---

## 💡 Key Points:

✅ **NO Landing AI credits needed** - Uses pre-built indexes
✅ **NO re-ingestion required** - Indexes are ready to use
✅ **Indexes included in deployment** - Just upload the zip
✅ **Fast setup** - 5-10 minutes total

---

## 🆘 Need Help?

### Common Issues:

**"Index files not found"**
→ Ensure indexes are uploaded to correct path (`/app/indexes` for Railway)

**CORS errors**
→ Update `CORS_ORIGINS` in `backend/main.py` with your frontend URL

**Out of memory**
→ Increase RAM allocation (need at least 512MB)

---

## 📚 More Information:

- **Detailed Guide**: `DEPLOYMENT.md`
- **Step-by-Step Checklist**: `DEPLOYMENT_CHECKLIST.md`
- **GitHub Repo**: https://github.com/ArshanBhanage/Clinical-Assistant-RAG

---

## 🎉 Ready to Deploy?

**Railway + Vercel** (Recommended):
1. Deploy backend to Railway → https://railway.app
2. Upload `clinical-ai-indexes.zip` to Railway volume
3. Deploy frontend to Vercel → https://vercel.com
4. Done in 10 minutes!

**Docker** (Local):
```bash
docker-compose up -d
```
Done in 5 minutes!

---

**Questions?** Check `DEPLOYMENT_CHECKLIST.md` for troubleshooting! 🚀
