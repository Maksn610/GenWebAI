# 🚀 GenWebAI - Next-Gen Web Content Generator

[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](Dockerfile)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](tests/)
![Coverage](https://codecov.io/gh/Maksn610/GenWebAI/branch/main/graph/badge.svg)
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

## 🚀 Quick Start

### Local Development

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

# Generate a website
python generate.py --topic "AI in Healthcare" --style technical
```

### Example Output
```
[2025-06-16 00:04:49,843] INFO: [CLI] Generating site 1 of 1 for topic='AI in Healthcare'
[2025-06-16 00:04:49,844] INFO: Generating website for topic='AI in Healthcare', style='technical'
[2025-06-16 00:04:49,845] INFO: Selected sections: ['Introduction', 'Use Cases', 'Technical Details', 'Challenges', 'Summary']
[2025-06-16 00:04:50,970] INFO: Calling LangChain runnable...
[2025-06-16 00:05:10,865] INFO: [CLI] Site saved to: sites/d392a9ca-2a0c-45fe-8e93-3fb6cfc4dbe8.html

[✔] Site 1/1
    📄 Title: AI in Healthcare
    📝 Meta: An in-depth look at the implementation, applications, technical aspects, and challenges of Artificial Intelligence in the healthcare sector.
    📁 Path: sites/d392a9ca-2a0c-45fe-8e93-3fb6cfc4dbe8.html
```

### Docker Deployment

```bash
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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📫 Contact

Maksym - [@Maksn610](https://github.com/Maksn610)

Project Link: [https://github.com/Maksn610/GenWebAI](https://github.com/Maksn610/GenWebAI)

---

⭐️ Star this project if you find it useful!
