# Systemic Risk and Financial Contagion in the Nigerian Banking Sector

A Multi-Regime Network Analysis of the Five Domestic Systemically Important Banks (2008–2024)

Samuel Babatunde Folorunsho Ajakaiye | Student Group 16011 | MScFE 690 Capstone | WorldQuant University | July 2026

## What this project does

I map a time-varying DCC-GARCH interconnectedness network, with Delta CoVaR supplying the edge weights, across the five(5) Nigerian domestic systemically important banks (D-SIBs);First Bank, GTBank/GTCO, Zenith, Access, and UBA. Onto this network I test a fiscal transmission channel that is my own construction, one that links Brent crude oil prices, monthly Federation Account Allocation Committee (FAAC) disbursements, and CBN external reserves to banking-system connectedness. I must however account for the government's own hand in these stress signals, and I do this with five(5) binary institutional dummies: the year 2009 to year 2011 interbank guarantee, AMCON operations, the multi-window FX regime, COVID-19 forbearance, and the June year 2023 FX unification. Without these controls, what looks like market stress in my data could just as easily be the residue of policy — these five(5) dummies exist to keep that distinction clear
## Repository structure

```
├── ngx_data_validation.ipynb        Original data-prep notebook: loads raw price CSVs,
│                                     splices predecessor/successor tickers, computes log
│                                     returns, and produces a data-quality report
├── nigerian_banking_contagion.ipynb Main research notebook: corporate-action verification,
│                                     univariate GARCH(1,1)-t / GJR-GARCH(1,1)-t comparison,
│                                     and DCC(1,1) estimation. Executed with outputs saved —
│                                     opens showing real tables and charts, no re-run required.
├── data/
│   └── raw/
│       ├── ngx_prices.csv                          Daily prices, five banks, 2012–2024
│       │                                            (source: Investing.com)
│       └── HISTORICAL_EQUITY_DATA__2005--2012.xlsx  Daily prices, five banks, 2008–2012
│                                                     (source: NGX academic data request)
├── outputs/
│   ├── corporate_action_verification_log.csv   Real, cited in the Project Proposal
│   ├── univariate_garch_gjr_comparison.csv     Real, cited in the Project Proposal
│   ├── dcc_parameters.csv                      Real, cited in the Project Proposal
│   ├── dcc_mean_pairwise_correlation.csv       Real, cited in the Project Proposal
│   ├── table1_delta_covar_matrix.csv           Placeholder — see note below, NOT cited
│   ├── table2_centrality_by_regime.csv         Placeholder — see note below, NOT cited
│   └── figures/                                The four charts embedded in the Proposal
└── requirements.txt                 Python dependencies
```

## How to run

1. Clone or download this repository.
2. Install dependencies: `pip install -r requirements.txt` (Python 3.10+).
3. Open `nigerian_banking_contagion.ipynb` in Jupyter, VS Code, or Google Colab
   and run all cells top to bottom. The notebook reads from `data/raw/` using
   relative paths.
4. Expected result: a merged sample of 4,208 daily trading days (4,193 complete
   rows across all five banks) spanning 2008-01-03 to 2024-12-31.

`ngx_data_validation.ipynb` remains in the repository as the original data-prep
notebook for the 2012–2024 segment; its logic has since been superseded by the
merge cell in `nigerian_banking_contagion.ipynb`, which also incorporates the
2008–2012 NGX segment.

## Data sources

| Series | Source | Status |
|---|---|---|
| Daily equity prices, five D-SIBs (2012–2024) | Investing.com (NGX-listed equities) | Collected and validated |
| Daily equity prices, five D-SIBs (2008–2012) | Nigerian Exchange (NGX) academic data request | **Received and merged** |
| Monthly FAAC disbursements | FAAC / National Bureau of Statistics publications | Next stage — placeholder data in use |
| Brent crude oil prices | U.S. EIA / FRED | Next stage — placeholder data in use |
| CBN external reserves | Central Bank of Nigeria statistics database | Next stage — placeholder data in use |
| Parallel market FX premium | AbokiFX / CBN BDC rates | Next stage — placeholder data in use |
| Bank-level annual oil & gas loan exposure | Audited annual reports, NGX-listed D-SIBs | Next stage — placeholder data in use |

Ticker continuity: GUARANTY→GTCO (2021 holdco restructuring), ACCESS→ACCESSCORP
(2022 holdco; Diamond Bank merger 2019), and FIRSTBANK→FBNH→FIRSTHOLDCO are
spliced into single continuous series per bank, with the return on each
transition date excluded. The NGX (2008–2012) and Investing.com (2012–2024)
segments are spliced at January 2013 with no return computed across the
boundary; validated against 233 common trading days in the 2012 overlap
window at per-bank correlations of 0.992–1.000.

## Data-readiness flags — read before citing any number

`nigerian_banking_contagion.ipynb` sets three independent flags in its Global
Research Parameters cell, since the underlying source series were not all
collected on the same timeline:

```python
USE_SYNTHETIC_EQUITY    = False   # Real: the five D-SIBs' daily returns, 2008–2024
USE_SYNTHETIC_MACRO     = True    # Placeholder: FAAC, Brent, reserves, parallel premium
USE_SYNTHETIC_OIL_PANEL = True    # Placeholder: bank-level annual oil & gas loan exposure
```

Every number reported as a finding in the Project Proposal is equity-only and
real-data-backed. `table1_delta_covar_matrix.csv` and `table2_centrality_by_regime.csv`
in `outputs/` are produced by the pre-existing network-estimation cells, which
still run on the placeholder macro/oil series — they are pipeline smoke-test
output, not research findings, and are not cited anywhere in the Proposal.

## Preliminary results (real data, as of this commit)

- **Corporate-action scan**: 24 flagged outlier returns (|move| > 12%) across
  the full 2008–2024 panel. 16 cluster in the March/April dividend season and
  are treated (same-day cross-sectional mean replacement); 8 cluster in the
  2008–2009 global financial crisis window and are retained as genuine
  crisis-period market moves.
- **GARCH(1,1)-t vs. GJR-GARCH(1,1)-t**: BIC prefers the symmetric
  specification for all five banks, including across the GFC episode — the
  leverage/asymmetry effect is rejected.
- **DCC(1,1)**, two-stage MLE with correlation targeting: α ≈ 0.038, β ≈ 0.904,
  α + β ≈ 0.942 — the correlation process sits comfortably inside the
  stationary region even though the univariate GARCH variances sit at the
  integrated boundary (α + β ≈ 1.000 for four of five banks).

**Note on precision**: the BIC values printed by this notebook differ slightly
from the table in the Project Proposal document (e.g. FIRSTBANK BIC ≈ 19,255
here vs. ≈ 19,189 in the document); the DCC parameters agree at the precision
reported there. The gap traces to the corporate-action treatment logic having
been iterated separately in the notebook and in a verification script across
sessions. The qualitative conclusion — symmetric GARCH preferred for every
bank — is unaffected. Reconciling the two to exact agreement is an open
housekeeping task.

## Model scope boundary statement

The committed scope of this research, as agreed with the course instructor,
comprises: (1) the DCC-GARCH / Delta CoVaR network with eigenvector centrality
rankings compared across regime periods; (2) the FAAC fiscal transmission
channel tested by Granger causality within a distributed-lag VAR; and (3) the
five institutional dummy controls.

The following are explicitly designated future work and are not yet
implemented on real data: the bank-level crude-oil loan exposure panel, the
parallel-market FX premium early-warning variable, and maximum-entropy
robustness checks. A stated limitation follows from the first exclusion:
without the oil-exposure panel, common factor exposure and bilateral
contagion cannot be fully separated, and the results are interpreted
accordingly.

**Known data limitations**: NGX equities exhibit thin trading (10–15%
zero-return days) and daily price limits (±10%) that censor extreme
single-day returns. One corporate-action flag (UBA, 2015-09-10) remains
unverified — it falls outside the dividend season with no explanatory
calendar gap, and may instead reflect the JP Morgan GBI-EM index exclusion
sell-off of that period rather than a corporate action; it is retained
untreated pending confirmation either way.

## Project status

- [x] Data acquisition and validation, five banks, 2012–2024
- [x] NGX historical extension, 2008–2012 — received and merged
- [x] Corporate-action scan and verification (24 flags, 16 treated, 8 retained)
- [x] Univariate GARCH(1,1)-t estimation per bank
- [x] GJR-GARCH(1,1)-t asymmetry check (symmetric preferred, all five banks)
- [x] DCC(1,1) estimation (two-stage MLE, converged)
- [ ] Delta CoVaR network construction
- [ ] Regime-period centrality comparison
- [ ] FAAC transmission channel VAR and Granger causality tests
- [ ] Bank-level oil-exposure panel and Wald heterogeneity test
- [ ] Institutional dummy augmentation
- [ ] Final report and presentation

Contact <samuel@teledinamik.com.ng>
