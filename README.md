---

# **Coffea-Casa Framework for CMS NanoAOD Analysis**

This repository contains a modular and extensible framework for performing CMS NanoAOD analyses using the **columnar analysis paradigm** enabled by the *SciKit-HEP ecosystem* (coffea, uproot, awkward, correctionlib, dask).
It is designed to run both **locally** and in a **distributed Coffea-Casa environment**, providing a clean separation between:

* **Object corrections**
* **Object selections**
* **Event corrections**
* **Event selections**
* **Histogramming**
* **Fileset building (local, DAS, and Rucio)**
* **Processor execution**

The goal is to offer a **reusable, maintainable, and well-structured workflow** for CMS analyses, following best practices recommended by the POGs and the CMS Analysis Software Group.

---

## **Repository Structure**

```
coffea-casa_framework/
│
├── constructors/              # Core building blocks of the analysis
│   ├── corrections/           # Object- and event-level corrections
│   │   ├── correct_polar_met.py
│   │   ├── crystall_ball.py
│   │   ├── event_corrector.py
│   │   ├── sets/              # External correction files (JSON/TXT)
│   │   │   ├── RoccoR2018UL.txt
│   │   │   ├── muon_Z.json.gz
│   │   │   └── run3_met_xy_corrections.json
│   ├── filesets/              # Fileset construction tools
│   │   ├── build_fileset.py
│   │   ├── filesets.py
│   │   └── rucio_queries.py   # Automatic Rucio listing utilities
│   ├── histograms/            # Histogram fillers and definitions
│   │   └── histogram_filler.py
│   ├── processors/            # Coffea processors
│   │   └── muon_processor.py
│   ├── selections/            # Object & event selection modules
│   │   ├── event_selector.py
│   │   └── object_selector.py
│   └── utils/                 # Utility functions
│       └── util_functions.py
│
├── loadmodule/                # Dynamic module loader (PEP 660 compatible)
│   └── pyproject.toml
│
├── runner.ipynb               # Full runnable example of the workflow
├── tester.ipynb               # Quick test of modules and processors
├── corrections-explorer_example.ipynb
├── rucio_builder_test.ipynb
└── README.md
```

---

## **Features**

### ✔ Object Corrections

* Rochester corrections for muons
* Z-peak tuning JSONs (POG-recommended)
* MET φ-modulation corrections
* Crystal-ball smearing utilities
* Automatic correction loading

---

### ✔ Object Selection

* Kinematic cuts (pt, eta, phi, charge…)
* ID and isolation selections
* Impact-parameter and quality filters
* Pair building (dimuons, dielectrons…)

---

### ✔ Event Corrections

* Pileup reweighting
* Trigger scale factors
* Event-level selections with PackedSelection
* Luminosity and normalization handling

---

### ✔ Event Selection

* HLT/L1 selection
* Vetoes and cleaning filters
* Signal-region and control-region definitions

---

### ✔ Histogramming

* Modular, processor-friendly histograms
* Centralized histogram filler
* coffea-compatible accumulator

---

### ✔ Fileset Builder

* Local JSON-based filesets
* DAS query builder
* **Rucio-based dataset discovery**
* Automatic JSON generation for processors

---

### ✔ Processors

* Example **MuonProcessor** included
* Easy extension for new analyses
* Uses the columnar paradigm (awkward)
* Ready for Coffea-Casa scaling (Dask)

---

## **Quick Start**

### 1. Clone the repository

```bash
git clone https://github.com/diego-riosp/coffea-casa_framework.git
cd coffea-casa_framework
```

### 2. (Optional) Install dynamic module loader

```bash
pip install -e loadmodule/
```

### 3. Run the full workflow

Open:

```
runner.ipynb
```

This notebook shows the complete chain:

1. Build or load a fileset
2. Apply object corrections
3. Apply event corrections
4. Select objects
5. Select events
6. Fill histograms
7. Return a coffea accumulator

---

## **Using the Processor**

Example (Python):

```python
from constructors.processors.muon_processor import MuonProcessor
from coffea import runner, nanoevents

processor_instance = MuonProcessor(year="2018UL")

output = runner.Runner().run(fileset, processor_instance)
```

---

## **Rucio Integration**

Use:

```python
from constructors.filesets.rucio_queries import query_rucio_dataset

query_rucio_dataset("/*/Run2018D-NanoAODv9*/NANOAOD")
```

to automatically retrieve NanoAOD datasets and generate a JSON fileset.

---

## **Jupyter Utilities**

* `tester.ipynb` – quick-smoke tests
* `corrections-explorer_example.ipynb` – visualize correction maps
* `rucio_builder_test.ipynb` – building filesets via Rucio

---

## **Future Plans**

* Add HLT-trigger extractor module
* Add automatic luminosity JSON loader
* Include more processors (Electron, Jet, MET, τ…)
* Add full CI pipeline
* And many many others

---

## **Author**

**Diego Ríos**
(CMS Collaboration – B Physics / HEP Analysis)

---
