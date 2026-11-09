import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ------------------------------------------------------------
# NICARAGUA: POPULATION HISTORY + CUBIC REGRESSION PROJECT
# Data: World Bank World Development Indicators, Population total
# Series: SP.POP.TOTL (1960-2025)
# ------------------------------------------------------------

st.set_page_config(
    page_title="Nicaragua | Population & History",
    page_icon="🇳🇮",
    layout="wide"
)

# Nicaragua-inspired colors
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f4f9fc 0%, #ffffff 45%, #f4f9fc 100%);
    }
    .hero {
        padding: 2rem 1.5rem;
        border-radius: 18px;
        background: linear-gradient(115deg, #0067a5 0%, #1687bd 55%, #ffffff 55%, #ffffff 100%);
        color: #082b45;
        border: 1px solid #d8e6ef;
        margin-bottom: 1rem;
    }
    .hero h1 { color: white; margin-bottom: .25rem; }
    .hero p { color: white; font-size: 1.05rem; max-width: 780px; }
    .small-note { color: #526575; font-size: .9rem; }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #dce7ee;
        padding: 12px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Annual population values in persons, sourced from World Bank WDI.
# Years 1960 through 2025, inclusive.
years = list(range(1960, 2026))
population = [
    1782370, 1836451, 1892320, 1950159, 2010176, 2072681,
    2137820, 2205567, 2275836, 2348398, 2423065, 2499825,
    2573578, 2649278, 2732075, 2816943, 2903851, 2992534,
    3080314, 3164525, 3252403, 3345674, 3438745, 3530282,
    3619104, 3706479, 3794157, 3882164, 3972320, 4066476,
    4162559, 4259637, 4357026, 4453732, 4549316, 4642931,
    4729974, 4809573, 4883655, 4954018, 5022633, 5087825,
    5149909, 5210963, 5272912, 5342105, 5418855, 5497243,
    5576593, 5656601, 5737450, 5819051, 5901287, 5983845,
    6066492, 6149417, 6232666, 6316231, 6400080, 6483657,
    6565267, 6644741, 6730654, 6823613, 6916140, 7007502
]

df = pd.DataFrame({"Year": years, "Population (people)": population})
df["Years since 1960"] = df["Year"] - 1960

# Fit a degree-3 polynomial using x = years since 1960.
x = df["Years since 1960"].to_numpy(dtype=float)
y = df["Population (people)"].to_numpy(dtype=float)
coefficients = np.polyfit(x, y, 3)
model = np.poly1d(coefficients)
first_derivative = np.polyder(model)
second_derivative = np.polyder(first_derivative)

def people(value):
    return f"{value:,.0f} people"

def rate(value):
    return f"{value:,.0f} people per year"

def year_label(x_value):
    return f"{1960 + x_value:.1f}"

st.markdown("""
<div class="hero">
    <h1>🇳🇮 Nicaragua: A Country in Numbers</h1>
    <p>Explore Nicaragua's history, culture, and population growth through real-world data
    and a cubic regression model.</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "This student project studies how Nicaragua's population changed from 1960 to 2025. "
    "The population is an important part of a country's story because it affects communities, "
    "schools, jobs, housing, transportation, and the economy."
)

# Country overview
st.header("Discover Nicaragua")
col1, col2 = st.columns([1.2, 1])
with col1:
    st.write(
        "**Nicaragua** is the largest country in Central America by land area. "
        "Its capital is **Managua**, and it has coastlines on both the Pacific Ocean "
        "and the Caribbean Sea. Spanish is the official language, and the country's "
        "culture includes Indigenous, Spanish, and Afro-Caribbean influences."
    )
    st.write(
        "Nicaragua is known for its lakes and volcanoes, traditional music and dance, "
        "poetry, agriculture, and cities such as León and Granada."
    )
with col2:
    st.info(
        "**Project focus**\n\n"
        "- Country: Nicaragua\n"
        "- Entity studied: Total population\n"
        "- Input (x): Year\n"
        "- Output (y): Number of people\n"
        "- Data period: 1960–2025\n"
        "- Model: Degree-3 polynomial (cubic) regression"
    )

st.divider()
st.header("1. Historical raw data")
st.write(
    "The table shows the annual population estimates used in this project. "
    "The input is the year, and the output is the estimated number of people living in Nicaragua."
)
st.dataframe(df[["Year", "Population (people)"]], use_container_width=True, hide_index=True)

csv = df[["Year", "Population (people)"]].to_csv(index=False).encode("utf-8")
st.download_button(
    "Download the raw data as CSV",
    data=csv,
    file_name="nicaragua_population_data_1960_2025.csv",
    mime="text/csv"
)

st.caption(
    "Source: World Bank, World Development Indicators, indicator SP.POP.TOTL. "
    "The values are annual population estimates."
)

st.divider()
st.header("2. Cubic regression model")

a, b, c, d = coefficients
st.write(
    "A cubic regression equation was fitted to all the population data. "
    "To make the equation easier to read, **x represents the number of years after 1960** "
    "and **P(x) represents the population in people**."
)
st.latex(
    rf"P(x) = ({a:.4f})x^3 + ({b:.4f})x^2 + ({c:.4f})x + ({d:.4f})"
)
st.caption("The coefficients are calculated from the data when the app runs; small rounding differences are normal.")

# Plot data and cubic curve over observed range, with optional extrapolation.
future_year = st.slider("Choose how far to extend the model beyond the data", 2025, 2040, 2030)
plot_years = np.linspace(1960, future_year, 400)
plot_x = plot_years - 1960
plot_y = model(plot_x)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Year"], y=df["Population (people)"],
    mode="markers", name="Actual population data",
    marker=dict(size=6)
))
fig.add_trace(go.Scatter(
    x=plot_years, y=plot_y,
    mode="lines", name="Cubic regression curve",
    line=dict(width=3)
))
fig.add_vline(x=2025, line_dash="dash", annotation_text="End of data (2025)")
fig.update_layout(
    title="Nicaragua Population: Data and Cubic Curve of Best Fit",
    xaxis_title="Year",
    yaxis_title="Population (people)",
    legend_title="",
    hovermode="x unified",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Fit quality
predicted_observed = model(x)
ss_res = np.sum((y - predicted_observed) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r_squared = 1 - ss_res / ss_tot
st.metric("R-squared (goodness of fit)", f"{r_squared:.5f}")
st.caption("R-squared describes how closely the model matches the data. It does not prove that the model explains why population changed.")

st.divider()
st.header("3. Function analysis in the real world")

# Local maxima/minima: derivative roots in the observed interval.
critical_roots = np.roots(first_derivative)
critical_in_domain = sorted(
    [float(root.real) for root in critical_roots
     if abs(root.imag) < 1e-7 and 0 <= root.real <= 65]
)

if critical_in_domain:
    for root in critical_in_domain:
        p_value = float(model(root))
        kind = "local maximum" if second_derivative(root) < 0 else "local minimum"
        st.write(
            f"- The model has a **{kind}** around the year **{year_label(root)}**, "
            f"at an estimated population of **{people(p_value)}**."
        )
else:
    st.write(
        "The cubic model has no local maximum or local minimum inside the observed years "
        "(1960–2025). This means the fitted curve does not turn around during the data period."
    )

# Increasing/decreasing intervals based on derivative sign.
test_points = [0] + critical_in_domain + [65]
interval_descriptions = []
for left, right in zip(test_points[:-1], test_points[1:]):
    midpoint = (left + right) / 2
    if first_derivative(midpoint) > 0:
        interval_descriptions.append(
            f"from about {year_label(left)} to {year_label(right)}, the model is increasing"
        )
    else:
        interval_descriptions.append(
            f"from about {year_label(left)} to {year_label(right)}, the model is decreasing"
        )
st.write("**Increasing or decreasing:** " + "; ".join(interval_descriptions) + ".")

# Fastest increase/decrease: extrema of derivative on [0, 65].
rate_candidates = [0.0, 65.0]
if abs(coefficients[0]) > 1e-12:
    derivative_vertex = -coefficients[1] / (3 * coefficients[0])
    if 0 <= derivative_vertex <= 65:
        rate_candidates.append(float(derivative_vertex))

rates = [(point, float(first_derivative(point))) for point in rate_candidates]
fastest_increase = max(rates, key=lambda item: item[1])
fastest_decrease = min(rates, key=lambda item: item[1])

st.write(
    f"**Fastest modeled increase:** around **{year_label(fastest_increase[0])}**, "
    f"at approximately **{rate(fastest_increase[1])}**."
)
if fastest_decrease[1] < 0:
    st.write(
        f"**Fastest modeled decrease:** around **{year_label(fastest_decrease[0])}**, "
        f"at approximately **{rate(fastest_decrease[1])}**."
    )
else:
    st.write(
        "The model does not predict a decrease during 1960–2025. "
        f"Its smallest growth rate in that period is around **{year_label(fastest_decrease[0])}**, "
        f"at approximately **{rate(fastest_decrease[1])}**."
    )

# Zeros of population model
model_roots = np.roots(model)
real_zeros = [
    float(root.real) for root in model_roots
    if abs(root.imag) < 1e-7 and 0 <= root.real <= 65
]
if real_zeros:
    st.write("**Zeros:** The model reaches a population of zero at " +
             ", ".join(year_label(root) for root in real_zeros) + ".")
else:
    st.write(
        "**Zeros:** There are no real zeros in the observed domain. "
        "That makes sense because Nicaragua's population stayed above zero throughout the data period."
    )

st.write(
    "**Domain for this project:** 1960 through 2025, because those are the years in the raw data. "
    "The model can be evaluated outside this interval, but predictions farther away become less reliable."
)
observed_min = float(np.min(y))
observed_max = float(np.max(y))
st.write(
    f"**Observed population range:** {people(observed_min)} to {people(observed_max)}. "
    "This is the range of the actual data, not necessarily the full mathematical range of the cubic equation."
)

st.divider()
st.header("4. What might explain population changes?")
st.write(
    "The data show a long-term increase in Nicaragua's population. Population can change because "
    "of birth rates, death rates, life expectancy, migration, public health, economic conditions, "
    "and major historical events."
)
st.write(
    "Nicaragua experienced major events during this period, including the 1972 Managua earthquake, "
    "the revolution and civil conflict around the late 1970s and 1980s, and later periods of political "
    "and economic change. These events may have affected where people lived, their access to services, "
    "and migration. However, this population graph by itself cannot prove that any one event caused "
    "a particular change. More research would be needed to establish a direct connection."
)

st.divider()
st.header("5. Extrapolation: predicting a future population")
prediction_year = st.number_input(
    "Choose a future year (after 2025)",
    min_value=2026, max_value=2100, value=2030, step=1
)
prediction_x = prediction_year - 1960
prediction = float(model(prediction_x))
annual_rate = float(first_derivative(prediction_x))

st.metric(f"Model prediction for {int(prediction_year)}", people(prediction))
st.write(
    f"According to this cubic regression model, Nicaragua's population in {int(prediction_year)} "
    f"would be approximately **{people(prediction)}**. At that year, the model's estimated rate "
    f"of change is about **{rate(annual_rate)}**."
)
st.warning(
    "This is a mathematical extrapolation, not an official population forecast. "
    "A cubic curve can behave unrealistically far beyond the years used to build it. "
    "Actual population will depend on future births, deaths, and migration."
)

st.divider()
st.header("6. Conclusion")
st.write(
    "The historical data show that Nicaragua's population grew substantially between 1960 and 2025. "
    "The cubic regression curve gives one mathematical way to describe that pattern. The model is "
    "useful for analyzing growth and making a short-term estimate, but it should not be treated as "
    "a guarantee of what will happen in the future. Population is connected to Nicaragua's national "
    "development because it influences the country's workforce, communities, public services, and economy."
)

st.divider()
st.header("Sources")
st.markdown(
    "- [World Bank – Population, total: Nicaragua (SP.POP.TOTL)]"
    "(https://data.worldbank.org/indicator/SP.POP.TOTL?locations=NI)\n"
    "- [World Bank – Nicaragua country data](https://data.worldbank.org/country/NI)\n"
    "- [United Nations – World Population Prospects](https://population.un.org/wpp/)"
)
st.caption(
    "Before submitting, review the data source and the model analysis with your teacher. "
    "The regression equation and all calculated analysis are generated from the data shown above."
)
