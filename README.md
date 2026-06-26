🛢️ LPG Distribution Efficiency Analysis (Dec 2024 – May 2026)
> **A Python-based operational analytics project analyzing distribution efficiency, demand variance, return rates, and delivery competitiveness of a Pertamina-authorized LPG 3kg sub-agent in Tanah Datar, West Sumatra.**
---
🎯 Project Objective
To identify operational inefficiencies in LPG distribution across 250 accounts (25 retailers + 225 individual buyers) over 18 months — with focus on demand unevenness across coverage areas, cylinder return/defect rates, and delivery speed competitiveness against neighboring agents.
---
🏢 Business Context
Entity: Pertamina-Authorized LPG 3kg Sub-Agent Distributor, Tanah Datar, West Sumatra
Scale: ~2,000 cylinders/month | 250 accounts (25 retailers + 225 individual buyers)
Period: December 2024 – May 2026 (18 months)
Key Challenges:
Uneven demand distribution across 3 coverage areas
Cylinder return rate ~0.5%/cycle (leaking/defective)
Inter-agent competition on delivery speed and area coverage
> *Dataset is simulated based on real operational experience as Distribution & Operations Staff. All figures reflect realistic operational parameters observed during the period.*
---
🛠️ Tools & Libraries
Tool	Purpose
`Python 3.10+`	Core language
`Pandas`	Data wrangling & aggregation
`NumPy`	Statistical calculations, simulation
`Matplotlib`	Bar charts, line charts, box plots
`Seaborn`	Color palettes & styling
---
📁 Project Structure
```
lgp-distribution-analysis/
│
├── lgp_distribution_analysis.py   # Main analysis script (Colab-ready)
├── README.md                       # Project documentation
│
└── outputs/
    ├── plot1_demand_fulfillment.png   # Monthly demand vs fulfillment + returns
    ├── plot2_demand_by_area.png       # Demand variance across 3 coverage areas
    ├── plot3_return_analysis.png      # Return rate by area + monthly trend
    ├── plot4_delivery_speed.png       # Delivery time distribution & avg by area
    └── plot5_retailer_performance.png # Top 5 vs bottom 5 retailers
```
---
🔍 Analyses Performed
1. Demand vs Fulfillment Tracking
Monthly comparison of total demand, fulfilled quantity, and return volume across all 250 accounts over 18 months.
2. Demand Variance by Area
Three coverage areas (Urban Core / Semi-Urban / Rural Fringe) analyzed for demand consistency using Coefficient of Variation (CV). Identifies which areas require buffer stock or priority allocation.
3. Return Rate Analysis
Return rate benchmarked at ≤0.5% per cycle
Monthly trend tracking to detect spike periods
Area-level breakdown to isolate high-defect zones
4. Delivery Speed & Competitiveness
Box plot distribution of delivery days per area
Average delivery time comparison (Area A: ~1.5d | B: ~2.2d | C: ~3.1d)
Basis for competitive positioning against neighboring agents
5. Retailer Performance Ranking
Top 5 vs bottom 5 retailers by average fulfillment rate — supports priority account management and reorder planning.
---
💡 Key Insights
(Insert your actual findings after running the script)
Example format:
Area C (Rural Fringe) showed the highest demand variance (CV ~XX%) — suggesting need for weekly demand forecasting rather than fixed monthly allocation
Return rate peaked in [Month] at X.X% — above the 1% benchmark — correlating with [seasonal factor / handling issue]
Area A retailers consistently achieved >95% fulfillment rate vs Area C at ~88% — gap driven by delivery time differential of ~1.6 days
Bottom 5 retailers concentrated in Area C — recommend priority reorder scheduling and closer monitoring
---
🚀 How to Run
Option A: Google Colab (Recommended)
Open Google Colab
Upload `lgp_distribution_analysis.py` or paste cell by cell
Run all cells → 5 charts generated automatically
Option B: Local
```bash
pip install pandas numpy matplotlib seaborn
python lgp_distribution_analysis.py
```
---
📌 CV Context
Entry (Analytical Projects section — Operations/Logistics CV):
> **LPG Distribution Efficiency Analysis** | Python, Pandas, Matplotlib | Dec 2024 – May 2026
> Analyzed 18-month distribution data across 250 accounts (~2,000 cylinders/month) for a Pertamina-authorized sub-agent; identified demand variance patterns across 3 coverage areas, tracked cylinder return rates against 1% benchmark, and benchmarked delivery speed competitiveness — generated 5 operational dashboards to support allocation and reorder planning decisions.
---
👤 Author
Ferdy Febrian Iskandar  
Management Graduate | Distribution & Operations Staff (Pertamina Sub-Agent) | Business Analytics Enthusiast  
📧 iskandarferdy559@gmail.com
---
Dataset simulated based on real operational experience. For portfolio and educational purposes only.
