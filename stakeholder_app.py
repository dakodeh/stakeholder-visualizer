
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Stakeholder Sentiment Visualizer", layout="centered")

st.title("📊 Stakeholder Sentiment vs. Influence Clustering v2.1.2")

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
        impact_size_map = {"Low": 20, "Medium": 40, "High": 60}

        df["Sentiment Value"] = df["Sentiment"].map(sentiment_map)
        df["Influence Value"] = df["Influence"].map(influence_map)
        df["Impact Size"] = df["Impact"].map(impact_size_map).fillna(30)

        # Create hover text
        df["Hover"] = df["Stakeholder Name"] + "<br>Group: " + df["Stakeholder Group"] +                       "<br>Sentiment: " + df["Sentiment"] +                       "<br>Influence: " + df["Influence"] +                       "<br>Impact: " + df["Impact"]

        # Plot with Plotly
        fig = px.scatter(df,
                         x="Influence Value",
                         y="Sentiment Value",
                         size="Impact Size",
                         color="Stakeholder Group",
                         hover_name="Stakeholder Name",
                         hover_data={"Influence Value": False,
                                     "Sentiment Value": False,
                                     "Impact Size": False,
                                     "Stakeholder Group": False,
                                     "Hover": True},
                         labels={"Influence Value": "Influence Level", "Sentiment Value": "Sentiment"},
                         size_max=60)

        # Update axes
        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=[0, 1, 2], ticktext=['Low', 'Medium', 'High']),
            yaxis=dict(tickmode='array', tickvals=[-1, 0, 1], ticktext=['Negative', 'Neutral', 'Positive']),
            title="Stakeholder Sentiment vs. Influence Clustering",
            legend_title_text="Stakeholder Group",
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Failed to read or parse Excel file: {e}")
else:
    st.info("Upload a stakeholder analysis Excel file to begin.")
