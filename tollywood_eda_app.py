# tollywood_eda_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime

st.set_page_config(page_title="Tollywood Movies 2024 - EDA", layout="wide")

st.title("🎬 Tollywood Movies 2024 - Exploratory Data Analysis")

# Upload dataset
uploaded_file = st.file_uploader("Upload your Tollywood 2024 dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Basic Preprocessing
    df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
    df['Month'] = df['Release_Date'].dt.month
    df['Quarter'] = df['Release_Date'].dt.quarter

    df['IMDb_Rating'].fillna(df['IMDb_Rating'].mean(), inplace=True)
    df.dropna(subset=['Title', 'Budget_Cr', 'BoxOffice_Cr'], inplace=True)

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    genres = st.sidebar.multiselect("Select Genres", df['Genre'].unique(), default=df['Genre'].unique())
    df = df[df['Genre'].isin(genres)]

    # Top Movies by Box Office
    st.subheader("💰 Top 10 Movies by Box Office Collection")
    top_movies = df.sort_values(by='BoxOffice_Cr', ascending=False).head(10)
    fig1, ax1 = plt.subplots()
    sns.barplot(data=top_movies, x='BoxOffice_Cr', y='Title', ax=ax1, palette="viridis")
    ax1.set_xlabel("Box Office (Cr)")
    ax1.set_ylabel("Movie Title")
    st.pyplot(fig1)

    # Ratings Distribution
    st.subheader("⭐ IMDb Ratings Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(df['IMDb_Rating'], bins=10, kde=True, color='skyblue', ax=ax2)
    ax2.set_xlabel("Rating")
    ax2.set_ylabel("Number of Movies")
    st.pyplot(fig2)

    # Budget vs Box Office
    st.subheader("📉 Budget vs Box Office Collection")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=df, x='Budget_Cr', y='BoxOffice_Cr', hue='Genre', ax=ax3)
    ax3.set_xlabel("Budget (Cr)")
    ax3.set_ylabel("Box Office (Cr)")
    st.pyplot(fig3)

    # Genre-wise Average Ratings
    st.subheader("🎭 Average IMDb Rating by Genre")
    avg_rating = df.groupby('Genre')['IMDb_Rating'].mean().sort_values(ascending=False)
    fig4, ax4 = plt.subplots()
    sns.barplot(x=avg_rating.index, y=avg_rating.values, palette="magma", ax=ax4)
    ax4.set_ylabel("Average Rating")
    ax4.set_xlabel("Genre")
    ax4.tick_params(axis='x', rotation=45)
    st.pyplot(fig4)

    # Most Active Directors
    st.subheader("🎬 Top 10 Directors by Number of Movies")
    top_directors = df['Director'].value_counts().head(10)
    fig5, ax5 = plt.subplots()
    sns.barplot(x=top_directors.values, y=top_directors.index, palette="flare", ax=ax5)
    ax5.set_xlabel("Number of Movies")
    st.pyplot(fig5)

    # WordCloud for Cast
    st.subheader("👥 WordCloud of Most Frequent Cast Members")
    all_cast = ', '.join(df['Cast'].dropna().tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_cast)
    fig6, ax6 = plt.subplots(figsize=(12, 6))
    ax6.imshow(wordcloud, interpolation='bilinear')
    ax6.axis("off")
    st.pyplot(fig6)

    # Monthly Release Trend
    st.subheader("📅 Monthly Movie Release Trend (2025)")
    monthly_releases = df['Month'].value_counts().sort_index()
    fig7, ax7 = plt.subplots()
    sns.lineplot(x=monthly_releases.index, y=monthly_releases.values, marker='o', ax=ax7)
    ax7.set_xlabel("Month")
    ax7.set_ylabel("Number of Movies")
    st.pyplot(fig7)

else:
    st.info("Please upload a CSV file to begin the analysis.")
