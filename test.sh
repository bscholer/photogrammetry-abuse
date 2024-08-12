#!/bin/bash

# Paths
INPUT_DIR="./images/baywatch_resort"
OUTPUT_BASE_DIR="./output"
SCRIPT="python3 image_processing.py"

# Output directories for each experiment
OUTPUT_COLOR_BANDS="${OUTPUT_BASE_DIR}/color_bands"
OUTPUT_MONOCHROME="${OUTPUT_BASE_DIR}/monochrome"
OUTPUT_INVERTED="${OUTPUT_BASE_DIR}/inverted"
OUTPUT_NO_GPS="${OUTPUT_BASE_DIR}/no_gps"
OUTPUT_TIMESTAMP="${OUTPUT_BASE_DIR}/timestamp"
OUTPUT_NOISE="${OUTPUT_BASE_DIR}/noise"
OUTPUT_PERSPECTIVE="${OUTPUT_BASE_DIR}/perspective"
OUTPUT_TILT="${OUTPUT_BASE_DIR}/tilt"

# Function to clear output directory
clear_output_dir() {
    if [ -d "$1" ]; then
        rm -rf "$1"/*
    else
        mkdir -p "$1"
    fi
}

# Run color bands experiment
clear_output_dir "$OUTPUT_COLOR_BANDS"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_COLOR_BANDS" -e color-bands -b rg

# Run monochrome experiment
clear_output_dir "$OUTPUT_MONOCHROME"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_MONOCHROME" -e monochrome -p 50

# Run inverted experiment
clear_output_dir "$OUTPUT_INVERTED"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_INVERTED" -e inverted -f 50 -m 50

# Run no-gps experiment
clear_output_dir "$OUTPUT_NO_GPS"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_NO_GPS" -e no-gps -p 50

# Run timestamp experiment
clear_output_dir "$OUTPUT_TIMESTAMP"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_TIMESTAMP" -e timestamp --start-date "2024-01-01" --end-date "2024-01-31"

# Run noise experiment
clear_output_dir "$OUTPUT_NOISE"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_NOISE" -e noise --noise-level 50

# Run perspective experiment
clear_output_dir "$OUTPUT_PERSPECTIVE"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_PERSPECTIVE" -e perspective -p 50 --warp-by 10

# Run tilt experiment
clear_output_dir "$OUTPUT_TILT"
$SCRIPT -i "$INPUT_DIR" -o "$OUTPUT_TILT" -e tilt -p 75 --max-tilt 10

echo "All experiments completed. Check the output directories for results."
