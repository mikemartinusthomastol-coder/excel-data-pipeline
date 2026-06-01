from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# Exceptions
# =========================

class BlockDimensionError(Exception):
    """Raised when a block has incorrect dimensions."""
    pass


# =========================
# Helpers
# =========================

DAY_OFFSETS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6,
}

def extract_date_from_filename(filename: str) -> datetime | None:
    match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
    if match:
        return datetime.strptime(match.group(), "%Y-%m-%d")
    return None


def get_day_index(day):
    if pd.isna(day):
        return 0
    return DAY_OFFSETS.get(str(day), 0)


# =========================
# Core logic
# =========================

def process_block(df_raw, i, block_rows, block_cols, reference_date):
    rows_per_block = block_rows[1] - block_rows[0]
    start_row = block_rows[0] + i * rows_per_block
    end_row = start_row + rows_per_block

    block = df_raw.iloc[start_row:end_row, block_cols[0]:block_cols[1]]

    if block.shape[0] != 7:
        raise BlockDimensionError(f"Invalid block size: {block.shape}")

    result = pd.DataFrame({
        "date": [],
        "group": [],
        "offered": [],
        "load_date": []
    })

    monday_base = reference_date - timedelta(days=reference_date.weekday())

    days = block.iloc[:, 0].tolist()
    result["date"] = [
        monday_base + timedelta(days=get_day_index(d)) for d in days
    ]

    result["group"] = block.iloc[:, 1].values

    # numeric aggregation
    data_slice = block.iloc[:, 5:57].apply(pd.to_numeric, errors="coerce")
    result["offered"] = (data_slice.sum(axis=1) / 4).round(0)

    result["load_date"] = datetime.now()

    return result


def process_excel_file(filepath: Path):
    filename = filepath.name
    reference_date = extract_date_from_filename(filename)

    if not reference_date:
        logger.warning(f"Skipping file without valid date: {filename}")
        return

    df_raw = pd.read_excel(filepath, sheet_name="forecast", header=None)

    block_rows = (1, 8)
    block_cols = (0, 57)

    groups = df_raw.iloc[:, 1].drop_duplicates().values.tolist()

    for i in range(len(groups)):
        try:
            yield process_block(df_raw, i, block_rows, block_cols, reference_date)
        except BlockDimensionError as e:
            logger.warning(f"Skipping block {i+1} in {filename}: {e}")
            continue


def process_directory(input_dir: Path) -> pd.DataFrame:
    all_blocks = []

    files = list(input_dir.glob("**/*.xlsx"))
    logger.info(f"Found {len(files)} Excel files")

    for file in files:
        logger.info(f"Processing {file.name}")

        for block in process_excel_file(file):
            all_blocks.append(block)

    if not all_blocks:
        return pd.DataFrame()

    return pd.concat(all_blocks, ignore_index=True)