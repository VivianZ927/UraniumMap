import streamlit as st
from streamlit_plotly_mapbox_events import plotly_mapbox_events
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Uranium Mine Map", layout="wide")


def load_data(path: str, sheet: str = "Mines") -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet)
    return df


def make_map(df: pd.DataFrame, height: int = 650, marker_size: int = 10):
    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Site",
        hover_data={
            "Country": True,
            # "Region/Area": True,
            "Closed year (numeric)": True,
            "Till Now(Years)": True,
            "Status": True,
            "Latitude": False,
            "Longitude": False,
        },
        zoom=5.5,
        height=height,
    )

    # Force uniform red markers (no size variation, no color mapping)
    fig.update_traces(marker=dict(size=marker_size, color="red", opacity=0.85))

    # Auto-fit to filtered points (nice when country filter changes)
    if len(df) >= 2:
        fig.update_layout(
            mapbox_bounds={
                "west": df["Longitude"].min(),
                "east": df["Longitude"].max(),
                "south": df["Latitude"].min(),
                "north": df["Latitude"].max(),
            }
        )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(r=0, t=0, l=0, b=0),
    )
    return fig


def main():
    st.title("Uranium Mine Map")

    df = load_data("uranium_mines_uk_europe_locations.xlsx", "Mines")

    # Sidebar: Country filter only
    with st.sidebar:
        st.header("Filter")
        if "Country" in df.columns:
            countries = sorted(df["Country"].dropna().unique())
            selected_countries = st.multiselect("Country", countries, default=countries)
            filtered = df[df["Country"].isin(selected_countries)].copy()
        else:
            st.warning("No 'Country' column found in the dataset.")
            filtered = df

        height = st.slider("Map height", 400, 900, 650, 50)
        marker_size = st.slider("Marker size", 6, 18, 10, 1)

    fig = make_map(filtered, height=height, marker_size=marker_size)

    plotly_mapbox_events(
        fig,
        click_event=True,
        select_event=True,
        hover_event=False,   # less noisy / better performance
        override_height=height,
    )


if __name__ == "__main__":
    main()
