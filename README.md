# Portfolio Optimizer

A professional portfolio optimization tool implementing **Markowitz Mean-Variance** and **Black-Litterman** models with Monte Carlo simulation for risk assessment. You can acess it via: https://modernportfoliooptimizer0.streamlit.app/

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🎯 Features

### Optimization Models
- **Markowitz (1952):** Classic mean-variance optimization using historical returns
- **Black-Litterman (1992):** Bayesian approach incorporating market equilibrium and investor views

### Risk Analysis
- **Monte Carlo Simulation:** Up to 50,000 scenarios for portfolio performance projection
- **Value at Risk (VaR):** 95th percentile risk metric
- **Conditional Value at Risk (CVaR):** Expected loss in worst 5% scenarios
- **Efficient Frontier:** Visualization of optimal risk-return trade-offs (Markowitz)

### Interactive Dashboard
- **51 Brazilian stocks (B3)** across multiple sectors
- **Custom market views** for Black-Litterman model
- **Real-time data** from Yahoo Finance with local caching
- **Dark theme** professional UI
- **Dynamic visualizations** with Plotly

---

## 📊 Screenshots

### Portfolio Allocation & Risk-Return Analysis
*Optimal asset weights and risk-return positioning*

### Monte Carlo Simulation
*Distribution of portfolio outcomes with VaR/CVaR metrics*

### Correlation Matrix
*Asset correlations with portfolio highlighting*

### Efficient Frontier (Markowitz)
*Risk-return optimization curve*

---

## 🚀 Getting Started

### Quick Start (Automated)

**Windows (PowerShell):**
```powershell
.\setup.ps1
cd dashboard
streamlit run app.py
```

**Linux/Mac:**
```bash
bash setup.sh
cd dashboard
streamlit run app.py
```

**Using Make (Linux/Mac):**
```bash
make install
make run-dashboard
```

---

### Manual Installation

#### Prerequisites
- Python 3.8 or higher (3.11 recommended)
- pip package manager

#### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/portfolio-optimizer.git
cd portfolio-optimizer
```

2. **Install dependencies**

**Option A: Using requirements.txt**
```bash
pip install -r requirements.txt
```

**Option B: Manual installation**
```bash
pip install numpy pandas scipy yfinance plotly streamlit

# Optional (for notebooks)
pip install jupyter matplotlib seaborn
```

3. **Run the dashboard**
```bash
cd dashboard
streamlit run app.py
```

4. **Access the application**
Open your browser and navigate to `http://localhost:8501`

---

## 📚 Project Structure

```
portfolio-optimizer/
├── notebooks/
│   ├── 01_Regressao_para_Markowitz.ipynb    # Markowitz fundamentals
│   ├── 02_Black_Litterman.ipynb             # Black-Litterman implementation
│   └── 03_Monte_Carlo_Risk_Management.ipynb # Monte Carlo & risk metrics
├── dashboard/
│   └── app.py                                # Streamlit application
├── data/                                     # Cached market data (auto-generated)
├── README.md
└── requirements.txt
```

---

## 🔧 Usage

### Basic Workflow

1. **Select Assets:** Choose 2+ stocks from 51 available B3 tickers
2. **Configure Parameters:**
   - Historical period (1-10 years)
   - Maximum weight per asset (10-100%)
   - Risk-free rate (0-50% p.a.)
   - Initial investment amount
3. **Choose Model:**
   - **Markowitz:** Pure historical optimization
   - **Black-Litterman:** Add custom market views (optional)
4. **Optimize:** Click "Optimize Portfolio"
5. **Analyze Results:**
   - Optimal allocation weights
   - Expected return & volatility
   - Sharpe ratio
   - Monte Carlo simulation
   - VaR/CVaR metrics

### Black-Litterman Views

**Absolute View:**
```
"PETR4 will return +15% annually" (confidence: 70%)
```

**Relative View:**
```
"VALE3 will outperform ITUB4 by +5%" (confidence: 60%)
```

Views are incorporated using Bayesian updating to adjust equilibrium returns.

---

## 📖 Methodology

### Markowitz Model

**Objective:** Minimize portfolio variance for target return

$$\min_{w} \quad w^T \Sigma w$$

**Subject to:**
- $w^T \mu = \mu_p$ (target return)
- $w^T \mathbf{1} = 1$ (weights sum to 100%)
- $0 \leq w_i \leq w_{max}$ (weight constraints)

Where:
- $w$ = asset weights
- $\Sigma$ = covariance matrix (annualized)
- $\mu$ = expected returns (annualized)

### Black-Litterman Model

**Step 1: Market Equilibrium**
$$\Pi = \delta \Sigma w_{mkt}$$

**Step 2: Bayesian Update**
$$E[R] = \left[(\tau\Sigma)^{-1} + P^T\Omega^{-1}P\right]^{-1} \left[(\tau\Sigma)^{-1}\Pi + P^T\Omega^{-1}Q\right]$$

Where:
- $\Pi$ = equilibrium returns
- $P$ = view matrix
- $Q$ = view returns
- $\Omega$ = view uncertainty

### Monte Carlo Simulation

Simulates 252 trading days using multivariate normal distribution:

$$r_t \sim N(\mu_{daily}, \Sigma_{daily})$$

Computes final portfolio value distribution and calculates:
- **VaR (95%):** 5th percentile of outcomes
- **CVaR (95%):** Average of worst 5% outcomes

---

## 🛠️ Technologies

### Core Libraries
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation
- **SciPy** - Optimization (SLSQP)
- **yfinance** - Market data

### Visualization
- **Plotly** - Interactive charts
- **Streamlit** - Web dashboard

### Data Management
- **hashlib** - Cache key generation
- Local CSV caching for faster reloads

---

## 📈 Available Assets (51 B3 Stocks)

### By Sector
- **Oil & Gas:** PETR4, PETR3, PRIO3
- **Mining:** VALE3
- **Banks:** ITUB4, BBDC4, BBAS3, SANB11
- **Retail:** MGLU3, LREN3, ARZZ3, VIIA3, PCAR3, ASAI3, CRFB3
- **Consumer Goods:** ABEV3, JBSS3, BEEF3, BRFS3
- **Technology:** TOTS3, LWSA3, MELI34
- **Electric Power:** ELET3, EGIE3, CPFE3, TAEE11, CMIG4
- **Telecommunications:** VIVT3, TIMS3
- **Construction:** CYRE3, MRVE3, EZTC3
- **Industry:** WEGE3, EMBR3, RAIZ4, KLBN11
- **Logistics:** RENT3, RAIL3
- **Healthcare:** RDOR3, HAPV3, FLRY3
- **Paper & Pulp:** SUZB3
- **Steel:** GGBR4, CSNA3, USIM5
- **Education:** COGN3, YDUQ3
- **Others:** B3SA3, CIEL3, NTCO3, RADL3

---

## 🎓 Educational Resources

### Notebooks

Each notebook contains:
- Theoretical foundations
- Step-by-step implementation
- Real market data examples
- Visualizations

**Topics covered:**
1. Regression as optimization (OLS → Markowitz)
2. Bayesian portfolio theory
3. Risk management with Monte Carlo
4. Practical constraints (max weight, no short-selling)

---

## ⚙️ Configuration

### Dashboard Settings

**Constraints:**
- Maximum weight per asset: 10-100%
- Risk-free rate: 0-50% p.a. (default: 2%)

**Simulation:**
- Monte Carlo scenarios: 100-50,000 (default: 10,000)
- Initial investment: R$ 100+ (default: R$ 10,000)

**Data:**
- Enable/disable local caching
- Historical period: 1-10 years

---

## 🐛 Known Issues

### Data Quality
Some tickers may have:
- Insufficient historical data (<100 days)
- Zero volatility (suspended trading)
- Missing values (corporate events)

**Solution:** App automatically filters invalid assets and displays warnings.

### Performance
- Large simulations (50,000 scenarios) may take 10-30 seconds
- Enable caching to speed up repeated analyses

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more asset classes (REITs, ETFs, Crypto)
- [ ] Implement additional optimization models (Risk Parity, Hierarchical Risk Parity)
- [ ] Support for transaction costs and rebalancing
- [ ] Portfolio backtesting module
- [ ] Export to PDF reports
- [ ] Multi-period optimization

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Matheus**
- Focus: Quantitative Finance & Data Science
- Background: Survival Analysis Research

---

## 🙏 Acknowledgments

- **Harry Markowitz** - Modern Portfolio Theory (1952)
- **Fischer Black & Robert Litterman** - Black-Litterman Model (1992)
- **Yahoo Finance** - Market data provider
- **Streamlit** - Dashboard framework

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue or reach out via [LinkedIn/Email].

---

**Built with ❤️ using Python, Streamlit, and Modern Portfolio Theory**
