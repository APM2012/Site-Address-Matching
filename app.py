"""
🎯 Site Address Matching Dashboard
-----------------------------------
A beautiful, simple-to-use cascading matching pipeline.
Upload your addresses, match them instantly, download results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import re
import os
from io import BytesIO
import time

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="Site Address Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - Beautiful Modern Design
# ============================================================================
st.markdown("""
<style>
    /* Clean White Background with Cherry Red Accents */
    .stApp {
        background: #FFFFFF;
        background-attachment: fixed;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Full page floating pharma background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100vw;
        height: 100vh;
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Ctext x='20' y='50' font-size='38' opacity='0.18'%3E💊%3C/text%3E%3Ctext x='130' y='110' font-size='38' opacity='0.15'%3E🧬%3C/text%3E%3Ctext x='40' y='180' font-size='38' opacity='0.16'%3E🔬%3C/text%3E%3Ctext x='160' y='200' font-size='38' opacity='0.15'%3E🧪%3C/text%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 220px 220px;
        pointer-events: none;
        z-index: 0;
        animation: floatBg 60s linear infinite;
    }
    
    @keyframes floatBg {
        0% { background-position: 0px 0px; }
        100% { background-position: 220px 220px; }
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100vw;
        height: 100vh;
        background-image: 
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='280' height='280'%3E%3Ctext x='60' y='70' font-size='42' opacity='0.12'%3E🧪%3C/text%3E%3Ctext x='180' y='140' font-size='42' opacity='0.13'%3E💊%3C/text%3E%3Ctext x='40' y='220' font-size='42' opacity='0.11'%3E🧬%3C/text%3E%3Ctext x='200' y='260' font-size='42' opacity='0.12'%3E🔬%3C/text%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 280px 280px;
        pointer-events: none;
        z-index: 0;
        animation: floatBg2 80s linear infinite reverse;
    }
    
    @keyframes floatBg2 {
        0% { background-position: 0px 0px; }
        100% { background-position: 300px 300px; }
    }
    
    /* Ensure main content is visible */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main,
    section[data-testid="stSidebar"],
    .stMainBlockContainer,
    .block-container {
        position: relative;
        z-index: 1;
    }
    
    .main .block-container,
    .stMainBlockContainer {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Cards with wine red glow */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 30px rgba(139, 35, 50, 0.15), 0 0 40px rgba(139, 35, 50, 0.08);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(139, 35, 50, 0.15);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 40px rgba(139, 35, 50, 0.25), 0 0 50px rgba(139, 35, 50, 0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #7b1e2b;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #37474f;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers - Dark for cream bg */
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d2d 50%, #3d3d3d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-size: 1.2rem;
        color: #555555;
        margin-top: 1rem;
    }
    
    /* Upload area */
    .upload-area {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(139, 35, 50, 0.15);
        margin: 2rem 0;
        border: 2px dashed rgba(139, 35, 50, 0.4);
    }
    
    /* Progress section */
    .progress-section {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(139, 35, 50, 0.12);
        border: 1px solid rgba(139, 35, 50, 0.1);
    }
    
    /* Stage badges */
    .stage-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
    
    .stage-dd { background: #e8f5e9; color: #2e7d32; }
    .stage-longctms { background: #e3f2fd; color: #1565c0; }
    .stage-citeline { background: #fff3e0; color: #ef6c00; }
    .stage-shortctms { background: #fce4ec; color: #c2185b; }
    .stage-unmatched { background: #f5f5f5; color: #616161; }
    
    /* Results table */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Buttons - Wine Red / Cherry Red */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #8b2332 0%, #a52a3a 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 25px rgba(139, 35, 50, 0.5);
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px dashed rgba(92, 107, 192, 0.4);
        margin-top: 0.5rem;
    }
    
    /* Primary button styling - Wine Red */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8b2332 0%, #a52a3a 100%);
        border: none;
        box-shadow: 0 4px 15px rgba(139, 35, 50, 0.4);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 25px rgba(139, 35, 50, 0.6);
        transform: translateY(-2px);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Success/info boxes */
    .success-box {
        background: linear-gradient(135deg, #8b2332 0%, #a52a3a 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        color: #1a1a2e;
    }
    
    /* DEFAULT: Dark text for cream background */
    .stMarkdown p, .stMarkdown span, .stMarkdown h3, .stMarkdown h4,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span,
    .stAlert p, .stAlert span, .stAlert strong,
    [data-testid="stAlert"] p, [data-testid="stAlert"] span,
    div[data-baseweb="notification"] p,
    div[data-baseweb="notification"] span,
    label {
        color: #1a1a2e !important;
    }
    
    /* Dark text inside white card containers */
    div[style*="background: rgba(255, 255, 255"] h3,
    div[style*="background: rgba(255, 255, 255"] p,
    div[style*="background: rgba(255, 255, 255"] span {
        color: inherit !important;
    }
    
    /* Dark text ONLY inside white containers */
    .stFileUploader p, .stFileUploader span, .stFileUploader label,
    [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] label,
    .stDataFrame, .stDataFrame th, .stDataFrame td,
    [data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {
        color: #1a1a2e !important;
    }
    
    /* Expander header - dark for cream bg */
    [data-testid="stExpander"] summary span {
        color: #1a1a2e !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Expander styling - bigger and more prominent */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(139, 35, 50, 0.15);
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    [data-testid="stExpander"] summary {
        padding: 1rem 1.5rem;
    }
    
    /* Expander content (dataframe inside) - give it white background */
    [data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    [data-testid="stExpander"] > div[data-testid="stExpanderDetails"] p,
    [data-testid="stExpander"] > div[data-testid="stExpanderDetails"] span {
        color: #1a1a2e !important;
    }
    
    /* Status messages - bigger and bolder */
    .status-text {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #1a1a2e !important;
        margin: 0.5rem 0;
    }
    
    /* Success/Error/Warning alerts - bigger text */
    [data-testid="stAlert"] {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        padding: 1rem 1.25rem !important;
    }
    
    [data-testid="stAlert"] p, [data-testid="stAlert"] span {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }
    
    /* Progress bar container */
    [data-testid="stProgress"] {
        margin: 0.5rem 0 1rem 0;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        min-height: 300px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURATION
# ============================================================================
TOPK = 100
THRESH_STRONG = 0.70
THRESH_REVIEW = 0.55
BATCH_SIZE = 256
MIN_NAME_SIM = 0.30
MIN_NAME_SIM_INCOMPLETE = 0.55

# ============================================================================
# HELPER FUNCTIONS (from original pipeline)
# ============================================================================

def classify_source_type(platinum_id: str) -> str:
    """Classify the source type based on DWH_SOURCE_KEY_PLATINUM pattern."""
    if not platinum_id:
        return "UNKNOWN"
    pid = str(platinum_id).upper().strip()
    if pid.startswith("DD"):
        return "DD"
    elif pid.startswith("CITELN-"):
        return "CITELINE"
    elif pid.startswith("CTMS-"):
        suffix = pid[5:]
        if suffix.isdigit():
            return "SHORT_CTMS"
        else:
            return "LONG_CTMS"
    else:
        return "OTHER"

def clean_series(s: pd.Series) -> pd.Series:
    return s.fillna("").astype(str).str.strip().str.lower()

def normalize_abbrev(s: pd.Series) -> pd.Series:
    subs = {
        r"\bst\b": "street", r"\bstr\b": "street",
        r"\bave\b": "avenue", r"\bav\b": "avenue",
        r"\brd\b": "road",
        r"\bblvd\b": "boulevard", r"\bboul\b": "boulevard",
        r"\bdr\b": "drive", r"\bdrv\b": "drive",
        r"\bln\b": "lane",
        r"\bct\b": "court", r"\bcrt\b": "court",
        r"\bcir\b": "circle",
        r"\bpl\b": "place",
        r"\bpkwy\b": "parkway", r"\bpky\b": "parkway",
        r"\bhwy\b": "highway",
        r"\bsq\b": "square",
        r"\bter\b": "terrace",
        r"\btrl\b": "trail",
        r"\bste\b": "suite",
        r"\bfl\b": "floor", r"\bflr\b": "floor",
        r"\bapt\b": "apartment",
        r"\bbldg\b": "building",
        r"\bn\b": "north", r"\bs\b": "south",
        r"\be\b": "east", r"\bw\b": "west",
        r"\bne\b": "northeast", r"\bnw\b": "northwest",
        r"\bse\b": "southeast", r"\bsw\b": "southwest",
    }
    out = s.str.lower()
    for k, v in subs.items():
        out = out.str.replace(k, v, regex=True)
    return out.str.replace(r"\s+", " ", regex=True).str.strip()

def norm_space(x: str) -> str:
    if x is None:
        return ""
    return re.sub(r"\s+", " ", str(x).strip().lower())

def safe_ratio(a: str, b: str) -> float:
    from rapidfuzz.fuzz import partial_ratio, token_set_ratio
    a = (a or "").strip()
    b = (b or "").strip()
    if not a or not b:
        return 0.0
    return max(partial_ratio(a, b), token_set_ratio(a, b)) / 100.0

def extract_street_number(addr: str) -> str:
    if not addr:
        return ""
    addr = norm_space(addr)
    match = re.match(r'^(\d+)', addr)
    if match:
        return match.group(1)
    nums = re.findall(r'\b(\d+)\b', addr)
    return nums[0] if nums else ""

def _is_valid_partial_number_match(num1: str, num2: str) -> bool:
    if not num1 or not num2:
        return False
    if len(num1) <= len(num2):
        shorter, longer = num1, num2
    else:
        shorter, longer = num2, num1
    if not longer.startswith(shorter):
        return False
    if len(shorter) == len(longer):
        return True
    next_char = longer[len(shorter)]
    return not next_char.isdigit()

def extract_suite(addr: str) -> str:
    if not addr:
        return ""
    addr_lower = addr.lower()
    suite_patterns = [
        r'\b(?:suite|ste)\s*#?\s*([a-z]?\d+[a-z]?)\b',
        r'\b(?:unit|apt|apartment)\s*#?\s*([a-z]?\d+[a-z]?)\b',
        r'\b(?:room|rm)\s*#?\s*(\d+[a-z]?)\b',
        r'#\s*(\d+[a-z]?)\b',
    ]
    floor_patterns = [
        r'\b(?:floor|flr|fl)\s*#?\s*(\d+)\b',
        r'\b(\d+)(?:st|nd|rd|th)?\s*(?:floor|flr|fl)\b',
    ]
    for pattern in suite_patterns:
        match = re.search(pattern, addr_lower)
        if match:
            return f"suite:{match.group(1)}"
    for pattern in floor_patterns:
        match = re.search(pattern, addr_lower)
        if match:
            return f"floor:{match.group(1)}"
    return ""

def compare_suite_floor(q_unit: str, c_unit: str) -> float:
    if not q_unit and not c_unit:
        return 1.0
    if not q_unit or not c_unit:
        return 0.7
    q_type, q_num = (q_unit.split(':', 1) + [''])[:2] if ':' in q_unit else ('raw', q_unit)
    c_type, c_num = (c_unit.split(':', 1) + [''])[:2] if ':' in c_unit else ('raw', c_unit)
    if q_type == c_type:
        return 1.0 if q_num == c_num else 0.0
    return 0.5

def remove_street_number(addr: str) -> str:
    if not addr:
        return ""
    addr = addr.strip()
    cleaned = re.sub(r'^\d+\s+', '', addr)
    return cleaned.strip()

def address_component_score(q_addr: str, c_addr: str) -> dict:
    q_addr_n = norm_space(q_addr)
    c_addr_n = norm_space(c_addr)
    scores = {
        'num_score': 0.5, 'street_score': 0.5, 'unit_score': 0.5,
        'overall': 0.5, 'is_incomplete': False, 'incomplete_reason': ''
    }
    if not q_addr_n or not c_addr_n:
        return scores
    q_num = extract_street_number(q_addr_n)
    c_num = extract_street_number(c_addr_n)
    num_missing_one_side = bool(q_num) != bool(c_num)
    if q_num and c_num:
        if q_num == c_num:
            scores['num_score'] = 1.0
        elif _is_valid_partial_number_match(q_num, c_num):
            scores['num_score'] = 0.85
        else:
            scores['num_score'] = 0.0
    elif num_missing_one_side:
        scores['num_score'] = 0.5
        scores['is_incomplete'] = True
        scores['incomplete_reason'] = 'street_number_missing'
    q_street = remove_street_number(q_addr_n)
    c_street = remove_street_number(c_addr_n)
    if q_street and c_street:
        street_fuzzy = safe_ratio(q_street, c_street)
        scores['street_score'] = street_fuzzy
    q_unit = extract_suite(q_addr_n)
    c_unit = extract_suite(c_addr_n)
    scores['unit_score'] = compare_suite_floor(q_unit, c_unit)
    if scores['unit_score'] == 0.7:
        scores['is_incomplete'] = True
        if scores['incomplete_reason']:
            scores['incomplete_reason'] += '+suite_missing'
        else:
            scores['incomplete_reason'] = 'suite_missing'
    scores['overall'] = (
        0.40 * scores['num_score'] +
        0.45 * scores['street_score'] +
        0.15 * scores['unit_score']
    )
    return scores

def name_similarity(name1: str, name2: str, strict_mode: bool = False) -> float:
    from rapidfuzz.fuzz import ratio, token_sort_ratio, token_set_ratio
    if not name1 or not name2:
        return 0.0
    n1 = norm_space(name1)
    n2 = norm_space(name2)
    name_abbrevs = {
        r"\bst\b": "saint", r"\bmt\b": "mount", r"\bdr\b": "doctor",
        r"\bmed\b": "medical", r"\bhosp\b": "hospital", r"\buniv\b": "university",
        r"\bctrs?\b": "center", r"\bcentre\b": "center", r"\bhealthcare\b": "health care",
        r"\bhlth\b": "health", r"\bassoc\b": "associates", r"\bcommun\b": "community",
        r"\bcomm\b": "community", r"\bnatl\b": "national", r"\bintl\b": "international",
    }
    for pattern, replacement in name_abbrevs.items():
        n1 = re.sub(pattern, replacement, n1)
        n2 = re.sub(pattern, replacement, n2)
    generic_terms = {
        'the', 'of', 'and', 'a', 'an', 'inc', 'llc', 'corp', 
        'corporation', 'company', 'co', 'ltd', 'pc', 'pllc', 'pa', 'md',
        'medical', 'center', 'centre', 'hospital', 'clinic', 'health',
        'healthcare', 'care', 'cancer', 'oncology', 'hematology', 
        'research', 'institute', 'foundation', 'group', 'associates',
        'physicians', 'doctors', 'specialists', 'practice', 'services',
        'treatment', 'therapy', 'radiation', 'surgical', 'surgery',
        'women', 'womens', 'mens', 'men', 'pediatric', 'adult',
        'community', 'regional', 'university', 'academic', 'teaching',
        'national', 'memorial', 'general', 'specialty', 'integrated',
        'comprehensive', 'advanced', 'professional', 'network',
    }
    tokens1 = [t for t in n1.split() if t not in generic_terms and len(t) > 1]
    tokens2 = [t for t in n2.split() if t not in generic_terms and len(t) > 1]
    if not tokens1 and not tokens2:
        base_score = safe_ratio(n1, n2)
        return base_score * 0.6 if strict_mode else base_score
    if not tokens1 or not tokens2:
        return 0.2 if strict_mode else 0.3
    unique1 = " ".join(tokens1)
    unique2 = " ".join(tokens2)
    has_overlap = False
    overlap_count = 0
    for t1 in tokens1:
        for t2 in tokens2:
            if ratio(t1, t2) > 80:
                has_overlap = True
                overlap_count += 1
                break
    set1 = set(tokens1)
    set2 = set(tokens2)
    intersection = set1 & set2
    union = set1 | set2
    jaccard = len(intersection) / len(union) if union else 0.0
    fuzzy_sort = token_sort_ratio(unique1, unique2) / 100.0
    fuzzy_set = token_set_ratio(unique1, unique2) / 100.0
    fuzzy = max(fuzzy_sort, fuzzy_set)
    score = max(jaccard, fuzzy)
    if strict_mode:
        if not has_overlap:
            score = min(score, 0.30)
        elif overlap_count < min(len(tokens1), len(tokens2)) * 0.5:
            score = score * 0.8
    else:
        if not has_overlap:
            score = min(score, 0.45)
    return score

# ============================================================================
# CACHED RESOURCES
# ============================================================================

@st.cache_resource(show_spinner=False)
def load_model():
    """Load the embedding model (cached)"""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("arinze/address-match-abp-v5")

@st.cache_data(show_spinner=False, ttl=3600)  # Cache for 1 hour
def load_platinum_data(username: str, oauth_token: str):
    """Load Platinum data from Snowflake (cached)"""
    from lib.Snowflake import open_connection
    
    database = os.getenv("SNOWFLAKE_DATABASE", "EXAMPLE_DATA")
    query = f"""
    SELECT dds.DWH_SOURCE_KEY_PLATINUM,
           dds.SITE_PLATINUM_NAME,
           dds.SITE_PLATINUM_STREET,
           dds.SITE_PLATINUM_POSTAL_CODE,
           dds.SITE_PLATINUM_CITY,
           dds.SITE_PLATINUM_STATE_CODE,
           dds.SITE_PLATINUM_LATITUDE,
           dds.SITE_PLATINUM_LONGITUDE
    FROM {database}.MART_DATA.DM_D_SITE dds
    WHERE dds.SITE_PLATINUM_COUNTRY_NAME = 'United States'
    ORDER BY dds.SITE_PLATINUM_STATE_CODE, dds.SITE_PLATINUM_CITY, dds.SITE_PLATINUM_STREET
    """
    
    try:
        engine = open_connection(oauth_token, username)
        raw_conn = engine.raw_connection()
        
        try:
            platinum = pd.read_sql(query, con=raw_conn)
        finally:
            raw_conn.close()
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Snowflake: {str(e)}")
    
    # Clean data
    platinum['SITE_PLATINUM_STREET_RAW'] = clean_series(platinum['SITE_PLATINUM_STREET'])
    platinum['SITE_PLATINUM_NAME'] = normalize_abbrev(clean_series(platinum['SITE_PLATINUM_NAME']))
    platinum['SITE_PLATINUM_STREET'] = normalize_abbrev(platinum['SITE_PLATINUM_STREET_RAW'])
    platinum['SITE_PLATINUM_CITY'] = clean_series(platinum['SITE_PLATINUM_CITY'])
    platinum['SITE_PLATINUM_STATE_CODE'] = clean_series(platinum['SITE_PLATINUM_STATE_CODE'])
    platinum['SITE_PLATINUM_POSTAL_CODE'] = clean_series(platinum['SITE_PLATINUM_POSTAL_CODE'])
    platinum['combined'] = (
        platinum['SITE_PLATINUM_NAME'] + ", " +
        platinum['SITE_PLATINUM_STREET'] + ", " +
        platinum['SITE_PLATINUM_CITY'] + ", " +
        platinum['SITE_PLATINUM_STATE_CODE']
    )
    platinum['SOURCE_TYPE'] = platinum['DWH_SOURCE_KEY_PLATINUM'].apply(classify_source_type)
    
    return platinum

# ============================================================================
# MATCHING FUNCTIONS
# ============================================================================

def match_against_platinum(
    iqvia_subset: pd.DataFrame,
    iqvia_embeddings: np.ndarray,
    platinum_subset: pd.DataFrame,
    source_type_name: str,
    model,
    progress_callback=None
) -> pd.DataFrame:
    """Match IQVIA records against a specific platinum subset."""
    import faiss
    
    if len(platinum_subset) == 0:
        return pd.DataFrame()
    
    # Encode platinum subset
    platinum_emb = model.encode(
        platinum_subset['combined'].tolist(),
        convert_to_numpy=True,
        batch_size=BATCH_SIZE,
        normalize_embeddings=False,
        show_progress_bar=False
    )
    faiss.normalize_L2(platinum_emb)
    
    # Build FAISS index
    index = faiss.IndexFlatIP(platinum_emb.shape[1])
    index.add(platinum_emb)
    
    results = []
    total_rows = len(iqvia_subset)
    
    for start in range(0, len(iqvia_subset), BATCH_SIZE):
        end = min(start + BATCH_SIZE, len(iqvia_subset))
        batch_indices = list(range(start, end))
        q_vecs = iqvia_embeddings[batch_indices]
        
        sims, idxs = index.search(q_vecs, TOPK)
        
        for i, (iq_idx, iq_row) in enumerate(zip(batch_indices, iqvia_subset.iloc[start:end].itertuples())):
            q_name = iq_row.name
            q_addr = iq_row.address
            q_city = iq_row.city
            q_state = iq_row.state
            q_zip = iq_row.postal_code
            q_raw = iq_row.address_raw
            
            candidates = []
            
            for rank, p_idx in enumerate(idxs[i]):
                vec_sim = float(sims[i][rank])
                if vec_sim < 0.30:
                    continue
                
                crow = platinum_subset.iloc[p_idx]
                
                if norm_space(q_state) != norm_space(crow['SITE_PLATINUM_STATE_CODE']):
                    continue
                
                addr_comp = address_component_score(q_raw, crow['SITE_PLATINUM_STREET_RAW'])
                addr_sim = addr_comp['overall']
                num_sim = addr_comp['num_score']
                street_sim = addr_comp['street_score']
                unit_sim = addr_comp['unit_score']
                is_incomplete = addr_comp['is_incomplete']
                incomplete_reason = addr_comp['incomplete_reason']
                
                name_sim = name_similarity(q_name, crow['SITE_PLATINUM_NAME'], strict_mode=is_incomplete)
                city_sim = 1.0 if norm_space(q_city) == norm_space(crow['SITE_PLATINUM_CITY']) else 0.3
                
                if num_sim == 0.0 or unit_sim == 0.0 or street_sim < 0.35:
                    continue
                
                suite_missing = (incomplete_reason == 'suite_missing')
                street_num_missing = ('street_number_missing' in incomplete_reason)
                
                if street_num_missing:
                    if name_sim < 0.60 or street_sim < 0.55 or city_sim < 0.5:
                        continue
                    final_score = (0.10 * vec_sim + 0.15 * num_sim + 0.40 * name_sim +
                                   0.20 * street_sim + 0.10 * city_sim + 0.05 * unit_sim)
                elif suite_missing:
                    if name_sim < MIN_NAME_SIM_INCOMPLETE:
                        continue
                    final_score = (0.15 * vec_sim + 0.30 * num_sim + 0.25 * name_sim +
                                   0.15 * street_sim + 0.10 * city_sim + 0.05 * unit_sim)
                else:
                    if name_sim < MIN_NAME_SIM:
                        continue
                    final_score = (0.20 * vec_sim + 0.30 * num_sim + 0.15 * name_sim +
                                   0.15 * street_sim + 0.10 * city_sim + 0.10 * unit_sim)
                
                candidates.append({
                    'score': final_score, 'row': crow, 'vec_sim': vec_sim,
                    'addr_sim': addr_sim, 'name_sim': name_sim, 'city_sim': city_sim,
                    'num_sim': num_sim, 'street_sim': street_sim, 'unit_sim': unit_sim,
                    'is_incomplete': is_incomplete, 'incomplete_reason': incomplete_reason
                })
            
            candidates.sort(key=lambda x: x['score'], reverse=True)
            
            if candidates:
                best_cand = candidates[0]
                best_score = best_cand['score']
                best_row = best_cand['row']
                
                if best_score >= THRESH_REVIEW:
                    match_reason = "MATCHED_STRONG" if best_score >= THRESH_STRONG else "REVIEW_REQUIRED"
                    if best_cand['is_incomplete']:
                        match_reason += "_INCOMPLETE"
                    
                    results.append({
                        'iqvia_original_index': iq_row.Index,
                        'uploaded_id': iq_row.iqvia_site_org_id if hasattr(iq_row, 'iqvia_site_org_id') else iq_idx,
                        'uploaded_address_combined': iq_row.combined,
                        'matched_platinum_id': best_row['DWH_SOURCE_KEY_PLATINUM'],
                        'matched_platinum_address': best_row['combined'],
                        'match_score': best_score,
                        'match_reason': match_reason,
                        'source_type': source_type_name,
                        'vec_sim': best_cand['vec_sim'],
                        'name_sim': best_cand['name_sim'],
                        'addr_sim': best_cand['addr_sim']
                    })
        
        if progress_callback:
            progress_callback(end / total_rows)
    
    return pd.DataFrame(results)

def run_cascading_pipeline(iqvia: pd.DataFrame, platinum: pd.DataFrame, model, progress_container):
    """Run the full cascading matching pipeline."""
    import faiss
    
    # Split platinum by source type
    platinum_dd = platinum[platinum['SOURCE_TYPE'] == 'DD'].reset_index(drop=True)
    platinum_long_ctms = platinum[platinum['SOURCE_TYPE'] == 'LONG_CTMS'].reset_index(drop=True)
    platinum_citeline = platinum[platinum['SOURCE_TYPE'] == 'CITELINE'].reset_index(drop=True)
    platinum_short_ctms = platinum[platinum['SOURCE_TYPE'] == 'SHORT_CTMS'].reset_index(drop=True)
    
    # Encode IQVIA
    with progress_container:
        st.markdown('<p class="status-text">🔄 Encoding your addresses...</p>', unsafe_allow_html=True)
        progress_bar = st.progress(0)
    
    iqvia_emb = model.encode(
        iqvia['combined'].tolist(),
        convert_to_numpy=True,
        batch_size=BATCH_SIZE,
        normalize_embeddings=False,
        show_progress_bar=False
    )
    faiss.normalize_L2(iqvia_emb)
    
    with progress_container:
        progress_bar.progress(100)
        st.success("✅ Encoding complete!")
    
    all_matches = []
    remaining_iqvia = iqvia.copy()
    remaining_iqvia_emb = iqvia_emb.copy()
    
    stages = [
        ("DD", platinum_dd, "🟢"),
        ("LONG_CTMS", platinum_long_ctms, "🔵"),
        ("CITELINE", platinum_citeline, "🟠"),
        ("SHORT_CTMS", platinum_short_ctms, "🔴")
    ]
    
    stage_results = {}
    
    for stage_name, plat_subset, emoji in stages:
        with progress_container:
            st.markdown(f'<p class="status-text">{emoji} Matching against {stage_name}...</p>', unsafe_allow_html=True)
            stage_progress = st.progress(0)
        
        def update_progress(pct):
            stage_progress.progress(int(pct * 100))
        
        matches = match_against_platinum(
            remaining_iqvia, remaining_iqvia_emb,
            plat_subset, stage_name, model, update_progress
        )
        
        stage_results[stage_name] = len(matches)
        
        if len(matches) > 0:
            all_matches.append(matches)
            matched_indices = matches['iqvia_original_index'].tolist()
            remaining_mask = ~remaining_iqvia.index.isin(matched_indices)
            remaining_iqvia = remaining_iqvia[remaining_mask].reset_index(drop=True)
            
            # Rebuild embeddings for remaining
            original_indices = iqvia.index.isin(remaining_iqvia['combined'].index) if 'combined' in remaining_iqvia.columns else list(range(len(remaining_iqvia)))
            remaining_indices = [i for i, row in enumerate(iqvia.itertuples()) if row.combined in remaining_iqvia['combined'].values]
            if len(remaining_indices) > 0:
                remaining_iqvia_emb = iqvia_emb[remaining_indices]
            else:
                remaining_iqvia_emb = np.array([])
        
        with progress_container:
            st.success(f"✅ {stage_name}: Found {len(matches)} matches")
    
    # Combine results
    if all_matches:
        combined_matches = pd.concat(all_matches, ignore_index=True)
    else:
        combined_matches = pd.DataFrame()
    
    # Add unmatched records
    unmatched_df = pd.DataFrame({
        'iqvia_original_index': range(len(remaining_iqvia)),
        'uploaded_id': remaining_iqvia['iqvia_site_org_id'] if 'iqvia_site_org_id' in remaining_iqvia.columns else range(len(remaining_iqvia)),
        'uploaded_address_combined': remaining_iqvia['combined'],
        'matched_platinum_id': None,
        'matched_platinum_address': "",
        'match_score': 0.0,
        'match_reason': "NO_MATCH",
        'source_type': "NONE",
        'vec_sim': 0.0,
        'name_sim': 0.0,
        'addr_sim': 0.0
    })
    
    stage_results['UNMATCHED'] = len(remaining_iqvia)
    
    final_output = pd.concat([combined_matches, unmatched_df], ignore_index=True)
    
    return final_output, stage_results

# ============================================================================
# LOGIN PAGE
# ============================================================================

def show_login_page():
    """Display the login page for Snowflake authentication"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🔗 Site Address Matcher</h1>
        <p>Sign in with your configured Snowflake credentials to continue</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered login form
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 2rem; 
             box-shadow: 0 4px 20px rgba(139, 35, 50, 0.15); border: 1px solid rgba(139, 35, 50, 0.1);">
            <h3 style="color: #1a1a2e; text-align: center; margin-bottom: 1.5rem;">
                🔐 Snowflake Login
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="e.g., DEMO_USER",
                help="Your data warehouse network username"
            )
            password = st.text_input(
                "Password", 
                type="password",
                placeholder="Your network password",
                help="Your configured identity provider password"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("🚀 Sign In", use_container_width=True, type="primary")
            
            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    with st.spinner("Authenticating..."):
                        try:
                            from lib.Snowflake import oauth_token_request
                            # Test authentication
                            token = oauth_token_request(username.upper(), password)
                            
                            # Store credentials in session state
                            st.session_state.authenticated = True
                            st.session_state.username = username.upper()
                            st.session_state.oauth_token = token
                            
                            st.success("✅ Authentication successful!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"""
                            ### ⚠️ Authentication Failed
                            
                            Please check your credentials and try again.
                            
                            *Error: {str(e)}*
                            """)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; color: #666; font-size: 0.85rem;">
            <p>🔒 Your credentials are used only for this session and are not stored permanently.</p>
            <p>You need access to the configured example database.</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Check authentication
    if not st.session_state.get('authenticated', False):
        show_login_page()
        return
    
    # Header with simple emoji icon and logout button
    col_header, col_logout = st.columns([4, 1])
    
    with col_header:
        st.markdown("""
        <div class="main-header">
            <h1>🔗 Site Address Matcher</h1>
            <p>Upload your addresses, match them instantly, download results</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session state
            for key in ['authenticated', 'username', 'password', 'oauth_token', 'results', 'stage_results', 'processed']:
                if key in st.session_state:
                    del st.session_state[key]
            st.cache_data.clear()
            st.rerun()
    
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'stage_results' not in st.session_state:
        st.session_state.stage_results = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    # Upload Section
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(10px); 
                        border-radius: 20px; padding: 2.5rem; margin-bottom: 1.5rem;
                        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15); text-align: center;
                        border: 1px solid rgba(200, 200, 200, 0.3);">
                <div style="margin-bottom: 1rem;">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 7C3 5.89543 3.89543 5 5 5H9.58579C9.851 5 10.1054 5.10536 10.2929 5.29289L12 7H19C20.1046 7 21 7.89543 21 9V17C21 18.1046 20.1046 19 19 19H5C3.89543 19 3 18.1046 3 17V7Z" fill="#5c6bc0"/>
                        <path d="M3 7C3 5.89543 3.89543 5 5 5H9.58579C9.851 5 10.1054 5.10536 10.2929 5.29289L12 7H19C20.1046 7 21 7.89543 21 9V10H3V7Z" fill="#7986cb"/>
                    </svg>
                </div>
                <h3 style="margin-bottom: 0.5rem; color: #1a1a2e !important; font-size: 1.5rem;">Upload Your Data</h3>
                <p style="color: #546e7a !important; margin-bottom: 0;">
                    Click the button below to upload your CSV file
                </p>
                <div style="display: flex; align-items: center; justify-content: center; margin: 1rem 0;">
                    <div style="flex: 1; height: 1px; background: #e0e0e0;"></div>
                    <span style="padding: 0 1rem; color: #9e9e9e; font-size: 0.85rem;">OR drag and drop</span>
                    <div style="flex: 1; height: 1px; background: #e0e0e0;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Drag and drop your CSV file here",
                type=['csv'],
                help="Your CSV should have columns: address, site_business_name, city, state",
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                # Show preview
                iqvia = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded **{len(iqvia):,}** records")
                
                with st.expander("📋 Preview uploaded data", expanded=True):
                    st.dataframe(iqvia.head(20), use_container_width=True, height=350)
    
    # Process Button
    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            process_btn = st.button("🚀 **Start Matching**", use_container_width=True, type="primary")
        
        if process_btn:
            # Reset uploaded file position
            uploaded_file.seek(0)
            iqvia = pd.read_csv(uploaded_file)
            
            # Clean IQVIA data
            iqvia['address_raw'] = clean_series(iqvia['address'])
            iqvia['name'] = normalize_abbrev(clean_series(iqvia['site_business_name']))
            iqvia['address'] = normalize_abbrev(iqvia['address_raw'])
            iqvia['city'] = clean_series(iqvia['city'])
            iqvia['state'] = clean_series(iqvia['state'])
            
            if 'postal_code' not in iqvia.columns:
                for cand in ('zip', 'zipcode', 'zip_code', 'postal'):
                    if cand in iqvia.columns:
                        iqvia['postal_code'] = clean_series(iqvia[cand])
                        break
            if 'postal_code' not in iqvia.columns:
                iqvia['postal_code'] = ""
            
            iqvia['combined'] = (
                iqvia['name'] + ", " +
                iqvia['address'] + ", " +
                iqvia['city'] + ", " +
                iqvia['state']
            )
            
            # Progress container
            progress_container = st.container()
            
            try:
                with progress_container:
                    st.markdown('<p class="status-text">📚 Connecting to Snowflake database...</p>', unsafe_allow_html=True)
                platinum = load_platinum_data(
                    st.session_state.username,
                    st.session_state.oauth_token
                )
                with progress_container:
                    st.success(f"✅ Loaded {len(platinum):,} Platinum records")
            except Exception as e:
                st.error(f"""
                ### ⚠️ Connection Error
                
                **Unable to connect to Snowflake database.**
                
                Your session may have expired. Please logout and login again.
                
                **How to fix:**
                1. Click the "Logout" button
                2. Login again with your credentials
                3. Restart the matching process
                
                *Technical details: {str(e)}*
                """)
                st.stop()
            
            try:
                with progress_container:
                    st.markdown('<p class="status-text">🧠 Loading model...</p>', unsafe_allow_html=True)
                model = load_model()
                with progress_container:
                    st.success("✅ Model loaded!")
            except Exception as e:
                st.error(f"""
                ### ⚠️ Model Loading Error
                
                **Unable to load the embedding model.**
                
                *Technical details: {str(e)}*
                """)
                st.stop()
            
            # Run pipeline
            results, stage_results = run_cascading_pipeline(iqvia, platinum, model, progress_container)
            
            st.session_state.results = results
            st.session_state.stage_results = stage_results
            st.session_state.processed = True
            st.session_state.total_input = len(iqvia)
            
            st.rerun()
    
    # Results Section
    if st.session_state.processed and st.session_state.results is not None:
        results = st.session_state.results
        stage_results = st.session_state.stage_results
        total = st.session_state.total_input
        
        st.markdown("---")
        st.markdown("## 📊 Results")
        
        # Stats Cards
        total_matched = sum(v for k, v in stage_results.items() if k != 'UNMATCHED')
        unmatched = stage_results.get('UNMATCHED', 0)
        match_rate = (total_matched / total * 100) if total > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{total:,}</p>
                <p class="metric-label">Total Records</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value" style="color: #4caf50;">{total_matched:,}</p>
                <p class="metric-label">Matched</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value" style="color: #f44336;">{unmatched:,}</p>
                <p class="metric-label">Unmatched</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value" style="color: #2196f3;">{match_rate:.1f}%</p>
                <p class="metric-label">Match Rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Source breakdown
        st.markdown("### 📈 Matches by Source")
        
        cols = st.columns(5)
        source_info = [
            ("DD", stage_results.get('DD', 0), "🟢", "#4caf50"),
            ("Long CTMS", stage_results.get('LONG_CTMS', 0), "🔵", "#2196f3"),
            ("Citeline", stage_results.get('CITELINE', 0), "🟠", "#ff9800"),
            ("Short CTMS", stage_results.get('SHORT_CTMS', 0), "🔴", "#f44336"),
            ("Unmatched", stage_results.get('UNMATCHED', 0), "⚪", "#9e9e9e"),
        ]
        
        for i, (name, count, emoji, color) in enumerate(source_info):
            with cols[i]:
                pct = (count / total * 100) if total > 0 else 0
                st.metric(f"{emoji} {name}", f"{count:,}", f"{pct:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Results Table
        st.markdown("### 📋 Match Results")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_source = st.selectbox(
                "Filter by Source",
                ["All"] + list(stage_results.keys())
            )
        with col2:
            filter_status = st.selectbox(
                "Filter by Status",
                ["All", "MATCHED_STRONG", "REVIEW_REQUIRED", "NO_MATCH"]
            )
        with col3:
            min_score = st.slider("Minimum Score", 0.0, 1.0, 0.0)
        
        # Apply filters
        filtered = results.copy()
        if filter_source != "All":
            filtered = filtered[filtered['source_type'] == filter_source]
        if filter_status != "All":
            filtered = filtered[filtered['match_reason'].str.contains(filter_status, na=False)]
        filtered = filtered[filtered['match_score'] >= min_score]
        
        st.markdown(f"*Showing {len(filtered):,} of {len(results):,} records*")
        
        # Display table
        display_cols = ['uploaded_address_combined', 'matched_platinum_id', 
                       'matched_platinum_address', 'match_score', 'match_reason', 'source_type']
        st.dataframe(
            filtered[display_cols].rename(columns={
                'uploaded_address_combined': 'Uploaded Address',
                'matched_platinum_id': 'Matched ID',
                'matched_platinum_address': 'Matched Address',
                'match_score': 'Score',
                'match_reason': 'Status',
                'source_type': 'Source'
            }),
            use_container_width=True,
            height=400
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Download Section
        st.markdown("### 💾 Download Results")
        
        col1, col2, col3 = st.columns(3)
        
        # Full results
        output_df = results[[
            'uploaded_id', 'uploaded_address_combined', 'matched_platinum_id',
            'matched_platinum_address', 'match_score', 'match_reason', 'source_type'
        ]].copy()
        output_df.columns = [
            'Uploaded_ID', 'Uploaded_Address', 'Matched_Platinum_ID',
            'Matched_Address', 'Match_Score', 'Match_Status', 'Source_Type'
        ]
        
        with col1:
            csv = output_df.to_csv(index=False)
            st.download_button(
                "📥 Download All Results",
                csv,
                "match_results_full.csv",
                "text/csv",
                use_container_width=True
            )
        
        # Matched only
        matched_df = output_df[output_df['Match_Status'] != 'NO_MATCH']
        with col2:
            csv_matched = matched_df.to_csv(index=False)
            st.download_button(
                "✅ Download Matched Only",
                csv_matched,
                "match_results_matched.csv",
                "text/csv",
                use_container_width=True
            )
        
        # Unmatched only
        unmatched_df = output_df[output_df['Match_Status'] == 'NO_MATCH']
        with col3:
            csv_unmatched = unmatched_df.to_csv(index=False)
            st.download_button(
                "❌ Download Unmatched Only",
                csv_unmatched,
                "match_results_unmatched.csv",
                "text/csv",
                use_container_width=True
            )
        
        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Start New Match", use_container_width=True):
                st.session_state.results = None
                st.session_state.stage_results = None
                st.session_state.processed = False
                st.rerun()

if __name__ == "__main__":
    main()
