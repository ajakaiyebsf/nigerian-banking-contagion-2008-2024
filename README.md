Systemic Risk and Financial Contagion in the Nigerian Banking Sector
A Multi-Regime Network Analysis of the Five Domestic Systemically Important Banks (2008–2024)
Samuel Babatunde Folorunsho Ajakaiye | Student Group 16011 | MScFE 690 Capstone | WorldQuant University | August 2026
What this project does
I map a time-varying DCC-GARCH interconnectedness network, with Delta CoVaR supplying the edge weights, across the five(5) Nigerian domestic systemically important banks (D-SIBs) ;First Bank, GTBank/GTCO, Zenith, Access, and UBA. On  this network I test a fiscal transmission channel that is my own construction, one that links Brent crude oil prices, monthly Federation Account Allocation Committee (FAAC) disbursements, and CBN external reserves to banking-system connectedness. I must however account for the government's own hand in these stress signals, and I do this with five(5) binary institutional dummies: the year 2009 to year 2011 interbank guarantee, AMCON operations, the multi-window FX regime, COVID-19 forbearance, and the June year 2023 FX unification. Without these controls, what looks like market stress in my data could just as easily be the residue of policy — these five(5) dummies exist to keep that distinction clear.
Repository structure
```
├── nigerian_banking_contagion.ipynb Main research notebook: corporate-action verification,
│                                     univariate GARCH(1,1)-t / GJR-GARCH(1,1)-t comparison,
│                                     DCC(1,1) estimation, Delta CoVaR network and regime
│                                     centrality, the FAAC/Brent/reserves transmission VAR
│                                     and Granger causality tests, the oil-exposure panel,
│                                     and two(2) of my five(5) robustness checks. Executed
│                                     with outputs saved — opens showing real tables and
│                                     charts, no re-run required.
├── data/
│   └── raw/
│       ├── ngx_prices.csv                          Daily prices, five banks, 2012–2024
│       │                                            (source: Investing.com)
│       ├── HISTORICAL_EQUITY_DATA__2005--2012.xlsx  Daily prices, five banks, 2008–2012
│       │                                            (source: NGX academic data request)
│       ├── brent_monthly.csv                        Real Brent crude, monthly, 2008–2024
│       │                                            (source: FRED/IMF POILBREUSDM)
│       ├── reserves.csv                             Real CBN external reserves, monthly,
│       │                                            2008–2024 (source: CBN daily Gross
│       │                                            reserves export; 5 months interpolated,
│       │                                            see Known data limitations below)
│       └── faac_annual.csv                          Real FAAC totals, annual, 2008–2023
│                                                     (source: CBN Statistical Bulletin
│                                                     Table B.3.3); year 2024 is my own
│                                                     estimate from five(5) real monthly
│                                                     disbursement reports
├── outputs/
│   ├── corporate_action_verification_log.csv   Real
│   ├── univariate_garch_gjr_comparison.csv     Real
│   ├── dcc_parameters.csv                      Real
│   ├── dcc_mean_pairwise_correlation.csv       Real
│   ├── table1_delta_covar_matrix.csv           Real (Brent, reserves, FAAC controls real;
│   │                                            see Model scope boundary statement)
│   ├── table2_centrality_by_regime.csv         Real, same basis as above
│   └── figures/                                Charts embedded in my Draft Project report
└── requirements.txt                 Python dependencies
```
How to run
Clone or download this repository.
Install dependencies: `pip install -r requirements.txt` (Python 3.10+).
Open `nigerian_banking_contagion.ipynb` in Jupyter, VS Code, or Google Colab and run all cells top to bottom. The notebook reads from `data/raw/` using relative paths.
Expected result: a merged sample of 4,208 daily trading days (4,193 complete rows across all five(5) banks) spanning 2008-01-03 to 2024-12-31, followed by the full network, transmission, and panel estimation described below.
Data sources
Series	Source	Status
Daily equity prices, five(5) D-SIBs (2012–2024)	Investing.com (NGX-listed equities)	Real
Daily equity prices, five(5) D-SIBs (2008–2012)	Nigerian Exchange (NGX) academic data request	Real
Brent crude oil prices, monthly	FRED/IMF (POILBREUSDM)	Real
CBN external reserves, monthly	CBN daily Gross reserves export	Real (5 months interpolated)
Monthly FAAC disbursements	CBN Statistical Bulletin Table B.3.3 + five(5) real 2024 monthly reports	Real annual (2024 estimated); evenly disaggregated to monthly
Parallel market FX premium	AbokiFX / CBN BDC rates	Placeholder — deferred to future work
Bank-level annual oil & gas loan exposure	Audited annual reports, NGX-listed D-SIBs	Placeholder — deferred to future work
Ticker continuity: GUARANTY→GTCO (2021 holdco restructuring), ACCESS→ACCESSCORP (2022 holdco; Diamond Bank merger 2019), and FIRSTBANK→FBNH→FIRSTHOLDCO are spliced into single continuous series per bank, with the return on each transition date excluded. The NGX (2008–2012) and Investing.com (2012–2024) segments are spliced at January 2013 with no return computed across the boundary; validated against 233 common trading days in the 2012 overlap window at per-bank correlations of 0.992–1.000.
Data-readiness flags — read before citing any number
I split my original two-flag structure into per-series flags this round, since my source series arrived on different timelines and a single `USE_SYNTHETIC_MACRO` flag was hiding partial progress:
```
USE_SYNTHETIC_EQUITY    = False   # Real: the five D-SIBs' daily returns, 2008–2024
USE_SYNTHETIC_BRENT     = False   # Real: FRED/IMF Brent crude, monthly, 2008–2024
USE_SYNTHETIC_RESERVES  = False   # Real: CBN daily reserves export, monthly-averaged
USE_SYNTHETIC_FAAC      = False   # Real annual 2008–2023 + estimated 2024, disaggregated
USE_SYNTHETIC_CPI       = True    # Placeholder: only feeds FAAC real-terms deflation
USE_SYNTHETIC_PREMIUM   = True    # Placeholder: deferred to future work
USE_SYNTHETIC_OIL_PANEL = True    # Placeholder: deferred to future work
```
My FAAC series carries one honest caveat I want stated plainly here rather than only in my report: because CBN's Statistical Bulletin publishes FAAC only at annual frequency, I distribute each year's real total evenly across its twelve(12) months. The real signal in this series is year-to-year; the within-year variation is a modelling convenience of mine, not observed data.
Preliminary results (real data, as of this commit)
Corporate-action scan: 24 flagged outlier returns (|move| > 12%) across the full 2008–2024 panel. 16 cluster in the March/April dividend season and are treated; 8 cluster in the 2008–2009 global financial crisis window and are retained as genuine crisis-period market moves.
GARCH(1,1)-t vs. GJR-GARCH(1,1)-t: BIC prefers the symmetric specification for all five(5) banks, including across the GFC episode.
DCC(1,1): α ≈ 0.038, β ≈ 0.904, α + β ≈ 0.942 — stationary, even though the univariate GARCH variances sit at the integrated boundary.
Delta CoVaR and regime centrality: now computed with real Brent, reserves, and FAAC as quantile-regression controls. Systemic centrality shifts materially across my four(4) regimes rather than staying fixed on one(1) or two(2) banks — UBA and FIRSTBANK dominate the earlier crisis regimes, GTB and ACCESS rise by the post-unification period.
Transmission VAR and Granger causality: my clearest finding this round. CBN reserve changes Granger-cause banking-sector connectedness decisively (p = 0.0006 at one lag, p = 0.0039 at two lags); FAAC and Brent do not. This shifts my study's emphasis from the fiscal channel I framed in Module 4 toward the monetary channel — read against Kaminsky and Reinhart's twin-crises framework, this is consistent with treating the currency/reserve channel as a leading indicator in its own right.
HMM regime-validation check: my original single-initialization, full-covariance specification failed to converge. I traced this to over-parameterization and fixed it with diagonal covariance and ten(10) random initializations, all of which now converge cleanly.
Oil-exposure panel: I found and fixed a genuine bug — the Wald test of slope equality previously returned a numerically degenerate statistic under entity-clustered standard errors, because I had exactly five(5) clusters matching five(5) free bank-specific parameters. I moved clustering to the time dimension, which resolves it. The panel itself still runs on synthetic oil-exposure data, so I do not report the Wald statistic as a finding yet.
Betweenness centrality: returns exactly zero for every bank. I confirmed this is not a bug — my Delta CoVaR construction produces a complete directed graph, and betweenness is mathematically zero for every node in a complete graph regardless of edge weights.
Model scope boundary statement
My committed scope, as agreed with my capstone supervisor, comprises: (1) the DCC-GARCH / Delta CoVaR network with eigenvector centrality rankings compared across regime periods; (2) the FAAC/Brent/reserves fiscal-monetary transmission channel tested by Granger causality within a vector autoregression; and (3) the five(5) institutional dummy controls. I dropped the parallel market premium from this core VAR specification this round — not because it is uninteresting, but because my supervisor felt my original scope was too large, and the premium, still synthetic at this stage, was one of the pieces we agreed to cut.
The following remain explicitly designated future work, not yet implemented on real data: the bank-level crude-oil loan exposure panel, the parallel-market FX premium early-warning variable, and my remaining three(3) robustness checks (Haver Analytics premium substitution, the formal Chow test writeup, and the maximum entropy bilateral network comparison). A stated limitation follows from the oil-exposure exclusion: without it, common-factor exposure and genuine bilateral contagion cannot yet be fully separated, and I interpret my results accordingly.
Known data limitations:
NGX equities exhibit thin trading (10–15% zero-return days) and daily price limits (±10%) that censor extreme single-day returns.
CBN reserves has no source ticks for five(5) months (February to June of year 2009); I interpolate linearly across this gap, which falls inside my GFC regime.
My FAAC series has no real within-year variation, for the reason stated above under Data-readiness flags; I cannot yet distinguish whether my null Granger-causality result for FAAC is genuine or an artifact of this disaggregation.
My Chow test for the June year 2023 unification currently has only twenty (20) post-break observations — low power, not yet a substantive finding either way.
One(1) corporate-action flag (UBA, 2015-09-10) remains unverified — it falls outside the dividend season with no explanatory calendar gap, and may instead reflect the JP Morgan GBI-EM index exclusion sell-off of that period rather than a corporate action; it is retained untreated pending confirmation either way.
Project status
[x] Data acquisition and validation, five(5) banks, 2012–2024
[x] NGX historical extension, 2008–2012 — received and merged
[x] Corporate-action scan and verification (24 flags, 16 treated, 8 retained)
[x] Univariate GARCH(1,1)-t estimation per bank
[x] GJR-GARCH(1,1)-t asymmetry check (symmetric preferred, all five banks)
[x] DCC(1,1) estimation (two-stage MLE, converged)
[x] Delta CoVaR network construction (real Brent/reserves/FAAC controls)
[x] Regime-period centrality comparison
[x] FAAC/Brent/reserves transmission VAR and Granger causality tests
[x] HMM regime-validation check (converged, diagonal covariance)
[x] Oil-exposure panel code and Wald test clustering fix (data still synthetic)
[x] Robustness Check A (centrality agreement) and Check C (forbearance exclusion)
[ ] Parallel market premium collection (future work)
[ ] Bank-level oil-exposure panel collection (future work)
[ ] Robustness Checks B, D, E
[ ] Final report and presentation
Contact samuel@teledinamik.com.ng
