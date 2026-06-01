# Excel Data Pipeline

## Overview
This project processes large volumes of Excel files with inconsistent and non-tabular structures into a clean, structured dataset.

It was originally developed in a workforce management (WFM) context, where forecasting data was distributed across multiple semi-structured Excel files.

---

## Problem

- Data stored across many Excel files
- Inconsistent layout (not standard tables)
- Variable block structures
- Difficult to process with standard tools

---

## Approach

- Block-based parsing of Excel sheets
- Generator pattern (`yield`) to process data efficiently
- Graceful error handling (skip invalid blocks instead of failing entire run)
- Conversion to a structured dataset for further analysis

---

## Features

- Memory-efficient processing of large datasets
- Robust handling of inconsistent structures
- Modular design for easy extension
- Clear separation between pipeline logic and execution

---

## Tech Stack

- Python
- Pandas
- Pathlib

---

## How to Run

```bash
python run/main.py
