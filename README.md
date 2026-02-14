# UniSummarize

A full-stack web application for summarizing university content and educational materials.

## Overview

UniSummarize is a modern web application built with a Python backend and JavaScript frontend that helps users quickly summarize and understand complex educational content. Whether you're a student looking to quickly grasp key concepts or an educator seeking efficient content summarization tools, UniSummarize provides an intuitive interface to process and summarize your materials.

## Tech Stack

### Backend
- **Language:** Python
- **Framework:** Flask (based on main.py structure)
- **Dependencies:** See `backend/requirements.txt`

### Frontend
- **Language:** JavaScript
- **Styling:** Tailwind CSS
- **Build Tools:** PostCSS
- **Package Manager:** npm
- **Deployment:** Node.js server with static file serving

## Project Structure

```
unisummarize/
├── backend/
│   ├── main.py              # Main Flask application
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/                 # React/JavaScript source code
│   ├── public/              # Static public assets
│   ├── package.json         # Frontend dependencies
│   ├── package-lock.json    # Dependency lock file
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   ├── postcss.config.js    # PostCSS configuration
│   ├── server.js            # Express/Node server
│   ├── serve.json           # Serve configuration
│   └── static.json          # Static file configuration
└── package-lock.json
```

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Node.js and npm
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python main.py
```

The backend server will start and be available at `http://localhost:5000` (or the configured port).

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install npm dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000` (or the configured port).

### Running Both Services

For a complete development environment, run the backend and frontend services in separate terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Features

- **Text Summarization:** Quickly summarize large blocks of text
- **Content Processing:** Handle various types of educational content
- **User-Friendly Interface:** Clean, modern UI built with Tailwind CSS
- **Responsive Design:** Works on desktop and mobile devices
- **Fast Processing:** Efficient Python backend for quick summarization

## API Documentation

The backend provides RESTful API endpoints for text summarization. The API details can be found in the backend implementation (`backend/main.py`).

## Frontend Components

The frontend is built with modern JavaScript and uses Tailwind CSS for styling. Key directories:
- `src/` - React components and application logic
- `public/` - Static assets and index.html

## Configuration Files

- **tailwind.config.js** - Tailwind CSS theme and variant configuration
- **postcss.config.js** - PostCSS plugin configuration
- **serve.json** - Frontend serving configuration
- **static.json** - Static asset configuration for deployment

## Deployment

Both the backend and frontend are configured for deployment:
- Backend: Deploy the Python Flask application to a Python hosting service
- Frontend: Deploy to any static hosting service or run the Node.js server

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for use and modification.

## Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.

---

**Last Updated:** February 14, 2026