import sqlite3

import pandas as pd

print("Whitespace Intelligence — SQL Analysis")
print("=" * 60)

# Load the data created by project5.py into a SQLite database
sme = pd.read_csv("whitespace_sme_data.csv")
benchmark = pd.read_csv("whitespace_benchmark.csv")

conn = sqlite3.connect("whitespace_sme.db")
sme.to_sql("sme_data", conn, if_exists="replace", index=False)
benchmark.to_sql("sector_benchmark", conn, if_exists="replace", index=False)
print(f"Loaded {len(sme)} SMEs and {len(benchmark)} sectors into whitespace_sme.db")


def run(title, query):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(pd.read_sql_query(query, conn).to_string(index=False))


# Query 1: SMEs grouped by risk band with average readiness and revenue
run("QUERY 1: SMEs BY RISK BAND", """
    SELECT risk_band,
           COUNT(*)                          AS sme_count,
           ROUND(AVG(readiness_score), 1)    AS avg_readiness,
           ROUND(AVG(annual_revenue_gbp), 0) AS avg_revenue_gbp
    FROM sme_data
    GROUP BY risk_band
    ORDER BY avg_readiness DESC
""")

# Query 2: Worst performing sectors by funding readiness
run("QUERY 2: SECTORS BY FUNDING READINESS (WEAKEST FIRST)", """
    SELECT sector,
           COUNT(*)                                                  AS sme_count,
           ROUND(AVG(readiness_score), 1)                            AS avg_readiness,
           SUM(CASE WHEN readiness_score < 50 THEN 1 ELSE 0 END)     AS below_50
    FROM sme_data
    GROUP BY sector
    ORDER BY avg_readiness ASC
""")

# Query 3: Quick wins, SMEs just below the fundable level of 50
run("QUERY 3: QUICK WINS (SCORE 45 TO 49, CLOSE TO FUNDABLE)", """
    SELECT sme_id,
           sector,
           readiness_score,
           credit_score,
           years_trading,
           cash_flow_score,
           debt_ratio
    FROM sme_data
    WHERE readiness_score BETWEEN 45 AND 49
    ORDER BY readiness_score DESC, cash_flow_score ASC
""")

conn.close()
print()
print("SQL analysis complete.")
