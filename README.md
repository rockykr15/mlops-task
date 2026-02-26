# ML/MLOps Engineering Internship -- Task 0

## Overview

This project implements a minimal MLOps-style batch pipeline in Python.
The pipeline is deterministic, observable, and fully Dockerized for
reproducible execution.

It performs:

-   YAML-based configuration loading
-   OHLCV dataset validation
-   Rolling mean computation on `close`
-   Binary signal generation
-   Structured metrics output (JSON)
-   Detailed logging
-   One-command Docker execution



## Objective

This solution demonstrates:

-   Reproducibility (Config-driven + seeded execution)
-   Observability (Structured metrics + logs)
-   Deployment readiness (Docker container)



## Project Structure

mlops-task/ │ ├── run.py ├── config.yaml ├── data.csv ├──
requirements.txt ├── Dockerfile ├── metrics.json ├── run.log └──
README.md



## Configuration (config.yaml)

seed: 42\
window: 5\
version: "v1"

-   seed → Ensures deterministic output\
-   window → Rolling mean window size\
-   version → Pipeline version tracking


## Processing Logic

1.  Load and validate YAML configuration

2.  Validate dataset (existence, non-empty, `close` column present)

3.  Compute rolling mean on `close`

4.  Generate signal:

    signal = 1 if close \> rolling_mean else 0

5.  Compute metrics:

    -   rows_processed
    -   signal_rate
    -   latency_ms


## Local Execution

python run.py --input data.csv --config config.yaml --output
metrics.json --log-file run.log



## Docker Execution

Build image:

docker build -t mlops-task .

Run container:

docker run --rm mlops-task



## Sample Output (metrics.json)

{ "version": "v1", "rows_processed": 9996, "metric": "signal_rate",
"value": 0.4991, "latency_ms": 35, "seed": 42, "status": "success" }



## Logging

run.log includes:

-   Job start timestamp
-   Config validation details
-   Dataset validation results
-   Rolling mean computation
-   Signal generation
-   Metrics summary
-   Job completion status
-   Exception handling (if any)



## Error Handling

The pipeline handles:

-   Missing input file
-   Invalid CSV format
-   Empty dataset
-   Missing required column (`close`)
-   Invalid configuration structure

In all cases, a metrics.json file is written.



## Reproducibility

The pipeline uses:

np.random.seed(seed)

Ensuring deterministic results across runs when the same configuration
is used.


## Deployment Readiness

-   Fully Dockerized
-   No hardcoded paths
-   Machine-readable output
-   Proper exit codes (0 on success, non-zero on failure)


