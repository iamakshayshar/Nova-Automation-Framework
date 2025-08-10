#!/bin/bash

# Fail on first error
set -e

ENVIRONMENT=${1:-qa}
BROWSER=${2:-chrome}
HEADLESS_FLAG=${3:-"--headless"}

# Output directories
REPORT_DIR="reports"
SCREENSHOT_DIR="$REPORT_DIR/screenshots"

# Create directories
mkdir -p "$REPORT_DIR"
mkdir -p "$SCREENSHOT_DIR"

echo "========================================"
echo " Running tests for environment: $ENVIRONMENT"
echo " Browser: $BROWSER"
echo " Headless: $HEADLESS_FLAG"
echo "========================================"

# Run tests
pytest tests \
  --env "$ENVIRONMENT" \
  --browser "$BROWSER" \
  $HEADLESS_FLAG \
  -n auto \
  --reruns 2 \
  --reruns-delay 1 \
  --junitxml="$REPORT_DIR/junit_report.xml" \
  -v --disable-warnings

echo "========================================"
echo " ✅ Tests completed for $ENVIRONMENT"
echo " Reports: $REPORT_DIR"
echo " Screenshots on failure: $SCREENSHOT_DIR"
echo "========================================"
