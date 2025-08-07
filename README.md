# node-status-pipeline
A complete data pipeline and automation system that simulates real-time network data via a FastAPI backend, cleans and preprocesses it, and trains a predictive model to estimate node health status.

**Features:**
1.FastAPI Backend: Simulates realistic node, latency, and status data with configurable randomness and real-time behavior.
2.Data Cleaning: Handles nulls, inconsistent labels, missing IDs, and transforms raw data into usable format.
3.Status Prediction Model: Trained ML model (Logistic Regression) predicts node status (Up / Down / Degraded) based on latency and historical behavior.
4.Automation Pipeline: Sequential Makefile execution to run API → cleaning → modeling in one click.

Modular & Extensible: Clean structure split across multiple Python scripts for flexibility and reuse.
Fully Documented: Easy to understand, deploy, and extend.
