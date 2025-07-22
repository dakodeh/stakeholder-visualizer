import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

st.set_page_config(page_title="Stakeholder Sentiment Visualizer", layout="centered")

st.title("📊 Stakeholder Sentiment vs. Influence Clustering")

uploaded_file = st.file_uploader("Upload Stakeholder Excel File (.xlsx)", type="xlsx")

if uploaded_file:
    sheet_name = "Stakeholder Analysis"

    try:
        raw_df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        header_row_idx = raw_df[raw_df.iloc[:, 0] == "Stakeholder Name"].index[0]
        df = raw_df.iloc[header_row_idx + 1:].copy()
        df.columns = raw_df.iloc[header_row_idx]

        # Filter out incomplete rows
        df = df[df["Stakeholder Name"].notna() & df["Sentiment"].notna() & df["Influence"].notna()]
        df = df[df["Stakeholder Group"].notna()]

        # Map values
        sentiment_map = {"Negative": -1, "Neutral": 0, "Positive": 1}
        influence_map = {"Low": 0, "Medium": 1, "High": 2}
        impact_size_map = {"Low": 200, "Medium": 400, "High": 600}

        df["Sentiment Value"] = df["Sentiment"].map(sentiment_map)
        df["Influence Value"] = df["Influence"].map(influence_map)
        df["Impact Size"] = df["Impact"].map(impact_size_map).fillna(300)

        unique_groups = df["Stakeholder Group"].unique()
        color_map = {group: color for group, color in zip(unique_groups, plt.cm.tab10.colors)}

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 8))
        texts = []

        for group in unique_groups:
            group_df = df[df["Stakeholder Group"] == group]
            ax.scatter(group_df["Influence Value"], group_df["Sentiment Value"],
                       s=group_df["Impact Size"], label=group, alpha=0.7,
                       color=color_map.get(group, 'gray'), edgecolors='black')

            for _, row in group_df.iterrows():
                text = ax.text(row["Influence Value"], row["Sentiment Value"],
                               row["Stakeholder Name"], fontsize=9)
                texts.append(text)

        adjust_text(texts,
                    arrowprops=dict(arrowstyle="-", color='gray', lw=0.5),
                    expand_points=(2, 2),
                    expand_text=(2, 2),
                    force_text=1.2,
                    force_points=1.0,
                    lim=500)

        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(["Low", "Medium", "High"])
        ax.set_yticks([-1, 0, 1])
        ax.set_yticklabels(["Negative", "Neutral", "Positive"])
        ax.set_xlabel("Influence Level")
        ax.set_ylabel("Sentiment")
        ax.set_title("Stakeholder Sentiment vs. Influence Clustering")
        ax.grid(True)
        ax.legend(title="Stakeholder Group", bbox_to_anchor=(1.05, 1), loc='upper left')
        fig.tight_layout()

        st.pyplot(fig)

    except Exception as e:
        st.error(f"⚠️ Failed to read or parse Excel file: {e}")
else:
    st.info("Upload a stakeholder analysis Excel file to begin.")
