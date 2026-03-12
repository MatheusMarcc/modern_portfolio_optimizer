import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import minimize
from datetime import datetime, timedelta
import os
import hashlib

# Config
st.set_page_config(
    page_title="Portfolio Optimizer",
    page_icon="■",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
os.makedirs(CACHE_DIR, exist_ok=True)

# Session state
if 'views_list' not in st.session_state:
    st.session_state.views_list = []
if 'views_selected' not in st.session_state:
    st.session_state.views_selected = []

# CSS - Dark Theme
st.markdown("""
<style>
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
        border-right: 1px solid #333333;
    }
    
    [data-testid="stSidebar"] * {
        color: #e5e5e5 !important;
    }
    
    /* Headers */
    .main-header {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 2.5rem;
        font-weight: 300;
        letter-spacing: 0.1em;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    
    .subtitle {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 0.9rem;
        font-weight: 300;
        letter-spacing: 0.05em;
        color: #999999;
        margin-bottom: 3rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 300 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #999999 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d5f2e 100%);
        color: #ffffff;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 300;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d5f2e 0%, #1f4420 100%);
        border-color: #2d5f2e;
    }
    
    /* Small delete button */
    .stButton > button[kind="secondary"] {
        background: transparent;
        color: #8B0000;
        border: 1px solid #8B0000;
        padding: 0.3rem 0.8rem;
        font-size: 0.75rem;
        border-radius: 4px;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(139, 0, 0, 0.1);
        color: #ffffff;
        border-color: #8B0000;
    }
    
    [data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }
    
    [data-baseweb="select"] input[role="combobox"] {
        pointer-events: auto !important;
    }
    
    [data-baseweb="select"] input::selection {
        background: transparent !important;
    }
    
    input:not([data-baseweb="select"] input), select {
        background-color: #1a1a1a !important;
        color: #e5e5e5 !important;
        border: 1px solid #333333 !important;
    }
    
    /* Divider */
    hr {
        border-color: #333333;
        margin: 2rem 0;
    }
    
    /* Text */
    p, span, label {
        color: #e5e5e5 !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #e5e5e5;
    }
    
    [data-baseweb="tag"] {
        background: linear-gradient(135deg, #2d1a1a 0%, #1a1a1a 100%) !important;
        border: 1px solid #4a2020 !important;
    }
    
    [data-baseweb="tag"] span {
        color: #d4a5a5 !important;
    }
    
    [data-baseweb="tag"]:hover {
        background: linear-gradient(135deg, #3d2020 0%, #2a1a1a 100%) !important;
        border-color: #5a2525 !important;
    }
    
    [data-baseweb="tag"] svg {
        fill: #d4a5a5 !important;
    }
    
    [data-baseweb="tag"]:hover svg {
        fill: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #999999;
        background-color: transparent;
        border-bottom: 2px solid transparent;
        padding: 0.5rem 0;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 300;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    .stTabs [aria-selected="true"] {
        color: #2d5f2e;
        border-bottom: 2px solid #2d5f2e;
    }
</style>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const observer = new MutationObserver(function() {
            const selectInputs = document.querySelectorAll('[data-baseweb="select"] input');
            selectInputs.forEach(input => {
                input.addEventListener('keydown', function(e) {
                    const allowedKeys = ['ArrowUp', 'ArrowDown', 'Enter', 'Escape', 'Tab'];
                    if (!allowedKeys.includes(e.key)) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                });
                input.addEventListener('input', function(e) {
                    e.preventDefault();
                    this.value = '';
                });
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    });
</script>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">Portfolio Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Quantitative Analysis with Markowitz & Black-Litterman</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("Configuration")

modelo = st.sidebar.selectbox(
    "Optimization Model",
    ["Markowitz", "Black-Litterman"],
    help="Markowitz: historical returns | Black-Litterman: incorporates market views",
    key="modelo_select"
)

st.sidebar.subheader("Assets")
ativos_disponiveis = {
    # Oil & Gas
    'PETR4.SA': 'Petrobras PN',
    'PETR3.SA': 'Petrobras ON',
    'PRIO3.SA': 'Prio',
    
    # Mining
    'VALE3.SA': 'Vale',
    
    # Banks
    'ITUB4.SA': 'Itaú',
    'BBDC4.SA': 'Bradesco',
    'BBAS3.SA': 'Banco do Brasil',
    'SANB11.SA': 'Santander',
    
    # Retail
    'MGLU3.SA': 'Magazine Luiza',
    'LREN3.SA': 'Lojas Renner',
    'ARZZ3.SA': 'Arezzo',
    'VIIA3.SA': 'Via',
    'PCAR3.SA': 'Grupo Pão de Açúcar',
    'ASAI3.SA': 'Assaí',
    'CRFB3.SA': 'Carrefour Brasil',
    
    # Consumer Goods
    'ABEV3.SA': 'Ambev',
    'JBSS3.SA': 'JBS',
    'BEEF3.SA': 'Minerva',
    'BRFS3.SA': 'BRF',
    
    # Technology
    'TOTS3.SA': 'Totvs',
    'LWSA3.SA': 'Locaweb',
    'MELI34.SA': 'MercadoLibre',
    
    # Electric Power
    'ELET3.SA': 'Eletrobras',
    'EGIE3.SA': 'Engie',
    'CPFE3.SA': 'CPFL Energia',
    'TAEE11.SA': 'Taesa',
    'CMIG4.SA': 'Cemig',
    
    # Telecommunications
    'VIVT3.SA': 'Vivo',
    'TIMS3.SA': 'Tim',
    
    # Construction
    'CYRE3.SA': 'Cyrela',
    'MRVE3.SA': 'MRV',
    'EZTC3.SA': 'EZ Tec',
    
    # Industry
    'WEGE3.SA': 'WEG',
    'EMBR3.SA': 'Embraer',
    'RAIZ4.SA': 'Raízen',
    'KLBN11.SA': 'Klabin',
    
    # Logistics
    'RENT3.SA': 'Localiza',
    'RAIL3.SA': 'Rumo',
    
    # Healthcare
    'RDOR3.SA': 'Rede D\'Or',
    'HAPV3.SA': 'Hapvida',
    'FLRY3.SA': 'Fleury',
    
    # Paper & Pulp
    'SUZB3.SA': 'Suzano',
    
    # Steel
    'GGBR4.SA': 'Gerdau',
    'CSNA3.SA': 'CSN',
    'USIM5.SA': 'Usiminas',
    
    # Education
    'COGN3.SA': 'Cogna',
    'YDUQ3.SA': 'Yduqs',
    
    # Others
    'B3SA3.SA': 'B3',
    'CIEL3.SA': 'Cielo',
    'NTCO3.SA': 'Natura',
    'RADL3.SA': 'Raia Drogasil'
}

ativos_selecionados = st.sidebar.multiselect(
    "Select assets",
    options=list(ativos_disponiveis.keys()),
    default=[],
    format_func=lambda x: ativos_disponiveis[x]
)

anos = st.sidebar.slider("Historical period (years)", 1, 10, 5)
end_date = datetime.now()
start_date = end_date - timedelta(days=anos*365)

st.sidebar.subheader("Constraints")
max_peso = st.sidebar.slider("Maximum weight per asset (%)", 10, 100, 35) / 100
rf = st.sidebar.number_input("Risk-free rate (% p.a.)", 0.0, 50.0, 2.0, 0.5) / 100

st.sidebar.subheader("Simulation")
n_sim = st.sidebar.number_input("Monte Carlo simulations", 100, 50000, 5000, 500)
inv = st.sidebar.number_input("Initial investment (BRL)", 100.0, 10000000.0, 10000.0, 100.0)

usar_cache = st.sidebar.checkbox("Use data cache", value=True)

# Functions
def get_cache_file(tickers, start, end):
    key = f"{'_'.join(sorted(tickers))}_{start.date()}_{end.date()}"
    return os.path.join(CACHE_DIR, f"prices_{hashlib.md5(key.encode()).hexdigest()[:12]}.csv")

@st.cache_data(ttl=3600)  # Cache por 1 hora
def baixar_dados(tickers, start, end, use_cache):
    cache_file = get_cache_file(tickers, start, end)
    
    if use_cache and os.path.exists(cache_file):
        try:
            prices = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            if all(t in prices.columns for t in tickers):
                return prices[tickers]
        except:
            pass
    
    data = yf.download(tickers, start=start, end=end, progress=False)
    prices = data['Close'] if len(tickers) > 1 else data[['Close']].rename(columns={'Close': tickers[0]})
    
    if use_cache:
        try:
            prices.to_csv(cache_file)
        except:
            pass
    
    return prices

def validar_dados(prices, tickers, nomes):
    validos, invalidos = [], []
    
    for t in tickers:
        if t not in prices.columns:
            invalidos.append({'ticker': t, 'nome': nomes[t], 'reason': 'Not found'})
            continue
        
        serie = prices[t].dropna()
        if len(serie) < 100:
            invalidos.append({'ticker': t, 'nome': nomes[t], 'reason': f'Short history ({len(serie)} days)'})
            continue
        
        ret = serie.pct_change().dropna()
        if ret.std() == 0 or np.isnan(ret.std()):
            invalidos.append({'ticker': t, 'nome': nomes[t], 'reason': 'Zero volatility'})
            continue
        
        validos.append(t)
    
    return validos, invalidos

def validar_view_duplicada(views_list, nova_view):
    """Check if view already exists"""
    for v in views_list:
        if nova_view['tipo'] == 'absoluta' and v['tipo'] == 'absoluta':
            if v['idx'] == nova_view['idx']:
                return True, f"View already exists for {nova_view['nome']}"
        
        elif nova_view['tipo'] == 'relativa' and v['tipo'] == 'relativa':
            # Same pair (order doesn't matter)
            if (v['idx1'] == nova_view['idx1'] and v['idx2'] == nova_view['idx2']) or \
               (v['idx1'] == nova_view['idx2'] and v['idx2'] == nova_view['idx1']):
                return True, f"View already exists for {nova_view['nome1']} vs {nova_view['nome2']}"
    
    return False, ""

def calcular_metricas(prices):
    returns = prices.pct_change().dropna()
    return returns, returns.mean().values * 252, returns.cov().values * 252

def retornos_equilibrio(Sigma, rf):
    n = len(Sigma)
    w_mkt = np.ones(n) / n
    R_mkt, var_mkt = 0.10, w_mkt @ Sigma @ w_mkt
    delta = (R_mkt - rf) / var_mkt
    return delta * (Sigma @ w_mkt)

def aplicar_views(Pi, Sigma, views, tau=0.025):
    if not views:
        return Pi
    
    n, k = len(Pi), len(views)
    P, Q, Omega = np.zeros((k, n)), np.zeros(k), np.zeros((k, k))
    
    for i, v in enumerate(views):
        if v['tipo'] == 'absoluta':
            P[i, v['idx']] = 1
            Q[i] = v['retorno']
        else:
            P[i, v['idx1']], P[i, v['idx2']] = 1, -1
            Q[i] = v['diferenca']
        
        conf = v['confianca'] / 100
        Omega[i, i] = (1 / conf) * tau * (P[i] @ Sigma @ P[i])
    
    tau_S = tau * Sigma
    M = np.linalg.inv(np.linalg.inv(tau_S) + P.T @ np.linalg.inv(Omega) @ P)
    return M @ (np.linalg.inv(tau_S) @ Pi + P.T @ np.linalg.inv(Omega) @ Q)

def otimizar(mu, Sigma, max_w, rf):
    n = len(mu)
    obj = lambda w: -(w @ mu - rf) / np.sqrt(w @ Sigma @ w)
    cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, max_w)] * n
    
    res = minimize(obj, np.ones(n)/n, method='SLSQP', bounds=bounds, constraints=cons)
    w = res.x
    return {
        'pesos': w,
        'retorno': w @ mu,
        'volatilidade': np.sqrt(w @ Sigma @ w),
        'sharpe': (w @ mu - rf) / np.sqrt(w @ Sigma @ w)
    }

def fronteira_eficiente(mu, Sigma, rf, n_pontos=50):
    """Calculate efficient frontier"""
    ret_min = mu.min()
    ret_max = mu.max()
    rets_target = np.linspace(ret_min, ret_max, n_pontos)
    
    vols = []
    for ret_target in rets_target:
        n = len(mu)
        obj = lambda w: np.sqrt(w @ Sigma @ w)
        cons = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - ret_target}
        ]
        bounds = [(0, 1)] * n
        
        res = minimize(obj, np.ones(n)/n, method='SLSQP', bounds=bounds, constraints=cons)
        if res.success:
            vols.append(res.fun)
        else:
            vols.append(np.nan)
    
    return rets_target, np.array(vols)

def monte_carlo(w, mu, Sigma, n_sim, inv):
    import time
    start = time.time()
    
    mu_d, Sigma_d = mu / 252, Sigma / 252
    
    # Gerar TODAS as simulações de uma vez (vetorizado)
    returns = np.random.multivariate_normal(mu_d, Sigma_d, (n_sim, 252))
    
    # Calcular retornos do portfólio para todas simulações
    portfolio_returns = returns @ w  # (n_sim, 252)
    
    # Calcular valor final para cada simulação
    vals = inv * np.prod(1 + portfolio_returns, axis=1)
    
    elapsed = time.time() - start
    print(f"✅ Monte Carlo vetorizado: {n_sim} sims em {elapsed:.2f}s")
    
    return vals

# Dark theme for Plotly
PLOTLY_THEME = dict(
    plot_bgcolor='#0a0a0a',
    paper_bgcolor='#0a0a0a',
    font=dict(family='Helvetica Neue, Arial', size=11, color='#e5e5e5'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#333333',
        gridwidth=0.5,
        color='#999999',
        zerolinecolor='#333333'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#333333',
        gridwidth=0.5,
        color='#999999',
        zerolinecolor='#333333'
    ),
    showlegend=False
)

# Views (Black-Litterman)
if modelo == "Black-Litterman" and len(ativos_selecionados) >= 2:
    st.subheader("Market Views")
    
    col_config, col_lista = st.columns([2, 1])
    
    with col_config:
        st.markdown("**Add View**")
        
        tipo = st.selectbox("Type", ["Absolute (1 asset)", "Relative (2 assets)"], key="tipo_view")
        
        if "Absolute" in tipo:
            ativo = st.selectbox("Asset", ativos_selecionados, format_func=lambda x: ativos_disponiveis[x], key="ativo_abs")
            retorno = st.number_input("Expected return (%)", -50.0, 100.0, 15.0, 1.0, key="ret_abs")
            conf = st.slider("Confidence (%)", 0, 100, 70, 10, key="conf_abs")
            
            if st.button("Add View", key="add_abs"):
                nova_view = {
                    'tipo': 'absoluta',
                    'idx': ativos_selecionados.index(ativo),
                    'nome': ativos_disponiveis[ativo],
                    'retorno': retorno / 100,
                    'confianca': conf
                }
                
                duplicada, msg = validar_view_duplicada(st.session_state.views_list, nova_view)
                
                if duplicada:
                    st.error(f"⚠️ {msg}")
                else:
                    st.session_state.views_list.append(nova_view)
                    st.session_state.views_selected.append(True)
                    st.rerun()
        
        else:
            col1, col2 = st.columns(2)
            with col1:
                ativo1 = st.selectbox("Asset 1", ativos_selecionados, format_func=lambda x: ativos_disponiveis[x], key="ativo1_rel")
            with col2:
                opcoes_ativo2 = [a for a in ativos_selecionados if a != ativo1]
                if opcoes_ativo2:
                    ativo2 = st.selectbox("Asset 2", opcoes_ativo2, 
                                         format_func=lambda x: ativos_disponiveis[x], key="ativo2_rel")
                else:
                    st.warning("Selecione mais ativos")
                    ativo2 = None
            
            if ativo2:
                dif = st.number_input("Difference (A1 - A2) %", -50.0, 50.0, 5.0, 1.0, key="dif_rel")
                conf_rel = st.slider("Confidence (%)", 0, 100, 60, 10, key="conf_rel")
                
                if st.button("Add View", key="add_rel"):
                    nova_view = {
                        'tipo': 'relativa',
                        'idx1': ativos_selecionados.index(ativo1),
                        'idx2': ativos_selecionados.index(ativo2),
                        'nome1': ativos_disponiveis[ativo1],
                        'nome2': ativos_disponiveis[ativo2],
                        'diferenca': dif / 100,
                        'confianca': conf_rel
                    }
                    
                    duplicada, msg = validar_view_duplicada(st.session_state.views_list, nova_view)
                    
                    if duplicada:
                        st.error(f"⚠️ {msg}")
                    else:
                        st.session_state.views_list.append(nova_view)
                        st.session_state.views_selected.append(True)
                        st.rerun()
    
    with col_lista:
        col_title, col_delete = st.columns([2, 1])
        with col_title:
            st.markdown("**Active Views**")
        with col_delete:
            if st.session_state.views_list:
                views_selecionadas_indices = [i for i, sel in enumerate(st.session_state.views_selected) if sel]
                if views_selecionadas_indices and st.button("Delete Selected", key="delete_selected", type="secondary", help="Delete selected views"):
                    for i in sorted(views_selecionadas_indices, reverse=True):
                        st.session_state.views_list.pop(i)
                        st.session_state.views_selected.pop(i)
                    st.rerun()
        
        if st.session_state.views_list:
            for i, v in enumerate(st.session_state.views_list):
                col_check, col_text = st.columns([1, 9])
                
                with col_check:
                    checked = st.checkbox("", value=st.session_state.views_selected[i], key=f"check_{i}", label_visibility="collapsed")
                    st.session_state.views_selected[i] = checked
                
                with col_text:
                    if v['tipo'] == 'absoluta':
                        st.markdown(f"{v['nome']}: {v['retorno']*100:.1f}% (conf: {v['confianca']}%)")
                    else:
                        st.markdown(f"{v['nome1']} > {v['nome2']}: {v['diferenca']*100:+.1f}% (conf: {v['confianca']}%)")
            
            st.markdown("---")
            usar_views = st.checkbox("Use selected views", value=True, key="usar_views")
        else:
            st.info("No views configured")
            usar_views = False
    
    st.markdown("---")

# Optimize
processar = st.button("Optimize Portfolio", type="primary")

if processar and len(ativos_selecionados) >= 2:
    
    with st.spinner(f'⏳ Downloading {len(ativos_selecionados)} assets... Please wait (first time may take 30-60s)'):
        prices = baixar_dados(ativos_selecionados, start_date, end_date, usar_cache)
    
    validos, invalidos = validar_dados(prices, ativos_selecionados, ativos_disponiveis)
    
    if invalidos:
        st.warning(f"{len(invalidos)} asset(s) removed")
        st.dataframe(pd.DataFrame(invalidos), use_container_width=True, hide_index=True)
    
    if len(validos) < 2:
        st.error("Minimum 2 valid assets required")
        st.stop()
    
    prices = prices[validos]
    returns, mu_hist, Sigma = calcular_metricas(prices)
    
    # Select returns
    if modelo == "Black-Litterman":
        Pi = retornos_equilibrio(Sigma, rf)
        
        # Filter only selected views
        views_ativas = [v for i, v in enumerate(st.session_state.views_list) 
                       if i < len(st.session_state.views_selected) and st.session_state.views_selected[i]]
        
        if views_ativas and usar_views:
            mu_final = aplicar_views(Pi, Sigma, views_ativas)
            st.info(f"Black-Litterman with {len(views_ativas)} selected view(s)")
        else:
            mu_final = Pi
            st.info("Black-Litterman without views (equilibrium)")
    else:
        mu_final = mu_hist
        st.info("Markowitz (historical returns)")
    
    portfolio = otimizar(mu_final, Sigma, max_peso, rf)
    
    # Identify assets in portfolio (>1%)
    ativos_no_portfolio = [validos[i] for i, peso in enumerate(portfolio['pesos']) if peso > 0.01]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Return", f"{portfolio['retorno']:.2%}")
    col2.metric("Volatility", f"{portfolio['volatilidade']:.2%}")
    col3.metric("Sharpe Ratio", f"{portfolio['sharpe']:.3f}")
    col4.metric("Active Assets", f"{(portfolio['pesos'] > 0.01).sum()}/{len(validos)}")
    
    st.markdown("---")
    
    # PRINCIPAIS: Allocation & Risk-Return
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Optimal Allocation")
        
        df_aloc = pd.DataFrame({
            'Asset': [ativos_disponiveis[t] for t in validos],
            'Weight': portfolio['pesos']
        }).sort_values('Weight', ascending=True)
        
        colors = ['#2d5f2e' if w > 0.01 else '#333333' for w in df_aloc['Weight']]
        
        fig_aloc = go.Figure(go.Bar(
            x=df_aloc['Weight'],
            y=df_aloc['Asset'],
            orientation='h',
            text=df_aloc['Weight'].apply(lambda x: f'{x:.1%}' if x > 0.01 else 'Excluded'),
            textposition='outside',
            marker=dict(
                color=colors,
                line=dict(width=0.5, color='#1a1a1a')
            )
        ))
        
        fig_aloc.update_layout(
            **PLOTLY_THEME,
            xaxis_title="Portfolio Weight",
            yaxis_title="",
            height=400
        )
        st.plotly_chart(fig_aloc, use_container_width=True, key="aloc_main")
    
    with col_right:
        st.subheader("Risk vs Return")
        
        df_scatter = pd.DataFrame({
            'Asset': [ativos_disponiveis[t] for t in validos],
            'Vol': np.sqrt(np.diag(Sigma)),
            'Ret': mu_final
        })
        
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(
            x=df_scatter['Vol'],
            y=df_scatter['Ret'],
            mode='markers+text',
            text=df_scatter['Asset'],
            textposition='top center',
            marker=dict(size=10, color='#666666', line=dict(width=1, color='#999999'))
        ))
        fig_scatter.add_trace(go.Scatter(
            x=[portfolio['volatilidade']],
            y=[portfolio['retorno']],
            mode='markers+text',
            text=['Portfolio'],
            textposition='top center',
            marker=dict(size=15, color='#2d5f2e', symbol='diamond',
                       line=dict(width=2, color='#ffffff'))
        ))
        
        fig_scatter.update_layout(
            **PLOTLY_THEME,
            xaxis_title="Volatility",
            yaxis_title="Expected Return",
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_main")
    
    st.markdown("---")
    
    # Monte Carlo
    st.markdown("### Monte Carlo Simulation")
    
    estimated_time = max(1, int(n_sim / 10000))  # ~10k simulações por segundo após otimização
    with st.spinner(f'🎲 Running {int(n_sim):,} simulations... (~{estimated_time} second{"s" if estimated_time > 1 else ""})'):
        vals = monte_carlo(portfolio['pesos'], mu_final, Sigma, int(n_sim), inv)
    
    VaR = np.percentile(vals, 5)
    CVaR = vals[vals <= VaR].mean()
    media = vals.mean()
    
    var_return_pct = ((VaR - inv) / inv) * 100
    cvar_return_pct = ((CVaR - inv) / inv) * 100
    
    if CVaR >= inv:
        var_interpretation = f"In 95% of scenarios, you will have at least R$ {VaR:,.2f} ({var_return_pct:+.1f}%)"
        cvar_interpretation = f"In the worst 5% of scenarios, average value is R$ {CVaR:,.2f} ({cvar_return_pct:+.1f}%)"
        risk_assessment = "🟢 Low downside risk - even worst-case scenarios show positive returns"
    else:
        cvar_loss = inv - CVaR
        cvar_loss_pct = abs(cvar_return_pct)
        var_interpretation = f"In 95% of scenarios, you will have at least R$ {VaR:,.2f} ({var_return_pct:.1f}%)"
        cvar_interpretation = f"In the worst 5% of scenarios, average value is R$ {CVaR:,.2f} ({cvar_return_pct:.1f}%)"
        
        if cvar_loss_pct < 20:
            risk_assessment = f"🟡 Moderate downside risk - in worst 5% scenarios, average loss is R$ {cvar_loss:,.2f} ({cvar_loss_pct:.1f}%)"
        else:
            risk_assessment = f"🔴 Significant downside risk - in worst 5% scenarios, average loss is R$ {cvar_loss:,.2f} ({cvar_loss_pct:.1f}%)"
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Value", f"R$ {media:,.2f}")
    col2.metric("Average Return", f"{(media/inv - 1)*100:+.1f}%")
    col3.metric("VaR 95%", f"R$ {VaR:,.2f}")
    col4.metric("CVaR 95%", f"R$ {CVaR:,.2f}")
    
    fig_hist = go.Figure()
    
    vals_loss = vals[vals < inv]
    vals_profit = vals[vals >= inv]
    
    if len(vals_loss) > 0:
        fig_hist.add_trace(go.Histogram(
            x=vals_loss,
            nbinsx=25,
            marker=dict(color='#8B0000', line=dict(width=0.5, color='#1a1a1a')),
            name='Loss',
            showlegend=False
        ))
    
    if len(vals_profit) > 0:
        fig_hist.add_trace(go.Histogram(
            x=vals_profit,
            nbinsx=25,
            marker=dict(color='#2d5f2e', line=dict(width=0.5, color='#1a1a1a')),
            name='Profit',
            showlegend=False
        ))
    
    fig_hist.update_layout(barmode='overlay')
    
    fig_hist.add_vline(x=inv, line=dict(dash="dash", color="#666666", width=1.5),
                      annotation=dict(text="Initial", font=dict(size=10, color='#999999')))
    fig_hist.add_vline(x=media, line=dict(dash="dash", color="#2d5f2e", width=2),
                      annotation=dict(text="Average", font=dict(size=10, color='#2d5f2e')))
    fig_hist.add_vline(x=VaR, line=dict(dash="dash", color="#8B0000", width=2),
                      annotation=dict(text="VaR 95%", font=dict(size=10, color='#8B0000')))
    
    fig_hist.update_layout(
        **PLOTLY_THEME,
        xaxis_title="Final Value (BRL)",
        yaxis_title="Frequency",
        height=400
    )
    st.plotly_chart(fig_hist, use_container_width=True, key="hist_main")
    
    prob = (vals > inv).sum() / int(n_sim) * 100
    
    st.markdown("**Interpretation**")
    st.markdown(f"""
    - **Profit probability:** {prob:.1f}% of scenarios result in gains
    - **VaR 95%:** {var_interpretation}
    - **CVaR 95%:** {cvar_interpretation}
    - **Risk assessment:** {risk_assessment}
    """)
    
    st.markdown("---")
    
    # Tabs
    if modelo == "Markowitz":
        tab1, tab2, tab3 = st.tabs(["Efficient Frontier", "Correlation Matrix", "Historical Performance"])
        
        with tab1:
            st.subheader("Efficient Frontier")
            
            rets_front, vols_front = fronteira_eficiente(mu_final, Sigma, rf)
            
            fig_front = go.Figure()
            
            fig_front.add_trace(go.Scatter(
                x=vols_front,
                y=rets_front,
                mode='lines',
                line=dict(color='#2d5f2e', width=2),
                name='Efficient Frontier'
            ))
            
            fig_front.add_trace(go.Scatter(
                x=np.sqrt(np.diag(Sigma)),
                y=mu_final,
                mode='markers',
                marker=dict(size=8, color='#666666', line=dict(width=1, color='#999999')),
                text=[ativos_disponiveis[t] for t in validos],
                name='Assets'
            ))
            
            fig_front.add_trace(go.Scatter(
                x=[portfolio['volatilidade']],
                y=[portfolio['retorno']],
                mode='markers',
                marker=dict(size=12, color='#2d5f2e', symbol='diamond', 
                           line=dict(width=2, color='#ffffff')),
                text=['Optimal Portfolio'],
                name='Portfolio'
            ))
            
            fig_front.update_layout(
                **PLOTLY_THEME,
                xaxis_title="Volatility (Risk)",
                yaxis_title="Expected Return",
                height=500
            )
            
            st.plotly_chart(fig_front, use_container_width=True, key="frontier")
    else:
        tab2, tab3 = st.tabs(["Correlation Matrix", "Historical Performance"])
    
    with tab2:
        st.subheader("Correlation Matrix")
        
        st.info("""
        **Why correlation matters:**
        - 🟢 **Low correlation (<0.4):** Assets move independently → **excellent** diversification benefit
        - ⚫ **Medium correlation (0.4-0.7):** Some independence → **moderate** diversification
        - 🔴 **High correlation (>0.7):** Assets move together → **poor** diversification benefit
        - The optimizer may exclude highly correlated assets if one has better Sharpe ratio
        - Green cells = better for diversification | Red cells = worse for diversification
        - Assets in bold are included in the optimal portfolio
        """)
        
        corr_matrix = returns[validos].corr()
        
        annotations = []
        for i, ticker_i in enumerate(validos):
            for j, ticker_j in enumerate(validos):
                corr_val = corr_matrix.iloc[i, j]
                
                if ticker_i in ativos_no_portfolio and ticker_j in ativos_no_portfolio:
                    if corr_val > 0.7:
                        text_color = '#0a0a0a'
                    else:
                        text_color = '#ffffff'
                    weight = 'bold'
                else:
                    if corr_val > 0.7:
                        text_color = '#333333'
                    else:
                        text_color = '#e5e5e5'
                    weight = 'normal'
                
                annotations.append(dict(
                    x=j,
                    y=i,
                    text=f'{corr_val:.2f}',
                    font=dict(size=10, color=text_color, family='Helvetica Neue'),
                    showarrow=False
                ))
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=[ativos_disponiveis[t] for t in validos],
            y=[ativos_disponiveis[t] for t in validos],
            colorscale=[
                [0, '#2d5f2e'],
                [0.5, '#1a1a1a'],
                [1, '#8B0000']
            ],
            showscale=True,
            colorbar=dict(
                title=dict(text="Correlation", side="right"),
                tickfont=dict(color='#e5e5e5')
            ),
            hovertemplate='%{y} vs %{x}: %{z:.3f}<extra></extra>'
        ))
        
        fig_corr.update_layout(
            plot_bgcolor='#0a0a0a',
            paper_bgcolor='#0a0a0a',
            font=dict(family='Helvetica Neue, Arial', size=11, color='#e5e5e5'),
            height=500,
            xaxis=dict(showgrid=False, color='#999999'),
            yaxis=dict(showgrid=False, color='#999999'),
            annotations=annotations
        )
        
        st.plotly_chart(fig_corr, use_container_width=True, key="corr")
        
        if len(ativos_no_portfolio) > 0:
            st.markdown("**Assets in portfolio:**")
            pesos_dict = dict(zip(validos, portfolio['pesos']))
            for ticker in ativos_no_portfolio:
                peso = pesos_dict[ticker]
                st.markdown(f"- {ativos_disponiveis[ticker]}: {peso:.1%}")
    
    with tab3:
        st.subheader("Historical Performance")
        
        st.info("""
        **Base 100 normalization:**
        - All assets start at 100 on the first day
        - Values show percentage performance relative to starting point
        - Example: 230 = +130% return, 50 = -50% loss
        - Allows comparison of assets with different price levels
        """)
        
        prices_norm = (prices / prices.iloc[0]) * 100
        
        fig_perf = go.Figure()
        
        for ticker in validos:
            if ticker in ativos_no_portfolio:
                width = 2.5
                opacity = 1.0
            else:
                width = 1.0
                opacity = 0.5
            
            fig_perf.add_trace(go.Scatter(
                x=prices_norm.index,
                y=prices_norm[ticker],
                mode='lines',
                name=ativos_disponiveis[ticker],
                line=dict(width=width),
                opacity=opacity
            ))
        
        fig_perf.update_layout(
            plot_bgcolor='#0a0a0a',
            paper_bgcolor='#0a0a0a',
            font=dict(family='Helvetica Neue, Arial', size=11, color='#e5e5e5'),
            xaxis=dict(showgrid=True, gridcolor='#333333', gridwidth=0.5, color='#999999', zerolinecolor='#333333'),
            yaxis=dict(showgrid=True, gridcolor='#333333', gridwidth=0.5, color='#999999', zerolinecolor='#333333'),
            xaxis_title="Date",
            yaxis_title="Normalized Price (Base 100)",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(26, 26, 26, 0.8)',
                bordercolor='#333333',
                borderwidth=1,
                font=dict(color='#e5e5e5')
            )
        )
        
        st.plotly_chart(fig_perf, use_container_width=True, key="perf")
        
        st.markdown("---")
        
        st.markdown("### Historical Price (BRL)")
        
        st.info("**Absolute prices in Brazilian Reais (BRL).** Shows actual trading prices without normalization.")
        
        fig_perf_brl = go.Figure()
        
        for ticker in validos:
            if ticker in ativos_no_portfolio:
                width = 2.5
                opacity = 1.0
            else:
                width = 1.0
                opacity = 0.5
            
            fig_perf_brl.add_trace(go.Scatter(
                x=prices.index,
                y=prices[ticker],
                mode='lines',
                name=ativos_disponiveis[ticker],
                line=dict(width=width),
                opacity=opacity
            ))
        
        fig_perf_brl.update_layout(
            plot_bgcolor='#0a0a0a',
            paper_bgcolor='#0a0a0a',
            font=dict(family='Helvetica Neue, Arial', size=11, color='#e5e5e5'),
            xaxis=dict(showgrid=True, gridcolor='#333333', gridwidth=0.5, color='#999999', zerolinecolor='#333333'),
            yaxis=dict(showgrid=True, gridcolor='#333333', gridwidth=0.5, color='#999999', zerolinecolor='#333333'),
            xaxis_title="Date",
            yaxis_title="Price (BRL)",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(26, 26, 26, 0.8)',
                bordercolor='#333333',
                borderwidth=1,
                font=dict(color='#e5e5e5')
            )
        )
        
        st.plotly_chart(fig_perf_brl, use_container_width=True, key="perf_brl")

elif processar:
    st.warning("Select at least 2 assets")
else:
    st.info("Configure parameters and click 'Optimize Portfolio'")

st.markdown("---")
st.caption("Data: Yahoo Finance | Cache enabled" if usar_cache else "Data: Yahoo Finance")