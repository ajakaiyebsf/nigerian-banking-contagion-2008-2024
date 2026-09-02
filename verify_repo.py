#!/usr/bin/env python3
"""
verify_repo.py — internal-consistency check for the Nigerian banking contagion repository.

Run from the repository root, after committing:

    python3 verify_repo.py            # full check, executes the notebook (~30s)
    python3 verify_repo.py --quick    # skips the notebook run (~2s)

Green means the repository is internally consistent and reproduces its own
outputs. Red names the file that disagrees. Amber is advisory.

Exit code 0 if nothing FAILED, 1 otherwise.
"""

import sys, os, re, json, io, contextlib, warnings, argparse
warnings.filterwarnings("ignore")

QUICK = "--quick" in sys.argv
PLAIN = "--no-color" in sys.argv or not sys.stdout.isatty()
G, R, Y, B, X = ("", "", "", "", "") if PLAIN else (
    "\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[0m")

results = []


def check(name):
    """Decorator: registers a check. The function returns (ok, detail) or
    (None, detail) for an advisory warning."""
    def wrap(fn):
        results.append((name, fn))
        return fn
    return wrap


# --------------------------------------------------------------------------
# 1. Files present
# --------------------------------------------------------------------------
REQUIRED = [
    "README.md", "requirements.txt", "nigerian_banking_contagion.ipynb",
    "data/raw/faac_annual.csv", "data/raw/brent_monthly.csv",
    "data/raw/reserves.csv", "data/raw/ngx_prices.csv",
    "data/raw/HISTORICAL_EQUITY_DATA__2005--2012.xlsx",
    "outputs/figures/fig1_dcc_correlation.png",
    "outputs/figures/fig2_connectedness.png",
    "outputs/figures/fig3_irf_reserves.png",
    "outputs/table1_delta_covar_matrix.csv",
    "outputs/table2_centrality_by_regime.csv",
]


@check("All required files present")
def _files():
    missing = [p for p in REQUIRED if not os.path.exists(p)]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, f"{len(REQUIRED)} files"


@check("No stale figures from earlier versions")
def _stale_figs():
    if not os.path.isdir("outputs/figures"):
        return False, "outputs/figures missing"
    stale = [f for f in os.listdir("outputs/figures")
             if f in ("fig1_conditional_volatility.png", "fig2_dcc_correlation.png",
                      "fig3_dcc_by_regime.png", "fig4_bic_garch_gjr.png")]
    if stale:
        return None, "M4-era figures still present: " + ", ".join(stale)
    return True, "clean"


# --------------------------------------------------------------------------
# 2. FAAC correction landed
# --------------------------------------------------------------------------
@check("FAAC 2024 is the corrected distributed figure")
def _faac():
    import pandas as pd
    f = pd.read_csv("data/raw/faac_annual.csv")
    row = f[f.year == 2024]
    if row.empty:
        return False, "no 2024 row"
    v = float(row.faac_nbn.iloc[0])
    est = bool(row.is_estimated.iloc[0])
    if abs(v - 15260.0) > 1.0:
        return False, f"2024 = {v:,.2f}, expected 15,260 (gross-basis value was 31,236)"
    if est:
        return False, "2024 value correct but is_estimated is still True"
    prev = float(f[f.year == 2023].faac_nbn.iloc[0])
    return True, f"15,260 real, +{100*(v/prev-1):.1f}% YoY"


# --------------------------------------------------------------------------
# 3. README agrees with the data
# --------------------------------------------------------------------------
@check("README does not contradict the data files")
def _readme_data():
    t = open("README.md", encoding="utf-8").read()
    bad = []
    if ("31,236" in t or "31236" in t):
        # mentioning the old figure is fine IF it is framed as a correction
        ctx = re.search(r"[^.]*31[,]?236[^.]*\.", t)
        framed = bool(ctx) and re.search(
            r"earlier version|replaced|was taken|incorrect|corrected|previously",
            ctx.group(0), re.I)
        if not framed:
            bad.append("cites 31,236 as a current value, not as a corrected error")
    if "15,260" not in t and "15260" not in t:
        bad.append("does not mention the corrected 15,260 figure")
    if "NEITI" not in t:
        bad.append("does not cite NEITI as the 2024 FAAC source")
    return (False, "; ".join(bad)) if bad else (True, "FAAC figures and source agree")


@check("README voice and number style")
def _readme_style():
    t = open("README.md", encoding="utf-8").read()
    body = re.sub(r"```.*?```", "", t, flags=re.S)          # ignore code blocks
    words = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
             "thirteen|fourteen|fifteen|sixteen|twenty|twenty-four|thirty|fifty|hundred")
    numerals = sorted(set(re.findall(rf"\b(?:{words})\s*\(\d+\)", body, re.I)))
    firstp = re.findall(r"\b(?:I|my|My|me)\b", body)
    msg = []
    if numerals:
        msg.append(f"numeral convention: {', '.join(numerals[:5])}")
    if firstp:
        msg.append(f"{len(firstp)} first-person instances")
    return (None, "; ".join(msg)) if msg else (True, "third person, no word(digit)")


# --------------------------------------------------------------------------
# 4. requirements.txt
# --------------------------------------------------------------------------
@check("requirements.txt covers every import and is pinned")
def _reqs():
    nb = json.load(open("nigerian_banking_contagion.ipynb"))
    src = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    mods = {m.split(".")[0] for m in
            re.findall(r"^\s*(?:from|import)\s+([a-zA-Z_][\w.]*)", src, re.M)}
    std = {"os", "pickle", "warnings", "sys", "json", "math", "itertools",
           "collections", "time", "datetime", "re"}
    lines = [l.strip() for l in open("requirements.txt") if l.strip()
             and not l.strip().startswith("#")]
    named = {re.split(r"[=<>!~]", l)[0].strip().lower() for l in lines}
    missing = sorted(m for m in mods if m.lower() not in named and m not in std)
    unpinned = [l for l in lines if "==" not in l]
    if missing:
        return False, "not declared: " + ", ".join(missing)
    if unpinned:
        return None, f"{len(unpinned)} unpinned: " + ", ".join(unpinned[:4])
    return True, f"{len(lines)} packages, all pinned"


# --------------------------------------------------------------------------
# 5. Notebook structure
# --------------------------------------------------------------------------
@check("Notebook imports sit in the first code cell")
def _imports_first():
    nb = json.load(open("nigerian_banking_contagion.ipynb"))
    code = [("".join(c["source"])) for c in nb["cells"] if c["cell_type"] == "code"]
    if not code:
        return False, "no code cells"
    if "import " not in code[0]:
        return False, "first code cell has no imports — a partial run will fail"
    return True, "run-all works from cold"


def _code_only(src):
    """Strip comment lines, so checks do not trip on prose describing old code."""
    return "\n".join(l for l in src.split("\n") if not l.strip().startswith("#"))


@check("Impulse responses use a true one-standard-deviation shock")
def _orth():
    nb = json.load(open("nigerian_banking_contagion.ipynb"))
    src = _code_only("\n".join("".join(c["source"]) for c in nb["cells"]
                               if c["cell_type"] == "code"))
    if "orth=False" in src:
        return False, "IRF uses orth=False (a unit shock) while captions claim one SD"
    return True, "orthogonalised"


@check("Output cell writes the figures the report uses")
def _outcell():
    nb = json.load(open("nigerian_banking_contagion.ipynb"))
    src = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    want = ["fig1_dcc_correlation.png", "fig2_connectedness.png", "fig3_irf_reserves.png"]
    missing = [w for w in want if w not in src]
    if missing:
        return False, "notebook never writes: " + ", ".join(missing)
    return True, "all report figures generated by the notebook"


# --------------------------------------------------------------------------
# 6. Cold run + reproducibility
# --------------------------------------------------------------------------
_STATE = {}


def _run_notebook():
    """Execute the notebook in a scratch copy of the repository, so that its
    output cells run for real without overwriting the committed outputs/."""
    if "g" in _STATE:
        return _STATE["g"], _STATE["fails"], _STATE["dir"]
    import matplotlib, tempfile, shutil
    matplotlib.use("Agg")
    src_dir = os.getcwd()
    tmp = tempfile.mkdtemp(prefix="verify_repo_")
    shutil.copy("nigerian_banking_contagion.ipynb", tmp)
    shutil.copytree("data", os.path.join(tmp, "data"))
    nb = json.load(open("nigerian_banking_contagion.ipynb"))
    g, fails = {"__name__": "__main__"}, []
    os.chdir(tmp)
    try:
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] != "code":
                continue
            s = "\n".join(l for l in "".join(c["source"]).split("\n")
                          if not l.strip().startswith("!"))
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(s, f"cell{i}", "exec"), g)
            except Exception as e:
                fails.append(f"cell {i}: {type(e).__name__}: {str(e)[:70]}")
    finally:
        os.chdir(src_dir)
    _STATE["g"], _STATE["fails"], _STATE["dir"] = g, fails, tmp
    return g, fails, tmp


@check("Notebook runs cold, top to bottom")
def _coldrun():
    if QUICK:
        return None, "skipped (--quick)"
    g, fails, _ = _run_notebook()
    if fails:
        return False, f"{len(fails)} cell failure(s): " + fails[0]
    n = len(g.get("clean_returns_df", []))
    return True, f"0 failures, {n:,} trading days"


@check("Committed outputs match a fresh run")
def _repro():
    if QUICK:
        return None, "skipped (--quick)"
    import pandas as pd
    g, fails, _ = _run_notebook()
    if fails:
        return False, "notebook did not complete"
    checks = [("outputs/table2_centrality_by_regime.csv", "centrality_table", 0.005),
              ("outputs/table1_delta_covar_matrix.csv", "delta_covar_matrix", 0.0005)]
    bad = []
    for path, var, tol in checks:
        if not os.path.exists(path) or var not in g:
            bad.append(f"{os.path.basename(path)}: absent")
            continue
        committed = pd.read_csv(path, index_col=0)
        fresh = g[var]
        try:
            d = (fresh - committed.reindex(index=fresh.index,
                                           columns=fresh.columns)).abs().max().max()
        except Exception as e:
            bad.append(f"{os.path.basename(path)}: not comparable ({e})")
            continue
        if pd.isna(d) or d > tol:
            bad.append(f"{os.path.basename(path)}: max diff {d:.4f} > {tol}")
    if bad:
        return False, "; ".join(bad) + "  → re-run the notebook and commit outputs/"
    return True, "tables reproduce"


@check("Headline numbers unchanged")
def _headline():
    if QUICK:
        return None, "skipped (--quick)"
    g, fails, _ = _run_notebook()
    if fails:
        return False, "notebook did not complete"
    try:
        from statsmodels.tsa.stattools import grangercausalitytests
        vd, bl = g["var_data"], g["best_lags"]
        with contextlib.redirect_stdout(io.StringIO()):
            r = grangercausalitytests(vd[["connectedness", "reserves_diff"]], maxlag=bl)
        p1 = r[1][0]["ssr_ftest"][1]
        ab = g["a_hat"] + g["b_hat"]
    except Exception as e:
        return False, f"could not evaluate: {e}"
    msgs = []
    if not (p1 < 0.01):
        msgs.append(f"reserves Granger p(lag1) = {p1:.4f}, expected < 0.01")
    if not (0.93 < ab < 0.95):
        msgs.append(f"DCC alpha+beta = {ab:.4f}, expected ~0.942")
    if msgs:
        return False, "; ".join(msgs)
    return True, f"reserves p={p1:.4f}, DCC a+b={ab:.3f}"


# --------------------------------------------------------------------------
def main():
    print(f"\n{B}Repository consistency check{X}")
    print(f"{'quick mode — notebook not executed' if QUICK else 'full check'}\n")
    n_fail = n_warn = 0
    for name, fn in results:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"check errored: {type(e).__name__}: {e}"
        if ok is True:
            print(f"  {G}PASS{X}  {name}\n        {detail}")
        elif ok is None:
            n_warn += 1
            print(f"  {Y}WARN{X}  {name}\n        {detail}")
        else:
            n_fail += 1
            print(f"  {R}FAIL{X}  {name}\n        {detail}")
    total = len(results)
    print(f"\n  {total - n_fail - n_warn} passed, {n_warn} warning(s), {n_fail} failure(s)")
    if n_fail:
        print(f"  {R}Repository is not internally consistent — see FAIL lines above.{X}\n")
    else:
        print(f"  {G}Repository is internally consistent.{X}\n")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
