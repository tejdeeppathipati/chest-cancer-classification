import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.data_ingestion import DataIngestion

if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run()
