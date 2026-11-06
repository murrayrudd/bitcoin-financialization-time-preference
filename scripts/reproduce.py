"""Reproduce in a temporary copy; preserve distributed outputs."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def run(script):
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--figures", action="store_true")
    args = parser.parse_args()
    report = {"full_regeneration": args.full, "result_tables_compared": 0}
    with tempfile.TemporaryDirectory(prefix="bitcoin-financialization-") as temporary:
        work = Path(temporary)
        shutil.copytree(ROOT / "model", work / "model")
        if args.full:
            run(work / "model/run_experiments.py")
            for original in sorted((ROOT / "model/results").glob("*.csv")):
                a = pd.read_csv(original)
                b = pd.read_csv(work / "model/results" / original.name)
                assert list(a.columns) == list(b.columns) and a.shape == b.shape, original.name
                for column in a:
                    if pd.api.types.is_numeric_dtype(a[column]):
                        np.testing.assert_allclose(a[column], b[column], rtol=1e-9, atol=1e-11,
                                                   equal_nan=True, err_msg=f"{original.name}:{column}")
                    else:
                        assert a[column].fillna("").equals(b[column].fillna("")), (original.name, column)
                report["result_tables_compared"] += 1
        run(work / "model/tests/verify.py")
        checks = json.loads((work / "model/results/verification.json").read_text())
        assert checks["all_passed"]
        report["model_verification"] = checks
        if args.figures:
            shutil.copytree(ROOT / "publication", work / "publication")
            for p in (work / "publication/data").glob("*.csv"):
                shutil.copy2(work / "model/results" / p.name, p)
            for fmt in ("png", "svg", "pdf"):
                shutil.rmtree(work / "publication" / fmt)
            run(work / "publication/make_figures.py")
            report["figure_exports_rebuilt"] = sum(
                len(list((work / "publication" / fmt).glob("*." + fmt)))
                for fmt in ("png", "svg", "pdf"))
            assert report["figure_exports_rebuilt"] == 12
        report["all_passed"] = True
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
