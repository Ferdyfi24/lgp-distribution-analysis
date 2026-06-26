# ============================================================
# LPG Distribution Efficiency Analysis (Dec 2024 – May 2026)
# Pertamina-Authorized LPG 3kg Sub-Agent | Tanah Datar, West Sumatra
# Author: Ferdy Febrian Iskandar
# Tools: Python, Pandas, NumPy, Matplotlib, Seaborn
# ============================================================

# CELL 1: Install & Import
# -------------------------
# !pip install pandas numpy matplotlib seaborn  # uncomment if needed

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
print("✅ Libraries loaded.")

# CELL 2: Generate Realistic Simulation Dataset
# ----------------------------------------------
# Business context:
# - 25 retailer outlets + 225 individual buyers = 250 accounts
# - ~2,000 cylinders/month total
# - Return rate ~1% per cycle (leaking/defective cylinders)
# - Period: Dec 2024 – May 2026 (18 months)

MONTHS = pd.date_range(start='2024-12-01', end='2026-05-01', freq='MS')
N_MONTHS = len(MONTHS)

RETAILERS = [f'Toko_{i:02d}' for i in range(1, 26)]
AREAS = {
    'Area_A': RETAILERS[:8],   # Urban core — high demand, competitive
    'Area_B': RETAILERS[8:17], # Semi-urban — moderate demand
    'Area_C': RETAILERS[17:],  # Rural fringe — uneven demand
}
AREA_MAP = {shop: area for area, shops in AREAS.items() for shop in shops}

# Demand pattern: uneven across areas and months
AREA_BASE = {'Area_A': 55, 'Area_B': 38, 'Area_C': 22}  # avg cylinders/retailer/month
SEASONAL_FACTOR = {12: 1.15, 1: 1.18, 2: 1.10, 3: 1.00,
                   4: 0.95, 5: 0.92, 6: 0.90, 7: 0.88,
                   8: 0.90, 9: 0.95, 10: 1.00, 11: 1.08}

rows = []
for month in MONTHS:
    sf = SEASONAL_FACTOR[month.month]
    for shop in RETAILERS:
        area = AREA_MAP[shop]
        base = AREA_BASE[area]
        demand = max(5, int(np.random.normal(base * sf, base * 0.18)))
        fulfilled = min(demand, int(demand * np.random.uniform(0.88, 1.0)))
        returns = max(0, int(fulfilled * np.random.uniform(0.002, 0.009)))  # ~0.5% return rate
        delivery_days = int(np.random.normal(
            1.5 if area == 'Area_A' else 2.2 if area == 'Area_B' else 3.1, 0.6
        ))
        delivery_days = max(1, delivery_days)
        rows.append({
            'month': month,
            'retailer': shop,
            'area': area,
            'demand_qty': demand,
            'fulfilled_qty': fulfilled,
            'return_qty': returns,
            'delivery_days': delivery_days,
            'fulfillment_rate': round(fulfilled / demand * 100, 2),
        })

df = pd.DataFrame(rows)

# Individual buyers: 225 buyers, distributed across months
buyer_rows = []
for month in MONTHS:
    n_buyers = int(np.random.normal(225, 15))
    for _ in range(n_buyers):
        qty = np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10])
        buyer_rows.append({'month': month, 'qty': qty})
buyers_df = pd.DataFrame(buyer_rows)

print(f"✅ Dataset generated: {len(df)} retailer-month records | {len(buyers_df)} buyer transactions")
print(f"   Period: {MONTHS[0].strftime('%b %Y')} – {MONTHS[-1].strftime('%b %Y')} ({N_MONTHS} months)")
print(df.head())

# CELL 3: Summary Statistics
# ---------------------------
total_demand    = df['demand_qty'].sum()
total_fulfilled = df['fulfilled_qty'].sum()
total_returns   = df['return_qty'].sum()
avg_fulfillment = df['fulfillment_rate'].mean()
avg_return_rate = (total_returns / total_fulfilled * 100)
avg_delivery    = df['delivery_days'].mean()

print("\n" + "="*55)
print("📋 OPERATIONAL SUMMARY (Dec 2024 – May 2026)")
print("="*55)
print(f"  Total Demand          : {total_demand:,} cylinders")
print(f"  Total Fulfilled       : {total_fulfilled:,} cylinders")
print(f"  Total Returns         : {total_returns:,} cylinders")
print(f"  Avg Fulfillment Rate  : {avg_fulfillment:.1f}%")
print(f"  Avg Return Rate       : {avg_return_rate:.2f}% per cycle")
print(f"  Avg Delivery Time     : {avg_delivery:.1f} days")

# CELL 4: Plot 1 — Monthly Demand vs Fulfillment
# ------------------------------------------------
monthly = df.groupby('month')[['demand_qty', 'fulfilled_qty', 'return_qty']].sum().reset_index()

fig, ax1 = plt.subplots(figsize=(14, 5))
x = range(len(monthly))
ax1.bar(x, monthly['demand_qty'], color='#90CAF9', label='Demand', width=0.4, align='center')
ax1.bar([i+0.4 for i in x], monthly['fulfilled_qty'], color='#1565C0', label='Fulfilled', width=0.4, align='center')
ax1.set_xticks([i+0.2 for i in x])
ax1.set_xticklabels([m.strftime('%b\n%Y') for m in monthly['month']], fontsize=8)
ax1.set_ylabel('Cylinders', fontsize=10)
ax1.set_title('Monthly LPG Demand vs Fulfillment (Dec 2024 – May 2026)', fontsize=13, fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(axis='y', alpha=0.3)
ax1.spines[['top','right']].set_visible(False)

ax2 = ax1.twinx()
ax2.plot([i+0.2 for i in x], monthly['return_qty'], color='#E53935', marker='o',
         linewidth=1.8, markersize=5, label='Returns')
ax2.set_ylabel('Return Qty', color='#E53935', fontsize=10)
ax2.tick_params(axis='y', colors='#E53935')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig('plot1_demand_fulfillment.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: plot1_demand_fulfillment.png")

# CELL 5: Plot 2 — Demand Variance by Area (Uneven Demand)
# ----------------------------------------------------------
area_monthly = df.groupby(['month','area'])['demand_qty'].sum().reset_index()

fig, ax = plt.subplots(figsize=(14, 5))
palette = {'Area_A': '#1565C0', 'Area_B': '#FB8C00', 'Area_C': '#43A047'}
for area, color in palette.items():
    subset = area_monthly[area_monthly['area'] == area]
    ax.plot(subset['month'], subset['demand_qty'], marker='o', label=area,
            color=color, linewidth=2, markersize=5)

ax.set_title('Monthly Demand by Area — Identifying Uneven Distribution Patterns', fontsize=13, fontweight='bold')
ax.set_ylabel('Total Cylinders Demanded', fontsize=10)
ax.set_xlabel('Month', fontsize=10)
ax.legend(title='Coverage Area')
ax.grid(alpha=0.3)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('plot2_demand_by_area.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: plot2_demand_by_area.png")

# CELL 6: Plot 3 — Return Rate Analysis per Area
# ------------------------------------------------
return_by_area = df.groupby('area').agg(
    total_fulfilled=('fulfilled_qty','sum'),
    total_returns=('return_qty','sum')
).reset_index()
return_by_area['return_rate'] = (return_by_area['total_returns'] / return_by_area['total_fulfilled'] * 100).round(2)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar: return rate per area
colors = ['#1565C0','#FB8C00','#43A047']
axes[0].bar(return_by_area['area'], return_by_area['return_rate'], color=colors, edgecolor='white')
axes[0].axhline(0.5, color='red', linestyle='--', linewidth=1.2, label='Target ≤0.5%')
for i, (_, row) in enumerate(return_by_area.iterrows()):
    axes[0].text(i, row['return_rate']+0.03, f"{row['return_rate']:.2f}%", ha='center', fontsize=10, fontweight='bold')
axes[0].set_title('Return Rate by Area (%)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Return Rate (%)')
axes[0].legend()
axes[0].set_ylim(0, 2.5)
axes[0].spines[['top','right']].set_visible(False)

# Monthly return rate trend
monthly_ret = df.groupby('month').agg(
    fulfilled=('fulfilled_qty','sum'),
    returns=('return_qty','sum')
).reset_index()
monthly_ret['rate'] = monthly_ret['returns'] / monthly_ret['fulfilled'] * 100

axes[1].plot(monthly_ret['month'], monthly_ret['rate'], color='#E53935', marker='o', linewidth=2)
axes[1].axhline(0.5, color='gray', linestyle='--', linewidth=1, label='Benchmark 0.5%')
axes[1].fill_between(monthly_ret['month'], monthly_ret['rate'], 0.5,
                     where=monthly_ret['rate']>0.5, alpha=0.2, color='red', label='Above benchmark')
axes[1].set_title('Monthly Return Rate Trend (%)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Return Rate (%)')
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)
axes[1].spines[['top','right']].set_visible(False)

plt.suptitle('LPG Cylinder Return Analysis — Leakage & Defect Tracking', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plot3_return_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: plot3_return_analysis.png")

# CELL 7: Plot 4 — Delivery Speed by Area (Competitive Positioning)
# ------------------------------------------------------------------
delivery_area = df.groupby('area')['delivery_days'].agg(['mean','std']).reset_index()
delivery_area.columns = ['area','avg_days','std_days']

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Box plot: delivery days distribution
area_order = ['Area_A','Area_B','Area_C']
data_box = [df[df['area']==a]['delivery_days'].values for a in area_order]
bp = axes[0].boxplot(data_box, labels=area_order, patch_artist=True,
                     medianprops={'color':'black','linewidth':2})
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0].set_title('Delivery Time Distribution by Area', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Delivery Days')
axes[0].grid(axis='y', alpha=0.3)
axes[0].spines[['top','right']].set_visible(False)

# Bar: avg delivery + std
axes[1].bar(delivery_area['area'], delivery_area['avg_days'], color=colors,
            yerr=delivery_area['std_days'], capsize=5, edgecolor='white')
for i, row in delivery_area.iterrows():
    axes[1].text(i, row['avg_days']+0.1, f"{row['avg_days']:.1f}d", ha='center', fontsize=10, fontweight='bold')
axes[1].set_title('Average Delivery Time by Area (days)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Days')
axes[1].set_ylim(0, 5)
axes[1].spines[['top','right']].set_visible(False)

plt.suptitle('Delivery Speed Analysis — Area Coverage Competitiveness', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plot4_delivery_speed.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: plot4_delivery_speed.png")

# CELL 8: Plot 5 — Top & Bottom Performing Retailers (Fulfillment Rate)
# ----------------------------------------------------------------------
retailer_summary = df.groupby(['retailer','area']).agg(
    avg_fulfillment=('fulfillment_rate','mean'),
    total_demand=('demand_qty','sum'),
    total_returns=('return_qty','sum')
).reset_index().sort_values('avg_fulfillment')

top5    = retailer_summary.tail(5)
bottom5 = retailer_summary.head(5)
highlight = pd.concat([bottom5, top5])

fig, ax = plt.subplots(figsize=(11, 6))
bar_colors = ['#E53935']*5 + ['#1565C0']*5
bars = ax.barh(highlight['retailer'], highlight['avg_fulfillment'], color=bar_colors, edgecolor='white')
ax.axvline(avg_fulfillment, color='gray', linestyle='--', linewidth=1, label=f'Overall avg ({avg_fulfillment:.1f}%)')
for bar, val in zip(bars, highlight['avg_fulfillment']):
    ax.text(val+0.2, bar.get_y()+bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=9)
ax.set_title('Top 5 vs Bottom 5 Retailers by Avg Fulfillment Rate', fontsize=13, fontweight='bold')
ax.set_xlabel('Average Fulfillment Rate (%)')
ax.set_xlim(80, 105)
ax.legend()
ax.grid(axis='x', alpha=0.3)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('plot5_retailer_performance.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Saved: plot5_retailer_performance.png")

# CELL 9: Final Insights
# -----------------------
print("\n" + "="*60)
print("💡 KEY OPERATIONAL INSIGHTS")
print("="*60)
print(f"\n1. DEMAND VARIANCE")
for area in ['Area_A','Area_B','Area_C']:
    subset = area_monthly[area_monthly['area']==area]['demand_qty']
    print(f"   {area}: avg {subset.mean():.0f} cyl/month | CV = {subset.std()/subset.mean()*100:.1f}%")

print(f"\n2. RETURN RATE")
for _, row in return_by_area.iterrows():
    status = '⚠️ Above target' if row['return_rate'] > 0.5 else '✅ On target'
    print(f"   {row['area']}: {row['return_rate']:.2f}% — {status}")

print(f"\n3. DELIVERY SPEED")
for _, row in delivery_area.iterrows():
    print(f"   {row['area']}: avg {row['avg_days']:.1f} days (±{row['std_days']:.1f})")

print(f"\n4. OVERALL FULFILLMENT: {avg_fulfillment:.1f}% across {N_MONTHS} months")
print("\n✅ Analysis complete. All 5 plots saved.")
