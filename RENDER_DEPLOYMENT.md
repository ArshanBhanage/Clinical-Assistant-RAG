# 🚀 Render Deployment Guide - Clinical AI Assistant

## Complete Step-by-Step Instructions

---

## Part 1: Deploy Backend (10 minutes)

### Step 1: Sign Up / Login to Render
1. Go to: https://render.com
2. Click **"Get Started"** or **"Sign In"**
3. Sign in with **GitHub** (recommended)

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find and select: **`Clinical-Assistant-RAG`** repository
5. Click **"Connect"**

### Step 3: Configure Backend Service
Fill in these settings:

**Basic Settings:**
- **Name**: `clinical-ai-backend`
- **Region**: `Oregon (US West)` (or closest to you)
- **Branch**: `main`
- **Root Directory**: `backend`

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `./start-render.sh`

**Instance Type:**
- Select: **Free** (or paid for better performance)

### Step 4: Add Environment Variable
Scroll to **"Environment Variables"** section:

Click **"Add Environment Variable"**:
```
Key: OPENROUTER_API_KEY
Value: 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
```

Click **"Add"**

### Step 5: Add Persistent Disk
Scroll to **"Disks"** section:

Click **"Add Disk"**:
- **Name**: `indexes-storage`
- **Mount Path**: `/app/indexes`
- **Size**: `1 GB` (free tier includes 1GB)

Click **"Add Disk"**

### Step 6: Create Service
1. Click **"Create Web Service"** button at bottom
2. Wait 3-5 minutes for deployment (watch the logs)
3. Once deployed, you'll see: ✅ **"Your service is live"**

### Step 7: Get Backend URL
1. On your service dashboard, look for the URL at top
2. Copy it: `https://clinical-ai-backend.onrender.com`
3. **SAVE THIS URL** - you'll need it for frontend!

---

## Part 2: Upload Indexes (15 minutes)

### Step 8: Access Shell
1. In your backend service dashboard
2. Click **"Shell"** tab (top navigation)
3. Wait for shell to load (green "Connected" status)

### Step 9: Prepare Directory
In the shell, run these commands:
```bash
# Navigate to indexes mount point
cd /app/indexes

# Check current location
pwd
# Should show: /app/indexes

# List files (should be empty initially)
ls -la
```

### Step 10: Upload Index File
You have 2 options:

#### **Option A: Direct Upload in Shell** (If available)
- Look for **"Upload"** button in shell interface
- Select: `clinical-ai-indexes.zip` (112MB from your computer)
- Wait for upload to complete

#### **Option B: Using SCP** (If Shell upload unavailable)
On your local terminal (NOT Render shell):
```bash
# Render will provide SSH connection details in Shell tab
# Look for something like: ssh -i key.pem user@host
```

### Step 11: Extract Indexes
Back in Render shell:
```bash
# Extract the zip file
unzip clinical-ai-indexes.zip

# Verify all files are present
ls -la

# You should see:
# - covid_index.faiss
# - covid_metadata.pkl
# - diabetes_index.faiss
# - diabetes_metadata.pkl
# - heart_attack_index.faiss
# - heart_attack_metadata.pkl
# - knee_injuries_index.faiss
# - knee_injuries_metadata.pkl
# - all_documents.pkl

# Remove zip file to save space
rm clinical-ai-indexes.zip

# Check disk usage
du -sh .
# Should show ~293MB
```

### Step 12: Restart Service
1. Go back to your service dashboard
2. Click **"Manual Deploy"** dropdown (top right)
3. Select **"Clear build cache & deploy"**
4. Wait for restart (~2 minutes)

### Step 13: Verify Backend is Working
1. Click on your service URL: `https://clinical-ai-backend.onrender.com`
2. You should see:
   ```json
   {
     "status": "online",
     "message": "Clinical AI Assistant API is running",
     "domains": ["covid", "diabetes", "heart_attack", "knee_injuries"]
   }
   ```

3. Test health endpoint: `https://clinical-ai-backend.onrender.com/health`
4. Should show all indexes loaded

---

## Part 3: Deploy Frontend (5 minutes)

### Step 14: Create Frontend Service
1. Click **"New +"** button again
2. Select **"Web Service"**
3. Select same repository: **`Clinical-Assistant-RAG`**
4. Click **"Connect"**

### Step 15: Configure Frontend Service
**Basic Settings:**
- **Name**: `clinical-ai-frontend`
- **Region**: Same as backend (e.g., Oregon)
- **Branch**: `main`
- **Root Directory**: `frontend`

**Build & Deploy:**
- **Runtime**: `Node`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm start`

**Instance Type:**
- Select: **Free**

### Step 16: Add Frontend Environment Variable
In **"Environment Variables"** section:

Click **"Add Environment Variable"**:
```
Key: NEXT_PUBLIC_API_URL
Value: https://clinical-ai-backend.onrender.com
```
*(Replace with your ACTUAL backend URL from Step 7)*

Click **"Add"**

### Step 17: Deploy Frontend
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build and deployment
3. Once live, you'll see: ✅ **"Your service is live"**

### Step 18: Get Frontend URL
1. Copy your frontend URL: `https://clinical-ai-frontend.onrender.com`
2. This is your live application!

---

## Part 4: Test Application (2 minutes)

### Step 19: Test Your Live App
1. Visit: `https://clinical-ai-frontend.onrender.com`
2. You should see the retro dark theme interface
3. Select domain: **"Heart Attack"**
4. Ask question: **"What are the symptoms of a heart attack?"**
5. Wait ~10-15 seconds (free tier is slower)
6. You should get response with sources and evidence!

---

## 🎉 You're Live!

**Your URLs:**
- 🌐 **Frontend**: `https://clinical-ai-frontend.onrender.com`
- 🔧 **Backend API**: `https://clinical-ai-backend.onrender.com`
- 📊 **API Docs**: `https://clinical-ai-backend.onrender.com/docs`

---

## 📋 Troubleshooting

### Backend shows "No indexes found"
- Go to Shell → `/app/indexes`
- Run: `ls -la` to check files
- If empty, re-upload and extract zip

### Frontend can't connect to backend
- Check environment variable: `NEXT_PUBLIC_API_URL`
- Must be exact backend URL (with https://)
- Redeploy frontend after fixing

### Disk full error
- 1GB should be enough for indexes (~293MB)
- Delete zip file: `rm clinical-ai-indexes.zip`

### Service sleeping (free tier)
- Free tier services sleep after 15 min inactivity
- First request takes ~30 seconds to wake up
- Consider upgrading to paid tier ($7/month) for always-on

---

## 🔒 Important Notes

1. **Don't commit API keys to GitHub** - Already safe in render.yaml
2. **Free tier limitations**:
   - Services sleep after 15 min inactivity
   - 750 hours/month free compute
   - Slower response times
3. **Indexes are persistent** - Stored on disk, won't be deleted
4. **Updates**: Push to GitHub → Render auto-deploys

---

## 💰 Cost Estimate

**Free Tier (Current Setup):**
- Backend: Free ($0/month)
- Frontend: Free ($0/month)
- Disk: 1GB Free ($0/month)
- **Total: $0/month** ✅

**Paid Tier (For Production):**
- Backend: Starter ($7/month)
- Frontend: Starter ($7/month)
- Disk: 1GB included
- **Total: $14/month**

---

## 🚀 Next Steps

After deployment:
- Share your frontend URL with users
- Monitor usage in Render dashboard
- Consider upgrading for better performance
- Add custom domain (optional)

---

**Need help?** Check Render logs or ask me! 🎯
