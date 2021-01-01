#!/bin/bash


# Configuration
SRC="../../../res/main/readme"
README="../../../README.md"

# Main script
cat ${SRC}/README_1.md > ${README}
./generate-usage.sh >> ${README}
