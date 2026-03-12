# Portfolio Optimizer - Automated Setup Script
# Run: .\setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Portfolio Optimizer - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    $version = [regex]::Match($pythonVersion, "\d+\.\d+").Value
    $major = [int]$version.Split('.')[0]
    $minor = [int]$version.Split('.')[1]
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "ERROR: Python 3.8+ required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
    
    if ($major -eq 3 -and $minor -ge 13) {
        Write-Host "WARNING: Python 3.13+ may have compatibility issues. Python 3.11 recommended." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "ERROR: Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

pip install numpy pandas scipy yfinance plotly streamlit

Write-Host ""

# Optional: Install Jupyter for notebooks
$jupyter = Read-Host "Install Jupyter for notebooks? (y/n)"
if ($jupyter -eq "y" -or $jupyter -eq "Y") {
    Write-Host "Installing Jupyter, matplotlib, seaborn..." -ForegroundColor Yellow
    pip install jupyter matplotlib seaborn
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Test imports
Write-Host "Testing installation..." -ForegroundColor Yellow
try {
    python -c "import numpy, pandas, scipy, yfinance, plotly, streamlit; print('All packages imported successfully!')"
    Write-Host "All dependencies working!" -ForegroundColor Green
}
catch {
    Write-Host "WARNING: Some packages failed to import" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. cd dashboard" -ForegroundColor White
Write-Host "2. streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "For notebooks:" -ForegroundColor Cyan
Write-Host "1. cd notebooks" -ForegroundColor White
Write-Host "2. jupyter notebook" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
