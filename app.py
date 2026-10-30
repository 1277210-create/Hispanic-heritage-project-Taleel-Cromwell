import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import io
import time
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xlsxwriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hispanic Heritage Historical Data Explorer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for printer mode & custom UI styling
st.markdown("""
    <style>
    @media print {
        .stApp { background-color: white !important; color: black !important; }
        .no-print, header, footer, .stSidebar, .stButton { display: none !important; }
        .main .block-container { max-width: 100% !important; padding: 0 !important; }
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1f77b4;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .status-badge {
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
    }
    .status-unmodified { background-color: #e3f2fd; color: #0d47a1; }
    .status-modified { background-color: #fff3e0; color: #e65100; }
    </style>
""", unsafe_allow_scope=True)

# -----------------------------------------------------------------------------
# 2. CONSTANTS & METADATA MAPPINGS
# -----------------------------------------------------------------------------
COUNTRY_MAPPING = {
    "NI": {"name": "Nicaragua", "flag": "🇳🇮", "note": "Primary Focus Country"},
    "MX": {"name": "Mexico", "flag": "🇲🇽", "note": "Latin American Peer"},
    "BR": {"name": "Brazil", "flag": "🇧🇷", "note": "Latin American Regional Benchmark"},
    "AR": {"name": "Argentina", "flag": "🇦🇷", "note": "Southern Cone Benchmark"},
    "CO": {"name": "Colombia", "flag": "🇨🇴", "note": "Andean Region Benchmark"},
    "CL": {"name": "Chile", "flag": "🇨🇱", "note": "High-Income Regional Peer"},
    "PE": {"name": "Peru", "flag": "🇵🇪", "note": "Andean Region Peer"},
    "VE": {"name": "Venezuela", "flag": "🇻🇪", "note": "Northern South America Peer"},
    "EC": {"name": "Ecuador", "flag": "🇪🇨", "note": "Andean Region Peer"},
    "UY": {"name": "Uruguay", "flag": "🇺🇾", "note": "Southern Cone Peer"}
}

INDICATOR_MAPPING = {
    "SP.DYN.LE00.IN": {
        "name": "Life Expectancy at Birth",
        "units": "years",
        "definition": "Number of years a newborn infant would live if prevailing mortality patterns at birth stay constant.",
        "exact_label": "Life expectancy at birth, total (years)",
        "source": "World Bank / UN Population Division"
    },
    "SL.UEM.TOTL.NE.ZS": {
        "name": "National-Estimate Unemployment",
        "units": "% of total labor force",
        "definition": "Share of the labor force without work but available and seeking employment (National Estimate).",
        "exact_label": "Unemployment, total (% of total labor force) (national estimate)",
        "source": "World Bank / ILOSTAT"
    },
    "NY.GDP.PCAP.CD": {
        "name": "GDP per Capita",
        "units": "current US$",
        "definition": "Gross domestic product divided by midyear population (economic output per person, NOT average personal income/wealth).",
        "exact_label": "GDP per capita (current US$)",
        "source": "World Bank national accounts data"
    },
    "SP.DYN.CBRT.IN": {
        "name": "Crude Birth Rate",
        "units": "per 1,000 people",
        "definition": "Annual number of live births occurring per 1,000 midyear population (NOT total annual birth count).",
        "exact_label": "Birth rate, crude (per 1,000 people)",
        "source": "World Bank / UN Population Division"
    },
    "SM.POP.NETM": {
        "name": "Net Migration",
        "units": "net headcount (immigrants - emigrants)",
        "definition": "Total net number of migrants (immigrants minus emigrants) over a five-year period or annual estimate (NOT total emigrants).",
        "exact_label": "Net migration",
        "source": "World Bank / UN Population Division"
    },
    "VC.IHR.PSRC.P5": {
        "name": "Intentional Homicide Rate",
        "units": "per 100,000 people",
        "definition": "Unlawful deaths purposefully inflicted on a person by another person, per 100,000 population.",
        "exact_label": "Intentional homicides (per 100,000 people)",
        "source": "UNODC / World Bank"
    },
    "FP.CPI.TOTL.ZG": {
        "name": "Consumer Price Inflation",
        "units": "annual %",
        "definition": "Annual percentage change in the cost to the average consumer of acquiring a basket of goods and services.",
        "exact_label": "Inflation, consumer prices (annual %)",
        "source": "IMF / World Bank"
    },
    "GC.DOD.TOTL.GD.ZS": {
        "name": "Central Government Debt",
        "units": "% of GDP",
        "definition": "Gross liabilities of central government including debt securities and loans, expressed as a share of GDP.",
        "exact_label": "Central government debt, total (% of GDP)",
        "source": "IMF / World Bank"
    },
    "FI.RES.TOTL.CD":