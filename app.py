import streamlit as st
import joblib
import re
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# -------------------- NLTK --------------------
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# -------------------- LOAD MODEL --------------------
model = joblib.load('logistic_regression_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# -------------------- PREPROCESSING --------------------
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

if 'single_review_result' not in st.session_state:
    st.session_state.single_review_result = None


def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    words = word_tokenize(text)
    words = [ps.stem(word) for word in words if word not in stop_words]
    return ' '.join(words)


def get_developer_container(label):
    if hasattr(st, 'popover'):
        return st.popover(label)
    return st.expander(label)


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title='Movie Review Sentiment Analysis',
    page_icon='??',
    layout='wide'
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(rgba(10,10,25,0.78), rgba(10,10,25,0.85)),
        url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    animation: bgZoom 20s ease-in-out infinite alternate;
}

@keyframes bgZoom {
    from { background-size: 100%; }
    to { background-size: 108%; }
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 8px;
    text-shadow: 0 0 18px rgba(255, 0, 128, 0.35);
    animation: fadeDown 1s ease;
}

.subtitle {
    text-align: center;
    color: #e5e7eb;
    font-size: 1.1rem;
    margin-bottom: 28px;
    animation: fadeUp 1.2s ease;
}

.glass {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    animation: fadeUp 0.8s ease;
}

.section-title {
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 14px;
    text-shadow: 0 0 10px rgba(99,102,241,0.4);
}  

.soft-text {
    color: #e5e7eb;
    font-size: 1rem;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.22) !important;
    border-radius: 18px !important;
    padding: 14px !important;
    font-size: 1rem !important;
    min-height: 180px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.22);
}

.stTextArea textarea::placeholder {
    color: #cbd5e1 !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.16);
}

div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6);
    background-size: 200% auto;
    box-shadow: 0 8px 22px rgba(139,92,246,0.45);
    transition: 0.35s ease;
    animation: pulseGlow 2.2s infinite;
}

div.stButton > button:hover {
    transform: scale(1.02);
    background-position: right center;
    box-shadow: 0 10px 26px rgba(59,130,246,0.58);
}

div.stDownloadButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-size: 1.02rem;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg, #10b981, #06b6d4);
    box-shadow: 0 8px 22px rgba(6,182,212,0.35);
    transition: 0.3s ease;
}

div.stDownloadButton > button:hover {
    transform: scale(1.02);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background: rgba(255,255,255,0.06);
    padding: 10px;
    border-radius: 16px;
    margin-bottom: 18px;
}

.stTabs [data-baseweb="tab"] {
    height: 56px;
    white-space: pre-wrap;
    background: rgba(255,255,255,0.08);
    border-radius: 14px;
    color: white;
    font-size: 1rem;
    font-weight: 700;
    padding: 10px 22px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.12);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(236,72,153,0.95), rgba(59,130,246,0.95)) !important;
    color: white !important;
    box-shadow: 0 8px 20px rgba(59,130,246,0.28);
}

.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.06));
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 22px;
    padding: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.24);
    transition: 0.3s ease;
    animation: zoomIn 0.8s ease;
}

.metric-card:hover {
    transform: translateY(-5px) scale(1.02);
}

.metric-title {
    color: #dbeafe;
    font-size: 1rem;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
}

.result-positive {
    background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(5,150,105,0.14));
    border: 1px solid rgba(16,185,129,0.35);
    color: #ecfdf5;
    padding: 18px;
    border-radius: 18px;
    font-size: 1.2rem;
    font-weight: 700;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 14px;
    animation: fadeUp 0.7s ease;
}

.result-negative {
    background: linear-gradient(135deg, rgba(239,68,68,0.22), rgba(190,24,93,0.14));
    border: 1px solid rgba(239,68,68,0.35);
    color: #fef2f2;
    padding: 18px;
    border-radius: 18px;
    font-size: 1.2rem;
    font-weight: 700;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 14px;
    animation: fadeUp 0.7s ease;
}

.processed-box {
    background: rgba(15,23,42,0.75);
    border-left: 5px solid #22d3ee;
    color: #f8fafc;
    padding: 16px;
    border-radius: 14px;
    font-size: 0.98rem;
    margin-top: 10px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.25);
}

.info-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 18px;
    padding: 18px;
    color: white;
    box-shadow: 0 4px 16px rgba(0,0,0,0.22);
}

.progress-label {
    color: white;
    font-weight: 600;
    margin-bottom: 5px;
    margin-top: 10px;
}

[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.08);
    padding: 8px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.14);
}

@keyframes fadeDown {
    from {opacity: 0; transform: translateY(-24px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes fadeUp {
    from {opacity: 0; transform: translateY(24px);}
    to {opacity: 1; transform: translateY(0);}
}

@keyframes zoomIn {
    from {opacity: 0; transform: scale(0.9);}
    to {opacity: 1; transform: scale(1);}
}

@keyframes pulseGlow {
    0% { box-shadow: 0 0 12px rgba(236,72,153,0.28); }
    50% { box-shadow: 0 0 24px rgba(59,130,246,0.5); }
    100% { box-shadow: 0 0 12px rgba(236,72,153,0.28); }
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<div class="main-title">Movie Review Sentiment Analysis</div>', unsafe_allow_html=True)

# -------------------- TABS --------------------
tab1, tab2 = st.tabs([' Single Review', ' CSV Upload'])

# -------------------- TAB 1 --------------------
with tab1:
    st.markdown('<div class="section-title">Analyze a Single Review</div>', unsafe_allow_html=True)
    st.markdown('<div class="soft-text">Enter a movie review and get the final sentiment first. Open Developer to see the detailed analysis.</div>', unsafe_allow_html=True)

    user_input = st.text_area(
        'Enter your movie review:',
        placeholder='Example: This movie was absolutely fantastic, emotional, and brilliantly acted.'
    )

    if st.button(' Analyze Review'):
        if not user_input.strip():
            st.warning('Please enter a review.')
        else:
            with st.spinner('Analyzing review...'):
                cleaned = preprocess_text(user_input)
                vector = vectorizer.transform([cleaned])
                result = model.predict(vector)[0]
                probabilities = model.predict_proba(vector)[0]

                st.session_state.single_review_result = {
                    'result': result,
                    'cleaned': cleaned,
                    'negative_conf': probabilities[0] * 100,
                    'positive_conf': probabilities[1] * 100,
                    'confidence': max(probabilities) * 100
                }

    if st.session_state.single_review_result is not None:
        single_review_result = st.session_state.single_review_result

        if single_review_result['result'] == 1:
            st.markdown('<div class="result-positive">Positive Review</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-negative">Negative Review</div>', unsafe_allow_html=True)

        developer_panel = get_developer_container('Developer')
        developer_panel.markdown('<div class="section-title">Detailed Analysis</div>', unsafe_allow_html=True)

        detail_col1, detail_col2, detail_col3 = developer_panel.columns(3)
        with detail_col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Overall Confidence</div>
                    <div class="metric-value">{single_review_result['confidence']:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

        with detail_col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Positive Score</div>
                    <div class="metric-value">{single_review_result['positive_conf']:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

        with detail_col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Negative Score</div>
                    <div class="metric-value">{single_review_result['negative_conf']:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

        developer_panel.markdown('<div class="section-title">Confidence Bars</div>', unsafe_allow_html=True)
        developer_panel.markdown('<div class="progress-label">Positive</div>', unsafe_allow_html=True)
        developer_panel.progress(min(int(single_review_result['positive_conf']), 100))
        developer_panel.markdown('<div class="progress-label">Negative</div>', unsafe_allow_html=True)
        developer_panel.progress(min(int(single_review_result['negative_conf']), 100))

        chart_data = pd.DataFrame(
            {
                'Sentiment': ['Negative', 'Positive'],
                'Confidence': [
                    single_review_result['negative_conf'],
                    single_review_result['positive_conf']
                ]
            }
        ).set_index('Sentiment')

        developer_panel.markdown('<div class="section-title">Confidence Graph</div>', unsafe_allow_html=True)
        developer_panel.bar_chart(chart_data)
        developer_panel.markdown('<div class="section-title">Processed Text</div>', unsafe_allow_html=True)
        developer_panel.markdown(
            f'<div class="processed-box">{single_review_result["cleaned"]}</div>',
            unsafe_allow_html=True
        )

# -------------------- TAB 2 --------------------
with tab2:
    st.markdown('<div class="section-title">Upload CSV File</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="soft-text">Upload a CSV file containing a column named <b>review</b>. The page shows only the sentiment percentages by default, and Developer opens the full analysis.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader('Choose a CSV file', type=['csv'])

    if uploaded_file is not None:
        try:
            with st.spinner('Processing CSV file...'):
                df = pd.read_csv(uploaded_file)

                if 'review' not in df.columns:
                    st.error("CSV must contain a column named 'review'.")
                else:
                    df['cleaned_review'] = df['review'].apply(preprocess_text)
                    vectors = vectorizer.transform(df['cleaned_review'])
                    predictions = model.predict(vectors)
                    probabilities = model.predict_proba(vectors)

                    df['prediction'] = predictions
                    df['sentiment'] = df['prediction'].apply(lambda x: 'Positive' if x == 1 else 'Negative')
                    df['negative_score'] = probabilities[:, 0] * 100
                    df['positive_score'] = probabilities[:, 1] * 100

                    total_reviews = len(df)
                    positive_count = (df['prediction'] == 1).sum()
                    negative_count = (df['prediction'] == 0).sum()
                    positive_percent = (positive_count / total_reviews) * 100
                    negative_percent = (negative_count / total_reviews) * 100

                    st.success('CSV processed successfully!')
                    st.markdown('<div class="section-title">Sentiment Summary</div>', unsafe_allow_html=True)

                    summary_col1, summary_col2 = st.columns(2)
                    with summary_col1:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">Positive Reviews</div>
                                <div class="metric-value">{positive_percent:.2f}%</div>
                            </div>
                        """, unsafe_allow_html=True)

                    with summary_col2:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">Negative Reviews</div>
                                <div class="metric-value">{negative_percent:.2f}%</div>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown(
                        f'<div class="soft-text">Total reviews analyzed: <b>{total_reviews}</b></div>',
                        unsafe_allow_html=True
                    )

                    developer_panel = get_developer_container('Developer')
                    developer_panel.markdown('<div class="section-title">Detailed CSV Analysis</div>', unsafe_allow_html=True)

                    count_col1, count_col2, count_col3 = developer_panel.columns(3)
                    with count_col1:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">Total Reviews</div>
                                <div class="metric-value">{total_reviews}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    with count_col2:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">Positive Reviews</div>
                                <div class="metric-value">{positive_count}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    with count_col3:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">Negative Reviews</div>
                                <div class="metric-value">{negative_count}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    detail_left, detail_right = developer_panel.columns([1, 1])
                    with detail_left:
                        st.markdown('<div class="info-card">', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Sentiment Percentages</div>', unsafe_allow_html=True)
                        st.write(f'**Positive Reviews:** {positive_count} ({positive_percent:.2f}%)')
                        st.write(f'**Negative Reviews:** {negative_count} ({negative_percent:.2f}%)')
                        st.markdown('<div class="progress-label">Positive Percentage</div>', unsafe_allow_html=True)
                        st.progress(min(int(positive_percent), 100))
                        st.markdown('<div class="progress-label">Negative Percentage</div>', unsafe_allow_html=True)
                        st.progress(min(int(negative_percent), 100))
                        st.markdown('</div>', unsafe_allow_html=True)

                    with detail_right:
                        summary_df = pd.DataFrame(
                            {
                                'Sentiment': ['Positive', 'Negative'],
                                'Percentage': [positive_percent, negative_percent]
                            }
                        ).set_index('Sentiment')
                        developer_panel.markdown('<div class="section-title">Sentiment Distribution</div>', unsafe_allow_html=True)
                        developer_panel.bar_chart(summary_df)

                    developer_panel.markdown('<div class="section-title">Prediction Results</div>', unsafe_allow_html=True)
                    developer_panel.dataframe(
                        df[['review', 'cleaned_review', 'sentiment', 'positive_score', 'negative_score']],
                        use_container_width=True
                    )

                    csv_download = df.to_csv(index=False).encode('utf-8')
                    developer_panel.download_button(
                        label='Download Results CSV',
                        data=csv_download,
                        file_name='predicted_reviews.csv',
                        mime='text/csv'
                    )

        except Exception as e:
            st.error(f'Error processing file: {e}')

# -------------------- FOOTER --------------------
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,27,75,0.95));
    color: #e5e7eb;
    text-align: center;
    padding: 10px 0;
    font-size: 0.9rem;
    border-top: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    z-index: 999;
}

.main-content {
    padding-bottom: 60px;
}
</style>

<div class="footer">
    2026 | Movie Review Sentiment Analysis | MCA 2nd Year Final Project | Institute of Engineering and Technology, Lucknow, Uttar Pradesh
</div>
""", unsafe_allow_html=True)
