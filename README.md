# P&ID Digitizer - AI-Powered Process Diagram Analysis

An intelligent web application that uses Google's Vertex AI (Gemini) to analyze P&ID (Piping and Instrumentation Diagram) images and extract structured data including equipment, instrumentation, valves, and process connections.

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app/)

## ✨ Features

- **AI-Powered Analysis**: Uses Google's Gemini 2.5 Pro model for accurate P&ID interpretation
- **Interactive Visualization**: Displays original image with AI-detected components
- **Structured Data Export**: Export results as JSON or CSV
- **Knowledge Graph**: Interactive process flow visualization
- **Multi-format Support**: Handles PNG, JPG, JPEG images
- **Real-time Processing**: Fast analysis with progress indicators

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Vertex AI (Gemini 2.5 Pro)
- **Image Processing**: OpenCV, PIL
- **Data Visualization**: Pyvis, NetworkX, Matplotlib
- **Data Processing**: Pandas, NumPy

## 📋 Requirements

- Python 3.8+
- Google Cloud Project with Vertex AI enabled
- Streamlit Cloud account

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pid-digitizer-streamlit.git
   cd pid-digitizer-streamlit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials**:
   - Create a Google Cloud project
   - Enable Vertex AI API
   - Create a service account with Vertex AI permissions
   - Set environment variables:
     ```bash
     export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
     export GOOGLE_CLOUD_LOCATION="us-central1"
     export GOOGLE_CLOUD_MODEL_ID="gemini-2.5-pro"
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

1. **Fork this repository**
2. **Set up Google Cloud project** (see detailed instructions in DEPLOYMENT.md)
3. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Configure secrets with your Google Cloud project details
   - Deploy!

## 📊 Data Structure

The application extracts the following data categories:

- **Equipment**: Pumps, tanks, vessels, etc.
- **Instrumentation**: Sensors, controllers, indicators
- **Lines**: Process piping and connections
- **Valves**: Control valves, isolation valves
- **Junctions**: Pipe intersections and connections
- **Control Relationships**: Control loops and signal connections
- **Annotations**: Text labels and notes
- **Safety Devices**: Relief valves, safety systems

## 🔧 Configuration

### Environment Variables

- `GOOGLE_CLOUD_PROJECT_ID`: Your Google Cloud project ID
- `GOOGLE_CLOUD_LOCATION`: GCP region (default: us-central1)
- `GOOGLE_CLOUD_MODEL_ID`: AI model (default: gemini-2.5-pro)

### Streamlit Secrets

Configure in Streamlit Cloud dashboard:

```toml
[gcp]
project_id = "your-project-id"
location = "us-central1"
model_id = "gemini-2.5-pro"
```

## 📈 Performance

- **Analysis Time**: 10-30 seconds per image (depending on complexity)
- **Image Size**: Optimized for images up to 10MB
- **Supported Formats**: PNG, JPG, JPEG
- **Concurrent Users**: Limited by Streamlit Cloud free tier

## 🛡️ Security

- No image data is stored permanently
- All processing happens in memory
- Google Cloud credentials are securely managed
- Temporary files are automatically cleaned up

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub Issues
- **Documentation**: Check DEPLOYMENT.md for detailed setup instructions
- **Community**: Join our discussions in GitHub Discussions

## 🙏 Acknowledgments

- Google Cloud Vertex AI team for the powerful Gemini model
- Streamlit team for the excellent web framework
- OpenCV community for image processing capabilities
