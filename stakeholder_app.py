import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO

# Mapping for axes
sentiment_mapping = {"Negative": 0, "Neutral": 1, "Positive": 2}
influence_mapping = {"Low": 0, "Medium": 1, "High": 2}

# Quadrant strategy labels
quadrant_labels = {
    (0, 0): "Distractor - Low Priority",
    (1, 0): "Skeptic - Address Concerns",
    (2, 0): "Resistor - Mitigate Risk",
    (0, 1): "Bystander - Inform",
    (1, 1): "Neutral - Educate",
    (2, 1): "Wild Card - Manage Closely",
    (0, 2): "Ally - Monitor",
    (1, 2): "Supporter - Engage",
    (2, 2): "Champion - Leverage"
}

def load_stakeholder_data(file):
    df = pd.read_excel(file, sheet_name="Stakeholder Analysis", skiprows=3)
    # Rename relevant columns
    column_map = {
        "Stakeholder Name": "Name",
        "Stakeholder Group": "Group",
        "Sentiment": "Sentiment",
        "Influence": "Influence"
    }
    df = df.rename(columns=column_map)
    # Keep only the columns we care about
    df = df[["Name", "Group", "Sentiment", "Influence"]].dropna(subset=["Name", "Sentiment", "Influence"])
    df["Size"] = 5  # Default bubble size if not specified
    return df

st.title("Stakeholder Sentiment vs. Influence Clustering")
uploaded_file = st.file_uploader("Upload Stakeholder Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = load_stakeholder_data(uploaded_file)
        df["SentimentScore"] = df["Sentiment"].map(sentiment_mapping)
        df["InfluenceScore"] = df["Influence"].map(influence_mapping)

        fig, ax = plt.subplots(figsize=(10, 8))
        groups = df["Group"].unique()
        colors = plt.cm.tab10(range(len(groups)))

        for group, color in zip(groups, colors):
            subset = df[df["Group"] == group]
            ax.scatter(subset["InfluenceScore"], subset["SentimentScore"],
                       s=subset["Size"] * 20, alpha=0.7, label=group, c=[color])

        # Add quadrant strategy labels
        for (x, y), label in quadrant_labels.items():
            ax.text(x, y, label, fontsize=8, ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

        # Axis and labels
        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(["Low", "Medium", "High"])
        ax.set_yticks([0, 1, 2])
        ax.set_yticklabels(["Negative", "Neutral", "Positive"])
        ax.set_xlabel("Influence Level")
        ax.set_ylabel("Sentiment")
        ax.set_title("Stakeholder Sentiment vs. Influence Clustering")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(title="Stakeholder Group", bbox_to_anchor=(1.05, 1), loc='upper left')

        st.pyplot(fig)

        # PNG download
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        st.download_button("Download Chart as PNG", data=buf.getvalue(),
                           file_name="stakeholder_chart.png", mime="image/png")

    except Exception as e:
        st.error(f"⚠️ An error occurred while processing the file: {str(e)}")
else:
    st.info("📄 Please upload an Excel file with a 'Stakeholder Analysis' worksheet.")
