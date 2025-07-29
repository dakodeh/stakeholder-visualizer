
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Stakeholder Sentiment Visualizer", layout="wide")
st.title("📊 Stakeholder Sentiment vs. Influence Visualizer (v2.1.4)")

uploaded_file = st.file_uploader("Upload Stakeholder Excel File (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        raw_df = pd.read_excel(uploaded_file, sheet_name="Stakeholder Analysis", header=None)

        # Identify the row with headers
        header_row_idx = raw_df[raw_df.iloc[:, 0] == "Stakeholder Name"].index[0]
        df = raw_df.iloc[header_row_idx + 1:].copy()
        df.columns = raw_df.iloc[header_row_idx]

        df = df[df["Stakeholder Name"].notna() & df["Sentiment"].notna() & df["Influence"].notna()]
        df = df[df["Stakeholder Group"].notna()]

        sentiment_map = {"Negative": -1, "Neutral": 0, "Positive": 1}
        influence_map = {"Low": 0, "Medium": 1, "High": 2}
        size_map = {"Low": 200, "Medium": 400, "High": 600}

        df["Sentiment Value"] = df["Sentiment"].map(sentiment_map)
        df["Influence Value"] = df["Influence"].map(influence_map)
        df["Impact Size"] = df["Impact"].map(size_map).fillna(300)

        # Add jitter
        np.random.seed(42)
        df["Influence Jitter"] = df["Influence Value"] + np.random.uniform(-0.35, 0.35, size=len(df))
        df["Sentiment Jitter"] = df["Sentiment Value"] + np.random.uniform(-0.35, 0.35, size=len(df))

        # Assign engagement strategy
        quadrant_strategies = {
            (2, -1): "Engage Immediately",
            (2, 0): "Leverage as Advocate",
            (2, 1): "Leverage as Advocate",
            (1, -1): "Monitor Closely",
            (1, 0): "Monitor Neutral Parties",
            (1, 1): "Inform Regularly",
            (0, -1): "Observe Occasionally",
            (0, 0): "Monitor Neutral Parties",
            (0, 1): "Inform as Needed",
        }
        df["Engagement Strategy"] = df.apply(
            lambda row: quadrant_strategies.get((row["Influence Value"], row["Sentiment Value"]), "Undefined"), axis=1
        )

        # Show Engagement Strategy Summary Table
        st.subheader("💡 Stakeholder Engagement Strategy Table")
        st.dataframe(df[["Stakeholder Name", "Engagement Strategy"]].sort_values(by="Engagement Strategy"))

        # Plotly chart
        fig = px.scatter(
            df,
            x="Influence Jitter",
            y="Sentiment Jitter",
            size="Impact Size",
            color="Stakeholder Group",
            hover_data={
                "Stakeholder Name": True,
                "Group": df["Stakeholder Group"],
                "Sentiment": df["Sentiment"],
                "Influence": df["Influence"],
                "Engagement Strategy": df["Engagement Strategy"],
                "Influence Jitter": False,
                "Sentiment Jitter": False,
                "Impact Size": False,
            },
            size_max=600,
        )

        fig.update_layout(
            xaxis=dict(
                title="Influence",
                tickvals=[0, 1, 2],
                ticktext=["Low", "Medium", "High"],
                range=[-0.5, 2.5]
            ),
            yaxis=dict(
                title="Sentiment",
                tickvals=[-1, 0, 1],
                ticktext=["Negative", "Neutral", "Positive"],
                range=[-1.5, 1.5]
            ),
            title="Stakeholder Sentiment vs. Influence Clustering",
            legend_title_text="Stakeholder Group"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Failed to read or parse Excel file: {e}")
else:
    st.info("Upload a stakeholder analysis Excel file to begin.")
