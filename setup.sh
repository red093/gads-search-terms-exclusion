#!/bin/bash
# Setup script for Google Ads Search Terms Analyzer
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Google Ads Search Terms Analyzer - Setup${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"

# Check Python version is 3.7+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo -e "${RED}Error: Python 3.7 or higher is required.${NC}"
    echo "You have Python $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}! Virtual environment already exists at ./$VENV_DIR${NC}"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${YELLOW}Using existing virtual environment.${NC}"
    fi
fi

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓${NC} Virtual environment created at ./$VENV_DIR"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓${NC} pip upgraded to latest version"

# Install requirements
echo -e "${BLUE}Installing dependencies from requirements.txt...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} All dependencies installed successfully"

# Check if google-ads.yaml exists
if [ ! -f "google-ads.yaml" ]; then
    echo -e "\n${YELLOW}⚠ Configuration file not found${NC}"
    echo "You need to create a google-ads.yaml file with your credentials."
    echo ""
    read -p "Do you want to copy the example file now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp google-ads.yaml.example google-ads.yaml
        echo -e "${GREEN}✓${NC} Created google-ads.yaml from example"
        echo -e "${YELLOW}Please edit google-ads.yaml and add your credentials.${NC}"
    fi
fi

# Setup complete
echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}================================================${NC}\n"

echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "2. Configure your credentials (if not done already):"
echo -e "   ${BLUE}nano google-ads.yaml${NC}"
echo ""
echo "3. Run the analyzer:"
echo -e "   ${BLUE}python search_terms_analyzer.py --customer-id YOUR_CUSTOMER_ID${NC}"
echo ""
echo "To deactivate the virtual environment later, just run:"
echo -e "   ${BLUE}deactivate${NC}"
echo ""
