#!/bin/bash
set -e

echo "Bootstrapping local development environment..."

# Create directories if they don't exist
mkdir -p data/raw data/processed data/quarantine data/reports logs
mkdir -p docker/postgres

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo "Local environment bootstrap complete!"
echo "Run the pipeline with: python -m src.pipeline.main"
echo "Run tests with: pytest tests/ -v"
