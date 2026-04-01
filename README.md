# Indian Food Explorer

Interactive [Panel](https://panel.holoviz.org/) dashboard for exploring the [Indian Food dataset](https://www.kaggle.com/datasets/nehaprabhavalkar/indian-food-101) (regional dishes, ingredients, prep/cook times, and diet/flavor metadata).

## Features

- **Ingredients in Common** — Venn diagram of shared ingredients across up to three dishes
- **Scatter Analysis** — Relationships between prep time, cook time, region, course, and flavor profile
- **Category Heatmap** — Cross-tab of two categorical columns
- **Sankeys** — Flows between selected categorical fields (with optional minimum count)

## Setup

**Conda (recommended)** — environment name matches `requirements.yml`:

```bash
conda env create -f requirements.yml
conda activate ds3500
```

**pip:**

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the dashboard

From this directory:

```bash
panel serve foodexplore.py --autoreload --show
```

Then open the URL printed in the terminal (typically `http://localhost:5006`).

## Stack

| Library | Role |
|--------|------|
| Panel | Layout and widgets |
| Plotly | Scatter, heatmap, Sankey |
| matplotlib + matplotlib-venn | Venn diagrams |
| pandas | Data loading and cleaning |

## Layout

| File | Purpose |
|------|---------|
| `foodexplore.py` | Dashboard entrypoint (servable app) |
| `foodapi.py` | Loads CSV and exposes filters / flows |
| `cleaner.py` | Normalizes names and ingredients |
| `plots.py` | Plot helpers |
| `indian_food.csv` | Dataset |
