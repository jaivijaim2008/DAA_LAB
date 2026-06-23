import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px

# ============================================================================
# STRING MATCHING ALGORITHMS
# ============================================================================

def naive_search(text, pattern):
    """Naive string search"""
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)
    return matches, comparisons

def compute_lps(pattern):
    """Compute Longest Proper Prefix which is also Suffix"""
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps

def kmp_search(text, pattern):
    """Knuth-Morris-Pratt search"""
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches, comparisons

def rabin_karp(text, pattern, q=101):
    """Rabin-Karp algorithm"""
    n, m = len(text), len(pattern)
    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0
    matches, comparisons = [], 0
    
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q
    
    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)
        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q
    return matches, comparisons

# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(page_title="Lab 2 - String Matching", layout="wide")
st.title("🔤 Lab 2: String Matching Algorithm Analysis")
st.markdown("Compare **Naive**, **KMP**, and **Rabin-Karp** string matching algorithms")

tab1, tab2 = st.tabs(["Single Search", "Performance Comparison"])

with tab1:
    st.subheader("Pattern Search Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        text_mode = st.radio("Text source:", ["Sample Text", "Custom Text"])
        if text_mode == "Sample Text":
            text = 'AABAACAADAABAABA'
        else:
            text = st.text_input("Enter text:", "AABAACAADAABAABA")
    
    with col2:
        pattern = st.text_input("Enter pattern:", "AABA")
    
    if text and pattern:
        if len(pattern) > len(text):
            st.error("❌ Pattern cannot be longer than text")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("### Naive Search")
                try:
                    m1, c1 = naive_search(text, pattern)
                    st.metric("Matches found", len(m1))
                    st.metric("Comparisons", c1)
                    if m1:
                        st.write(f"**Positions:** {m1}")
                    else:
                        st.info("No matches found")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            with col2:
                st.write("### KMP Search")
                try:
                    m2, c2 = kmp_search(text, pattern)
                    st.metric("Matches found", len(m2))
                    st.metric("Comparisons", c2)
                    if m2:
                        st.write(f"**Positions:** {m2}")
                    else:
                        st.info("No matches found")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            with col3:
                st.write("### Rabin-Karp Search")
                try:
                    m3, c3 = rabin_karp(text, pattern)
                    st.metric("Matches found", len(m3))
                    st.metric("Comparisons", c3)
                    if m3:
                        st.write(f"**Positions:** {m3}")
                    else:
                        st.info("No matches found")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            # Visualization
            st.write("---")
            st.write("### Algorithm Comparison")
            comparison = pd.DataFrame({
                'Algorithm': ['Naive', 'KMP', 'Rabin-Karp'],
                'Comparisons': [c1, c2, c3],
                'Matches': [len(m1), len(m2), len(m3)]
            })
            
            fig = px.bar(comparison, x='Algorithm', y='Comparisons',
                        title='Character Comparisons by Algorithm',
                        color='Algorithm',
                        labels={'Comparisons': 'Number of Comparisons'})
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Performance Analysis (10,000 character text)")
    
    text_large = ''.join(random.choices('ABCD', k=10000))
    patterns = ['AB', 'ABCD', 'ABCDAB', 'ABCDABCD']
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, pattern in enumerate(patterns):
        status_text.text(f"Testing pattern: {pattern}...")
        
        _, c1 = naive_search(text_large, pattern)
        _, c2 = kmp_search(text_large, pattern)
        _, c3 = rabin_karp(text_large, pattern)
        
        results.append({
            'Pattern': pattern,
            'Naive': c1,
            'KMP': c2,
            'Rabin-Karp': c3
        })
        
        progress_bar.progress((idx + 1) / len(patterns))
    
    status_text.empty()
    df = pd.DataFrame(results)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(df, x='Pattern', y=['Naive', 'KMP', 'Rabin-Karp'],
                    title='Algorithm Performance Comparison',
                    barmode='group',
                    labels={'value': 'Comparisons', 'Pattern': 'Search Pattern'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("### Results Table")
        st.dataframe(df, use_container_width=True)
        
        st.write("---")
        st.write("### Summary")
        st.write(f"📊 **Text size:** 10,000 characters (random ABCD)")
        
        best_algo = df[['Naive', 'KMP', 'Rabin-Karp']].sum().idxmin()
        st.write(f"✅ **Best performer:** **{best_algo}** (fewest total comparisons)")
        
        st.write("---")
        st.write("### Algorithm Details")
        st.markdown("""
        - **Naive Search:** O(n*m) — checks every position
        - **KMP Search:** O(n+m) — uses failure function to skip redundant comparisons
        - **Rabin-Karp:** O(n+m) average — uses rolling hash for faster comparison
        """)
