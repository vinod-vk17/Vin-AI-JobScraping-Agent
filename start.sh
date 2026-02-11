#!/bin/bash

# Quick Start Script for Job Scraper Web App
# This script sets up and runs the application

echo "🚀 Job Scraper Web App - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✓ Python detected: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your GEMINI_API_KEY"
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Check if database exists
if [ ! -f "jobs.db" ]; then
    echo ""
    echo "🔍 No database found. Would you like to run the scraper first? (y/n)"
    read -p "> " run_scraper
    
    if [ "$run_scraper" = "y" ]; then
        echo ""
        echo "🤖 Running initial scrape (this may take a few minutes)..."
        python gemini_scraper.py
        echo "✓ Initial scrape complete"
    fi
fi

echo ""
echo "🌐 Starting web application..."
echo "===================================="
echo ""
echo "🎉 Web app will be available at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python app.py
