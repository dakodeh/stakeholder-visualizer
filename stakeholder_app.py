
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Stakeholder Sentiment Visualizer", layout="centered")
st.title("📊 Stakeholder Sentiment vs. Influence Clustering v2.1.3")

uploaded_file = st.file_uploader("Upload Stakeholder Excel File (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        sheet_name = "Stakeholder Analysis"
        raw_df = pd.read_excel(uploaded_file, sheet_name=sheet_name)

        header_row_idx = raw_df[raw_df.iloc[:, 0] == "Stakeholder Name"].index[0]
        df = raw_df.iloc[header_row_idx + 1:].copy()
        df.columns = raw_df.iloc[header_row_idx]
        df = df[df["Stakeholder Name"].notna() & df["Sentiment"].notna() & df["Influence"].notna()]
        df = df[df["Stakeholder Group"].notna()]

        sentiment_map = {"Negative": -1, "Neutral": 0, "Positive": 1}
        influence_map = {"Low": 0, "Medium": 1, "High": 2}
        impact_size_map = {"Low": 20, "Medium": 40, "High": 60}

        df["Sentiment Value"] = df["Sentiment"].map(sentiment_map)
        df["Influence Value"] = df["Influence"].map(influence_map)
        df["Impact Size"] = df["Impact"].map(impact_size_map).fillna(30)

        np.random.seed(42)
        df["Influence Jitter"] = df["Influence Value"] + np.random.uniform(-0.25, 0.25, len(df))
        df["Sentiment Jitter"] = df["Sentiment Value"] + np.random.uniform(-0.25, 0.25, len(df))

        fig = px.scatter(
            df,
            x="Influence Jitter",
            y="Sentiment Jitter",
            size="Impact Size",
            color="Stakeholder Group",
            hover_name="Stakeholder Name",
            hover_data={
                "Stakeholder Name": False,
                "Influence Jitter": False,
                "Sentiment Jitter": False,
                "Impact Size": False,
                "Influence": True,
                "Sentiment": True,
                "Impact": True,
                "Stakeholder Group": True
            },
            size_max=60,
            title="Stakeholder Sentiment vs. Influence Clustering"
        )

        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=[0, 1, 2], ticktext=["Low", "Medium", "High"], title="Influence Level"),
            yaxis=dict(tickmode='array', tickvals=[-1, 0, 1], ticktext=["Negative", "Neutral", "Positive"], title="Sentiment"),
            legend_title_text='Stakeholder Group'
        )

        for _, row in df.iterrows():
            fig.add_annotation(
                x=row["Influence Jitter"],
                y=row["Sentiment Jitter"],
                text=row["Stakeholder Name"],
                showarrow=False,
                font=dict(size=12, color="black")
            )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Failed to read or parse Excel file: {e}")
else:
    st.info("Upload a stakeholder analysis Excel file to begin.")
