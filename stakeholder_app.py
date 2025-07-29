import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Stakeholder Sentiment Visualizer", layout="centered")
st.title("📊 Stakeholder Sentiment vs. Influence Clustering")

uploaded_file = st.file_uploader("Upload Stakeholder Excel File (.xlsx)", type="xlsx")

def determine_strategy(sentiment, influence):
    if sentiment == 'Negative' and influence == 'High':
        return 'Engage Immediately'
    elif sentiment == 'Positive' and influence == 'High':
        return 'Leverage as Advocate'
    elif sentiment == 'Neutral':
        return 'Monitor Neutral Parties'
    else:
        return 'Observe Occasionally'

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

        # Add jitter for improved readability
        jitter_strength = 0.15
        df["Jittered Influence"] = df["Influence Value"] + [random.uniform(-jitter_strength, jitter_strength) for _ in range(len(df))]
        df["Jittered Sentiment"] = df["Sentiment Value"] + [random.uniform(-jitter_strength, jitter_strength) for _ in range(len(df))]

        # Assign engagement strategy
        df["Engagement Strategy"] = df.apply(lambda x: determine_strategy(x["Sentiment"], x["Influence"]), axis=1)

        # Display engagement table
        st.subheader("📋 Stakeholder Engagement Strategies")
        st.dataframe(df[["Stakeholder Name", "Stakeholder Group", "Sentiment", "Influence", "Impact", "Engagement Strategy"]])

        # Create interactive plot
        fig = px.scatter(
            df,
            x="Jittered Influence",
            y="Jittered Sentiment",
            size="Impact Size",
            color="Stakeholder Group",
            text="Stakeholder Name",
            hover_data={
                "Stakeholder Name": True,
                "Stakeholder Group": True,
                "Sentiment": True,
                "Influence": True,
                "Impact": True,
                "Engagement Strategy": True,
                "Jittered Influence": False,
                "Jittered Sentiment": False,
                "Impact Size": False
            },
            labels={"Jittered Influence": "Influence Level", "Jittered Sentiment": "Sentiment"},
            title="Stakeholder Sentiment vs. Influence Clustering"
        )

        fig.update_traces(textposition='top center')
        fig.update_layout(legend_title_text='Stakeholder Group')

        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"⚠️ Failed to read or parse Excel file: {e}")
else:
    st.info("Upload a stakeholder analysis Excel file to begin.")
