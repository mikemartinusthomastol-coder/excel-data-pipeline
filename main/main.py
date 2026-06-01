from pathlib import Path
from pipeline.excel_pipeline import process_directory

def main():
    input_dir = Path("data/input")
    
    df = process_directory(input_dir)

    if not df.empty:
        output_path = Path("data/output/result.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)
        print(f"Saved output to {output_path}")
    else:
        print("No data processed.")


if __name__ == "__main__":
    main()
