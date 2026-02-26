import argparse
import yaml
import pandas as pd
import numpy as np
import json
import logging
import time
import sys
import os


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def write_metrics(output_path, metrics):
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=4)


def main(args):
    start_time = time.time()

    try:
        logging.info("Job started")

        # ---- Load Config ----
        if not os.path.exists(args.config):
            raise FileNotFoundError("Config file not found")

        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        required_keys = ["seed", "window", "version"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # ---- Load Dataset ----
        if not os.path.exists(args.input):
            raise FileNotFoundError("Input CSV not found")

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Input CSV is empty")

        if "close" not in df.columns:
            raise ValueError("Missing required column: close")

        logging.info(f"Rows loaded: {len(df)}")

        # ---- Rolling Mean ----
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # ---- Signal ----
        df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)
        df = df.dropna()

        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        write_metrics(args.output, metrics)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=4))
        sys.exit(0)

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)

        error_metrics = {
            "version": config["version"] if 'config' in locals() and "version" in config else "unknown",
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, error_metrics)

        logging.error(f"Error occurred: {str(e)}")
        print(json.dumps(error_metrics, indent=4))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logging(args.log_file)
    main(args)