"""Streamlit app."""

import duckdb
import streamlit as st

from dotenv import load_dotenv

DATABASE = "FG_DWH"
TABLE = "dbt_staging.obt_fct_tbl"

load_dotenv()

con = duckdb.connect(database=f"md:{DATABASE}", read_only=True)

st.title("Green Grid Geeks")
st.text("Insights into Finland's electricity grid.")

# power generated in the last 24 hours by type
query = f"""
WITH pivot_alias AS (
  SELECT date_value, year_value, month_value, day_value, time_value, quarter_hour,
    avg(source_value) FILTER (source_name = 'Hydroelectric Power Production') AS hydro,
    avg(source_value) FILTER (source_name = 'Wind Power Production') AS wind,
    avg(source_value) FILTER (source_name = 'Nuclear Power Production') AS nuclear,
    avg(source_value) FILTER (source_name = 'Total Electricity Production') AS total
  FROM {TABLE}
  GROUP BY ALL
)
, transform_alias AS (
  SELECT *,
    total - nuclear - hydro - wind AS other,
    make_timestamp(
      year_value,
      month_value,
      day_value,
      split_part(quarter_hour, ':', 1)::BIGINT,
      split_part(split_part(quarter_hour, ' ', 1), ':', 2)::BIGINT,
      0
    ) AS quarter_start_timestamp
  FROM pivot_alias
)
SELECT
    quarter_start_timestamp AS generated_at,
    avg(nuclear) AS nuclear,
    avg(hydro) AS hydro,
    avg(wind) AS wind,
    avg(other) AS other 
FROM transform_alias
-- random date as placeholder till we get live data
WHERE date_value = '2024-09-02'
GROUP BY ALL;
"""
df = con.execute(query).df()
st.subheader("Live Power Production")
st.bar_chart(
    data=df,
    x="generated_at",
    y=["nuclear", "hydro", "wind", "other"],
    y_label="megawatts",
    stack=True,
)

# all power generated by year-month
query = f"""
SELECT
    CONCAT(year_value, month_value) AS year_month,
    AVG(source_value) AS megawatts
FROM {TABLE}
WHERE date_value < '2025-01-01'
  AND source_name = 'Total Electricity Production'
GROUP BY CONCAT(year_value, month_value)
ORDER BY CONCAT(year_value, month_value);
"""
df = con.execute(query).df()
st.subheader("Historical Power Production")
st.line_chart(df, x="year_month", y="megawatts")

# power generated by source by year-month
source_query = "SELECT source_name FROM dbt_staging.dim_sources;"
sources = [source[0] for source in con.execute(source_query).fetchall()]
source = st.selectbox("Power source:", sources)
st.subheader(f"{source}")
query = f"""
SELECT
    CONCAT(year_value, month_value) AS year_month,
    AVG(source_value) AS megawatts
FROM {TABLE}
WHERE date_value < '2025-01-01'
  AND source_name = '{source}'
GROUP BY CONCAT(year_value, month_value)
ORDER BY CONCAT(year_value, month_value);
"""
df = con.execute(query).df()
st.line_chart(df, x="year_month", y="megawatts")
