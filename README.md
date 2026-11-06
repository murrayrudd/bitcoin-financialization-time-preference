# Same Bitcoin, Different Time Horizons: Financialization and the Erosion of Patience

Self-contained model, saved results, and replication materials for Murray A. Rudd's **Same Bitcoin, Different Time Horizons: Financialization and the Erosion of Patience**.

**Model version 0.5 · Replication package 0.5.1.**

The study asks whether financialization can raise effective time preference relative to engaged independent holding when the same holder has the same Bitcoin exposure and baseline psychological patience. Institutional arrangements differ in independent control, operational assistance, monitoring incentives, and the consequences of financial review. Those features change attention allocation, maintained understanding, and decision pressure.

## Main findings

- Financialization can weaken support for patient holding without changing Bitcoin's monetary properties. The reference normalized effective rate is **0.767 under consequential service versus 0.397 under engaged independent holding**.
- Both rates remain below the common baseline of 1. Financialization produces a smaller modeled reduction in discounting relative to that baseline; the baseline is not an observed pre-adoption rate.
- Independent control does not eliminate consequential review pressure. Retaining control with consequential review gives a reference rate of **0.591**.
- Operational assistance and pressure relief provide different benefits. Sufficient pressure relief can reverse some comparisons, while complementarity can support engagement when attention remains available.

These are conditional theoretical results. The temporal links are explicit hypotheses, and scenario counts do not represent population frequencies.

## Get the complete materials

All replication files are included directly in the repository. Use GitHub's **Code → Download ZIP** and extract the folder, or clone [this repository](https://github.com/murrayrudd/bitcoin-financialization-time-preference). No earlier repository, private archive, external dataset, or model-provider account is required.

## Reproduce

Use **Python 3.12.14** and the pinned dependencies:

~~~bash
python -m venv .venv
# Activate .venv using the command for your operating system.
python -m pip install -r requirements.txt
python scripts/verify_package.py
python scripts/reproduce.py --full --figures
~~~

On Windows, py -3.12 can replace python. Installation requires internet access; research computations use local files only.

The full command uses a temporary copy, reruns the experiments and 19 numerical checks, compares every regenerated CSV result table with its saved counterpart, and rebuilds the publication figures. It preserves the distributed results. Omit --full --figures for a faster numerical check. See [replication instructions](docs/REPRODUCING.md).

## Find the evidence

| Material | Location |
| --- | --- |
| Allocation solver, states, discounting, analytical boundaries | [Model source](model/src/model.py) |
| Experiment definitions and settings | [Experiment runner](model/run_experiments.py) · [Configuration](model/results/configuration.json) |
| Complete saved results and output definitions | [Results](model/results/) · [Output map](model/results/README.md) |
| Specification, propositions, assumptions | [Specification](model/docs/model_specification.md) · [Propositions](model/docs/propositions.md) · [Assumptions](model/docs/assumptions.json) |
| Literature roles and interpretation boundaries | [Evidence ledger](model/docs/evidence_ledger.csv) · [Source provenance](model/docs/source_provenance.json) |
| Figure source and exact plotting data | [Publication materials](publication/) |
| Manuscript figures | [PNG](publication/png/) · [SVG](publication/svg/) · [PDF](publication/pdf/) |
| Manuscript-to-output map | [Manuscript map](docs/MANUSCRIPT_MAP.md) |
| Numerical checks and package verification | [Model checks](model/tests/verify.py) · [Verification record](docs/VERIFICATION.json) |
| Version history and distribution choices | [Provenance](docs/PROVENANCE.md) |

## Research basis

**Rudd, M. A. (2026).** *Same Bitcoin, Different Time Horizons: Financialization and the Erosion of Patience*. Working paper, 2026.

An SSRN link can be added when available. The manuscript and third-party papers are not included.

## Citation

Please cite the accompanying paper and identify **model version 0.5**, **replication package 0.5.1**, and the repository commit used:

~~~bibtex
@unpublished{Rudd2026BitcoinFinancialization,
  author = {Rudd, Murray A.},
  title = {Same Bitcoin, Different Time Horizons: Financialization and the Erosion of Patience},
  year = {2026},
  note = {Working paper; model version 0.5}
}
~~~

[CITATION.cff](CITATION.cff) supplies machine-readable software metadata and the preferred paper citation through GitHub's **Cite this repository** option. This package has no assigned DOI.

## License

Original project code and associated software documentation are available under the [MIT License](LICENSE.md). See [license scope](LICENSE_SCOPE.md) for the distinction between software and scholarly material. Third-party works retain their source terms.

## Author

**Murray A. Rudd, Ph.D.**  
Futures Insight Research

- ORCID: [0000-0001-9533-5070](https://orcid.org/0000-0001-9533-5070)
- SSRN: [Author profile](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=5958022)
- Google Scholar: [Profile](https://scholar.google.co.uk/citations?hl=en&user=84qbofEAAAAJ)
