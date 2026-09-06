import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

import logging
from datetime import datetime

LOG_PATH = PROJECT_ROOT / "logs"
LOG_PATH.mkdir(exist_ok=True)

log_filename = LOG_PATH / f"pipeline_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Starting TransactionPulse pipeline...")

def run_script(script_name: str):
    script_path = SRC_PATH / script_name
    logging.info(f"Running: {script_name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True
    )

    logging.info(result.stdout)

    if result.returncode != 0:
        logging.error(f"ERROR in {script_name}:")
        logging.error(result.stderr)
        sys.exit(1)
    else:
        logging.info(f"{script_name} completed successfully.")


run_script("inject_dirty_data.py")
run_script("data_quality_checks.py")
run_script("clean_data.py")
run_script("transform_data.py")

print("🎉 Pipeline completed successfully! All outputs are in data/clean and data/transformed.")