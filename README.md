# 🚀 GenWebAI - Next-Gen Web Content Generator

[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](Dockerfile)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](tests/)

## 🌟 Features

- 🤖 AI-Powered Content Generation
- 🎯 High-Performance Processing
- 🔒 Secure & Scalable Architecture
- 📊 Advanced Analytics & Logging
- 🐳 Docker Containerization
- 🧪 Comprehensive Test Suite

## 🛠️ Tech Stack

- Python 3.11
- FastAPI
- Docker & Docker Compose
- Pytest
- Modern Python Libraries

## 🚀 Quick Start### Local Development

```bash
# Clone the repository
git clone https://github.com/Maksn610/GenWebAI.git
cd GenWebAI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env  # For Windows use: copy .env.example .env
# Then open the .env file and paste your OpenAI API key

# Generate a website
python generate.py --topic "AI in Healthcare" --style technical
```

### Docker Deployment

To build and run the application using Docker:

```bash
# Clone the repository
git clone https://github.com/Maksn610/GenWebAI.git
cd GenWebAI

# Create a .env file with your OpenAI API key
cp .env.example .env
# Then edit .env and set your key:
# OPENAI_API_KEY=your_openai_key_here

# Build and run with Docker Compose
docker-compose up --build
```

## 📁 Project Structure

```
GenWebAI/
├── app/                # Main application code
├── tests/             # Test suite
├── .venv/             # Virtual environment
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage (90%+ code coverage)
pytest --cov=app tests/
```

## 🔄 CI/CD

This project uses GitHub Actions for continuous integration and deployment. On each push to the `main` branch:

- The code is built and tested.
- A Docker image is built and pushed to GitHub Container Registry (GHCR) using the latest `Dockerfile`.
- Secrets for authentication are securely managed using GitHub Actions Secrets (e.g., `GHCR_TOKEN`).

You can find the workflow in `.github/workflows/docker-publish.yml`.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📫 Contact

Maksym - [@Maksn610](https://github.com/Maksn610)

Project Link: [https://github.com/Maksn610/GenWebAI](https://github.com/Maksn610/GenWebAI)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

⭐️ Star this project if you find it useful!