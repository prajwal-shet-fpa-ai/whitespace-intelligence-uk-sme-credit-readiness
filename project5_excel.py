import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter

# Load data
df = pd.read_csv('whitespace_sme_data.csv')
benchmark = pd.read_csv('whitespace_benchmark.csv')
benchmark = benchmark.rename(columns={'Unnamed: 0': 'sector'})

# Styles
hf   = Font(name="Arial", bold=True, color="FFFFFF", size=11)
hfil = PatternFill("solid", start_color="1F3864")
nf   = Font(name="Arial", size=10)
bf   = Font(name="Arial", bold=True, size=10)
tf   = Font(name="Arial", bold=True, size=14, color="1F3864")
ntf  = Font(name="Arial", italic=True, size=9, color="595959")
ctr  = Alignment(horizontal="center")
gf   = PatternFill("solid", start_color="EAF3DE")
af   = PatternFill("solid", start_color="FFF2CC")
rf   = PatternFill("solid", start_color="FFE0E0")
blf  = PatternFill("solid", start_color="BDD7EE")
sbf  = PatternFill("solid", start_color="EEF4FB")

wb = Workbook()

# ── SHEET 1: EXECUTIVE SUMMARY ────────────────────────────
ws1 = wb.active
ws1.title = "Executive Summary"

ws1['A1'] = "Whitespace Intelligence — UK SME Funding Readiness Report"
ws1['A1'].font = tf
ws1.merge_cells('A1:F1')
ws1.row_dimensions[1].height = 30

ws1['A2'] = "Prepared by: Whitespace Intelligence Platform  |  Confidential"
ws1['A2'].font = ntf
ws1.merge_cells('A2:F2')

# Key metrics
metrics = [
    ("Total SMEs Analysed", len(df)),
    ("High Risk SMEs", len(df[df['risk_band']=='High Risk'])),
    ("Medium Risk SMEs", len(df[df['risk_band']=='Medium Risk'])),
    ("Portfolio Avg Readiness", f"{df['readiness_score'].mean():.1f}/100"),
    ("Below Fundable Threshold", f"{len(df[df['readiness_score']<50])} ({len(df[df['readiness_score']<50])}%)"),
    ("Best Performing Sector", benchmark.loc[benchmark['avg_readiness'].idxmax(), 'sector']),
    ("Worst Performing Sector", benchmark.loc[benchmark['avg_readiness'].idxmin(), 'sector']),
]

ws1['A4'] = "KEY METRICS"
ws1['A4'].font = Font(name="Arial", bold=True, size=12, color="1F3864")

for i, (label, value) in enumerate(metrics, start=5):
    ws1.cell(row=i, column=1, value=label).font = bf
    ws1.cell(row=i, column=2, value=str(value)).font = nf
    ws1.cell(row=i, column=1).fill = sbf
    ws1.cell(row=i, column=2).fill = sbf

# CxO conclusions
ws1['A13'] = "CxO SECTOR CONCLUSIONS"
ws1['A13'].font = Font(name="Arial", bold=True, size=12, color="1F3864")

for i, (_, row) in enumerate(benchmark.iterrows(), start=14):
    score = row['avg_readiness']
    if score < 45:
        status = f"CRITICAL — {row['sector']}: {score:.1f}/100. Urgent intervention needed."
        fill = rf
    elif score < 55:
        status = f"AT RISK — {row['sector']}: {score:.1f}/100. Coaching recommended."
        fill = af
    else:
        status = f"STABLE — {row['sector']}: {score:.1f}/100. Monitor and maintain."
        fill = gf
    c = ws1.cell(row=i, column=1, value=status)
    c.font = nf
    c.fill = fill
    ws1.merge_cells(f'A{i}:F{i}')

# Insert dashboard chart
try:
    img = XLImage('whitespace_dashboard.png')
    img.width  = 600
    img.height = 360
    ws1.add_image(img, 'A23')
except:
    print("Chart image not found — skipping")

ws1.column_dimensions['A'].width = 50
ws1.column_dimensions['B'].width = 25

# ── SHEET 2: FULL SME DATA ────────────────────────────────
ws2 = wb.create_sheet("SME Data")

headers = list(df.columns)
for col, h in enumerate(headers, 1):
    c = ws2.cell(row=1, column=col, value=h)
    c.font = hf
    c.fill = hfil
    c.alignment = ctr

for i, (_, row) in enumerate(df.iterrows(), start=2):
    for col, val in enumerate(row, 1):
        c = ws2.cell(row=i, column=col, value=val)
        c.font = nf
        if row['risk_band'] == 'High Risk':
            c.fill = rf
        elif row['risk_band'] == 'Medium Risk':
            c.fill = af

for col in range(1, len(headers)+1):
    ws2.column_dimensions[get_column_letter(col)].width = 18

# ── SHEET 3: SECTOR BENCHMARK ─────────────────────────────
ws3 = wb.create_sheet("Sector Benchmark")

ws3['A1'] = "Sector Benchmark Analysis"
ws3['A1'].font = tf
ws3.merge_cells('A1:F1')

bench_headers = list(benchmark.columns)
for col, h in enumerate(bench_headers, 1):
    c = ws3.cell(row=2, column=col, value=h)
    c.font = hf
    c.fill = hfil
    c.alignment = ctr

for i, (_, row) in enumerate(benchmark.iterrows(), start=3):
    for col, val in enumerate(row, 1):
        c = ws3.cell(row=i, column=col, value=val)
        c.font = nf
        if row['avg_readiness'] < 45:
            c.fill = rf
        elif row['avg_readiness'] < 55:
            c.fill = af
        else:
            c.fill = gf

for col in range(1, len(bench_headers)+1):
    ws3.column_dimensions[get_column_letter(col)].width = 20

# Save
output = 'Whitespace_SME_Funding_Report.xlsx'
wb.save(output)
print(f"Excel report saved: {output}")
print("Sheets: Executive Summary, SME Data, Sector Benchmark")