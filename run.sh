#!/bin/bash
# Helper script to run the analyzer with virtual environment activated
# Usage: ./run.sh --customer-id YOUR_CUSTOMER_ID [other options]

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run ./setup.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the analyzer with all provided arguments
python search_terms_analyzer.py "$@"

# Deactivate is automatic when script exits
