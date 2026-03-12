.PHONY: install run-dashboard run-notebooks clean help

help:
	@echo "Portfolio Optimizer - Available Commands"
	@echo "========================================"
	@echo "make install        - Install all dependencies"
	@echo "make run-dashboard  - Run Streamlit dashboard"
	@echo "make run-notebooks  - Open Jupyter notebooks"
	@echo "make clean          - Clean cache files"
	@echo "make help           - Show this help"

install:
	@echo "Installing dependencies..."
	pip install numpy pandas scipy yfinance plotly streamlit
	@echo "Done! Run 'make run-dashboard' to start."

install-dev:
	@echo "Installing all dependencies (including Jupyter)..."
	pip install numpy pandas scipy yfinance plotly streamlit jupyter matplotlib seaborn
	@echo "Done!"

run-dashboard:
	@echo "Starting Streamlit dashboard..."
	cd dashboard && streamlit run app.py

run-notebooks:
	@echo "Starting Jupyter..."
	cd notebooks && jupyter notebook

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	rm -rf data/*.csv 2>/dev/null || true
	@echo "Done!"
