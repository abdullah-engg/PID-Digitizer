# Streamlit Cloud Deployment Guide

## Prerequisites

1. **Google Cloud Project Setup**:
   - Create a Google Cloud Project
   - Enable Vertex AI API
   - Create a service account with Vertex AI permissions
   - Download service account JSON key

2. **GitHub Repository**:
   - Push your code to GitHub
   - Ensure `app.py` is in the root directory
   - Include `requirements.txt` in root directory

## Deployment Steps

### 1. Prepare Google Cloud Authentication

**Option A: Service Account Key (Recommended for Streamlit Cloud)**
1. Go to Google Cloud Console → IAM & Admin → Service Accounts
2. Create a new service account with Vertex AI User role
3. Download the JSON key file
4. In Streamlit Cloud dashboard, go to your app → Settings → Secrets
5. Add the JSON content as a secret named `gcp_service_account`

**Option B: Environment Variables**
Set these in Streamlit Cloud dashboard:
- `GOOGLE_CLOUD_PROJECT_ID`: Your GCP project ID
- `GOOGLE_CLOUD_LOCATION`: us-central1
- `GOOGLE_CLOUD_MODEL_ID`: gemini-2.5-pro

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - **Repository**: Your GitHub repo
   - **Branch**: main (or your preferred branch)
   - **Main file path**: app.py
5. Click "Deploy"

### 3. Configure Secrets (After Initial Deployment)

1. Go to your app dashboard
2. Click "Settings" → "Secrets"
3. Add your Google Cloud configuration:

```toml
[gcp]
project_id = "your-actual-project-id"
location = "us-central1"
model_id = "gemini-2.5-pro"
```

## Troubleshooting

- **Authentication Errors**: Ensure service account has proper permissions
- **Import Errors**: Check that all dependencies are in requirements.txt
- **File Path Issues**: All paths are relative, should work on Streamlit Cloud
- **Memory Issues**: Streamlit Cloud has memory limits for free tier

## Cost Considerations

- Google Cloud Vertex AI charges per API call
- Streamlit Cloud free tier has usage limits
- Consider implementing caching for repeated analyses
