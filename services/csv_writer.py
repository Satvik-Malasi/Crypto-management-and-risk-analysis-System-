import csv
from pathlib import Path
from modal.stock_data import stock_data

class csv_writer:
    """
    Service to write StockUpdate data to a CSV file.
    """
    def __init__(self, filename: str = "stock_data.csv"):
        self.file_path = Path(filename)
        # Create file with header if it doesn't exist
        if not self.file_path.exists():
            with open(self.file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Symbol", "Price", "Time", "Volume"])

    def write(self, update: stock_data):
        """
        Append a stock update to the CSV.
        """
        with open(self.file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([update.symbol, update.price, update.time, update.volume])
        print(f"Wrote to CSV: {update}")
