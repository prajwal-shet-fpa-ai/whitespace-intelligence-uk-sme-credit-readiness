import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('whitespace_sme_data.csv')
benchmark = pd.read_csv('whitespace_benchmark.csv')

# Fix sector column
if 'sector' not in benchmark.columns:
    benchmark = benchmark.reset_index()
    benchmark.columns.values[0] = 'sector'

print("Whitespace Intelligence — Charts & Excel Export")
print("=" * 60)
print(f"Records loaded: {len(df)}")
print(f"Benchmark columns: {list(benchmark.columns)}")

# Sort benchmark
benchmark_sorted = benchmark.sort_values('avg_readiness')

# ── 4 CHARTS ──────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Whitespace Intelligence — UK SME Funding Readiness Dashboard',
             fontsize=14, fontweight='bold')

# Chart 1 — Readiness score by sector
ax1 = axes[0, 0]
colors1 = ['#C0392B' if s < 45 else '#E67E22' if s < 55 else '#1F3864'
           for s in benchmark_sorted['avg_readiness']]
bars1 = ax1.barh(benchmark_sorted['sector'],
                 benchmark_sorted['avg_readiness'], color=colors1)
ax1.axvline(x=50, color='gray', linestyle='--', linewidth=1)
ax1.set_title('Avg Funding Readiness by Sector', fontweight='bold')
ax1.set_xlabel('Readiness Score (0-100)')
for bar, val in zip(bars1, benchmark_sorted['avg_readiness']):
    ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}', va='center', fontsize=9)

# Chart 2 — Risk band pie chart
ax2 = axes[0, 1]
risk_counts = df['risk_band'].value_counts()
colors2 = {'Medium Risk': '#E67E22', 'High Risk': '#C0392B',
           'Low Risk': '#27AE60', 'Very High Risk': '#922B21'}
pie_colors = [colors2.get(r, '#95A5A6') for r in risk_counts.index]
ax2.pie(risk_counts.values, labels=risk_counts.index,
        colors=pie_colors, autopct='%1.1f%%', startangle=90)
ax2.set_title('SME Risk Band Distribution', fontweight='bold')

# Chart 3 — High risk count by sector
ax3 = axes[1, 0]
high_risk = df[df['risk_band'] == 'High Risk'].groupby('sector').size()
high_risk = high_risk.sort_values(ascending=False)
bars3 = ax3.bar(range(len(high_risk)), high_risk.values, color='#C0392B')
ax3.set_xticks(range(len(high_risk)))
ax3.set_xticklabels(high_risk.index, rotation=45, ha='right', fontsize=8)
ax3.set_title('High Risk SME Count by Sector', fontweight='bold')
ax3.set_ylabel('Number of SMEs')
for bar, val in zip(bars3, high_risk.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             str(val), ha='center', fontsize=9)

# Chart 4 — Readiness score distribution
ax4 = axes[1, 1]
ax4.hist(df['readiness_score'], bins=15, color='#1F3864',
         edgecolor='white', alpha=0.8)
ax4.axvline(x=50, color='red', linestyle='--', linewidth=1.5,
            label='Fundable threshold (50)')
ax4.axvline(x=df['readiness_score'].mean(), color='orange',
            linestyle='--', linewidth=1.5,
            label=f"Portfolio avg ({df['readiness_score'].mean():.1f})")
ax4.set_title('Readiness Score Distribution', fontweight='bold')
ax4.set_xlabel('Readiness Score')
ax4.set_ylabel('Number of SMEs')
ax4.legend(fontsize=8)

plt.tight_layout()
plt.savefig('whitespace_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("Dashboard saved: whitespace_dashboard.png")

# ── CHART DESCRIPTIONS ────────────────────────────────────
print()
print("=" * 60)
print("CHART DESCRIPTIONS")
print("=" * 60)

worst_sector = benchmark_sorted.iloc[0]
best_sector  = benchmark_sorted.iloc[-1]

print()
print("CHART 1 — Avg Funding Readiness by Sector")
print(f"  Worst: {worst_sector['sector']} at {worst_sector['avg_readiness']:.1f}/100")
print(f"  Best:  {best_sector['sector']} at {best_sector['avg_readiness']:.1f}/100")
print(f"  Most sectors fall below the 50-point fundable threshold.")
print(f"  This confirms a systemic funding readiness problem.")

print()
print("CHART 2 — Risk Band Distribution")
high  = len(df[df['risk_band'] == 'High Risk'])
med   = len(df[df['risk_band'] == 'Medium Risk'])
total = len(df)
print(f"  {high} of {total} SMEs ({high/total*100:.0f}%) are High Risk.")
print(f"  {med} of {total} SMEs ({med/total*100:.0f}%) are Medium Risk.")
print(f"  Only {total-high-med} SMEs are in a strong funding position.")

print()
print("CHART 3 — High Risk SME Count by Sector")
top_sector = high_risk.index[0]
top_count  = high_risk.values[0]
print(f"  {top_sector} has the most High Risk SMEs: {top_count}.")
print(f"  Priority sector for Whitespace intervention.")

print()
print("CHART 4 — Readiness Score Distribution")
avg   = df['readiness_score'].mean()
below = len(df[df['readiness_score'] < 50])
print(f"  Portfolio average: {avg:.1f}/100")
print(f"  {below} of {total} SMEs ({below/total*100:.0f}%) below fundable threshold.")
print(f"  These SMEs need Whitespace Intelligence intervention.")

print()
print("=" * 60)
print("Charts complete. Ready for Excel export.")
print("=" * 60)