import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Airline Demand Dashboard", layout="wide")

st.title("✈️ Airline Market Demand Dashboard")

# ========== Sidebar Filters ==========
st.sidebar.header("🔍 Filters")

search_route = st.sidebar.text_input("Search Route (e.g., Sydney ➝ Melbourne)").strip().lower()
search_airline = st.sidebar.text_input("Search Airline").strip().lower()

chart_type = st.sidebar.selectbox("Chart Type", ["Bar", "Pie"])
refresh = st.sidebar.button("🔄 Refresh Data")

# Placeholder for future date support
st.sidebar.date_input("Select Date (optional)", help="API does not support date filter yet.")

if refresh:
    st.experimental_rerun()

# ========== Fetch API Data ==========
API_ENDPOINT = "http://127.0.0.1:8000/insights"

with st.spinner("Fetching flight market data..."):
    try:
        response = requests.get(API_ENDPOINT)
        insights = response.json()

        # --------- Process Top Routes ---------
        routes = insights.get("top_routes", [])[:20]
        if search_route:
            routes = [r for r in routes if search_route in r[0].lower()]
        total_routes = len(routes)
        total_flights = sum([count for _, count in routes])

        # --------- Process Airlines ---------
        airlines = insights.get("top_airlines", [])[:20]
        if search_airline:
            airlines = [a for a in airlines if search_airline in a[0].lower()]
        total_airlines = len(airlines)

        # --------- Flight Statuses ---------
        statuses = insights.get("flight_statuses", {})

    except Exception as e:
        st.error(f"⚠️ Could not load data: {e}")
        st.stop()

# ========== Metrics ==========
st.markdown("### 📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("🛫 Total Routes", total_routes)
col2.metric("🛬 Total Airlines", total_airlines)
col3.metric("📦 Flights Tracked", total_flights)

st.markdown("---")

# ========== Routes Chart ==========
st.subheader("🧭 Top Routes")
if routes:
    route_names, route_counts = zip(*routes)
    if chart_type == "Bar":
        st.bar_chart(pd.DataFrame({"Route": route_names, "Flights": route_counts}).set_index("Route"))
    else:
        fig = px.pie(names=route_names, values=route_counts, title="Route Share", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # Download CSV
    df_routes = pd.DataFrame(routes, columns=["Route", "Flights"])
    st.download_button("📥 Download Routes CSV", df_routes.to_csv(index=False).encode(), "routes.csv", "text/csv")
else:
    st.info("No route data found.")

# ========== Airlines Chart ==========
st.subheader("🏢 Top Airlines")
if airlines:
    airline_names, airline_counts = zip(*airlines)
    if chart_type == "Bar":
        st.bar_chart(pd.DataFrame({"Airline": airline_names, "Flights": airline_counts}).set_index("Airline"))
    else:
        fig = px.pie(names=airline_names, values=airline_counts, title="Airline Share", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # Download CSV
    df_airlines = pd.DataFrame(airlines, columns=["Airline", "Flights"])
    st.download_button("📥 Download Airlines CSV", df_airlines.to_csv(index=False).encode(), "airlines.csv", "text/csv")
else:
    st.info("No airline data found.")

# ========== Flight Status Chart ==========
st.subheader("📶 Flight Status Summary")
if statuses:
    status_df = pd.DataFrame(list(statuses.items()), columns=["Status", "Count"]).set_index("Status")
    st.bar_chart(status_df)
else:
    st.info("No flight status information available.")

# ========== Footer ==========
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, FastAPI, and AviationStack API.")
