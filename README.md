<div align="center">
   <img width=100% src="https://capsule-render.vercel.app/api?type=waving&height=300&color=0:282C34,25:181921,75:313642,100:282C34&text=ChainPulse&fontColor=F7DC6F" />
</div>

> **Implementasi "String Matching Algorithms for Cryptocurrency News Sentiment Analysis and Price Prediction"**

> Dipakai untuk kebutuhan makalah **IF2211 Strategi Algoritma**

---

# **ChainPulse**

ChainPulse is a full-stack web application that analyzes real-time cryptocurrency news to extract coin sentiment using advanced string matching algorithms such as Aho-Corasick, Levenshtein (fuzzy matching), and regex. It offers an interactive dashboard powered by D3.js for visualizing coin sentiment trends from the CryptoPanic API.

<div align="center">
    <img width=100% src="frontend/public/chainpulse.png" />

> <b>Dikembangkan dengan ❤️ untuk Strategi Algoritma </b>

</div>

---

## Features & Technologies

#### ChainPulse offers the following features:

-   Real-time cryptocurrency news aggregation
-   Sentiment analysis on crypto news
-   Coin mention detection and tracking
-   News sentiment scoring based on string matching algorithms and coin mention detection
-   Interactive frontend dashboard with bubble chart visualization

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-16A085?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Next.js](https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![d3.js](https://img.shields.io/badge/d3.js-F9A03C?style=for-the-badge&logo=d3.js&logoColor=white)](https://d3js.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![CryptoPanic](https://img.shields.io/badge/CryptoPanic-FA5C5C?style=for-the-badge&logo=cryptopanic&logoColor=white)](https://cryptopanic.com/)

---

## Prerequisites

-   Python 3.11+
-   Node.js 18+
-   pnpm (recommended) or npm
-   CryptoPanic API key

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/andrewtedja/chain-pulse.git
cd chain-pulse
```

2. **Backend Setup**
   From root directory:

```bash
cd backend
python -m venv venv
source venv/bin/activate # On Windows: source venv\Scripts\activate
pip install -r requirements.txt
```

---

## **Create .env file (inside backend/) with:**

```env
CRYPTO_PANIC_API_KEY=your_api_key_here
CRYPTO_PANIC_BASE_URL=https://cryptopanic.com/api/v2/posts/
```

> **Note**: The CryptoPanicAPI key is limited and required to fetch news data from CryptoPanic, you can get it from https://cryptopanic.com/developers/api/ after you sign up (and add to the .env file).

> You can make the .env file based on .env.example

3. **Frontend Setup**
   From root directory:

```bash
cd frontend
pnpm install
```

## Running the Application

### (Option 1) Running Concurrently:

1. Get to root directory (outside frontend/ or backend/) using:

```bash
cd chain-pulse
or
cd .. (from frontend/ or backend/)
```

2. Run the following command:

```bash
pnpm run dev
```

> This will start both the backend and frontend servers concurrently, and you can access the local web on http://localhost:3000.

### (Option 2) Running Individually:

1. Start the backend server:

```bash
cd backend
python main.py
# Server runs on http://localhost:8081
```

2. Start the frontend dev server:

```bash
cd frontend
pnpm dev
# Frontend runs on http://localhost:3000
```

> This will start both the backend and frontend servers, and you can access the local web on http://localhost:3000.

---

## Project Structure

```
chain-pulse/
├── README.md
├── package.json
├── pnpm-lock.yaml
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│ ├── app/
│ │ ├── models.py # Database models (News)
│ │ ├── services.py # API endpoints and business logic
│ │ ├── database.py # Database connection
│ │ └── coins.py # Crypto coins related utilities
│ └── main.py # FastAPI application entry (uvicorn)
└── frontend/
    ├── public/ # Static assets
    └── src/
        ├── app/
        │   ├── _components/
        │   │   └── Dashboard.tsx
        │   ├── types/
        │   │   └── types.tsx # Shared types
        │   ├── layout.tsx # Shared layout
        │   └── page.tsx # Contains Dashboard component
        ├── .env.local
        └── package.json
```

> **Note**: The `package.json` in the frontend/ directory is different than the one in the root directory. The root directory is used for concurrently (library for running multiple terminals concurrently) and the frontend/ directory is used for running the frontend dev server.

---

## Author

| Author                                                | NIM      |
| ----------------------------------------------------- | -------- |
| [Andrew Tedjapratama](https://github.com/andrewtedja) | 13523148 |

---

## License

This project is released under the [MIT License](LICENSE).
