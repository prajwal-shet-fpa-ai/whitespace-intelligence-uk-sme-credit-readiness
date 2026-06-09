import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

print("Whitespace Intelligence — UK SME Funding Readiness Analysis")
print("=" * 60)

# Sectors
sectors = {
    'Retail':                {'avg_revenue': 420000, 'funding_success_rate': 0.38},
    'Hospitality':           {'avg_revenue': 310000, 'funding_success_rate': 0.29},
    'Professional Services': {'avg_revenue': 580000, 'funding_success_rate': 0.61},
    'Manufacturing':         {'avg_revenue': 750000, 'funding_success_rate': 0.52},
    'Technology':            {'avg_revenue': 490000, 'funding_success_rate': 0.67},
    'Construction':          {'avg_revenue': 620000, 'funding_success_rate': 0.44},
    'Healthcare':            {'avg_revenue': 380000, 'funding_success_rate': 0.55},
    'Food & Beverage':       {'avg_revenue': 280000, 'funding_success_rate': 0.31},
}

# Generate 100 SMEs
sector_list = list(sectors.keys())
records = []

for i in range(1, 101):
    sector_name = random.choice(sector_list)
    profile     = sectors[sector_name]

    revenue         = max(50000, int(np.random.normal(profile['avg_revenue'], profile['avg_revenue'] * 0.3)))
    credit_score    = max(300, min(850, int(np.random.normal(580, 120))))
    years_trading   = random.randint(1, 20)
    cash_flow_score = random.randint(1, 10)
    debt_ratio      = round(random.uniform(0.1, 0.8), 2)

    score = 0
    score += min(25, int((credit_score - 300) / 22))
    score += min(20, int(years_trading * 1.5))
    score += min(20, cash_flow_score * 2)
    score += min(15, int((1 - debt_ratio) * 15))
    score += min(10, int(revenue / 100000))
    score  = max(0, min(100, score))

    if score >= 75:   risk_band = 'Low Risk'
    elif score >= 50: risk_band = 'Medium Risk'
    elif score >= 25: risk_band = 'High Risk'
    else:             risk_band = 'Very High Risk'

    records.append({
        'sme_id':             f'WS{i:04d}',
        'sector':             sector_name,
        'annual_revenue_gbp': revenue,
        'credit_score':       credit_score,
        'years_trading':      years_trading,
        'cash_flow_score':    cash_flow_score,
        'debt_ratio':         debt_ratio,
        'readiness_score':    score,
        'risk_band':          risk_band,
    })

df = pd.DataFrame(records)
print(f"Generated {len(df)} SME records")

# Benchmark — sector as a column not index
benchmark = df.groupby('sector').agg(
    sme_count     = ('sme_id', 'count'),
    avg_readiness = ('readiness_score', 'mean'),
    avg_revenue   = ('annual_revenue_gbp', 'mean'),
    avg_credit    = ('credit_score', 'mean'),
).round(1).reset_index()

benchmark = benchmark.sort_values('avg_readiness', ascending=False)

print()
print("=" * 60)
print("SECTOR BENCHMARK")
print("=" * 60)
print(benchmark.to_string(index=False))

# CxO conclusions
print()
print("=" * 60)
print("CxO ONE-LINE CONCLUSIONS")
print("=" * 60)

for _, row in benchmark.iterrows():
    sector = row['sector']
    score  = row['avg_readiness']
    if score < 45:
        print(f"CRITICAL — {sector}: avg readiness {score:.1f}/100. Urgent support needed.")
    elif score < 55:
        print(f"AT RISK — {sector}: avg readiness {score:.1f}/100. Coaching recommended.")
    else:
        print(f"STABLE — {sector}: avg readiness {score:.1f}/100. Monitor and maintain.")

# Export
df.to_csv('whitespace_sme_data.csv', index=False)
benchmark.to_csv('whitespace_benchmark.csv', index=False)

print()
print("=" * 60)
print("DATA EXPORTED")
print("=" * 60)
print("whitespace_sme_data.csv — 100 SME records")
print("whitespace_benchmark.csv — sector benchmark with sector column")
print()
print("Part 1 complete.")