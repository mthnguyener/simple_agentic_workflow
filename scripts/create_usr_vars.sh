#!/bin/bash
# create_usr_vars.sh

help_function()
{
    echo ""
    echo "Create usr_vars configuration file."
    echo ""
    echo "Usage: $0"
    exit 1
}

# Parse arguments
while getopts "p:" opt
do
    case $opt in
        ? ) help_function ;;
    esac
done

# Create usr_vars configuration file
INITIAL_PORT=$(( (UID - 500) * 50 + 10000 ))
printf "%s\n" \
    "USER_NAME=${USER}" \
    "PROJECT_NAME=saw" \
    "" \
    "# Data Directory" \
    "DATA_DIR=/mnt/data" \
    "" \
    "# Ports" \
    "PORT_GOOGLE=$INITIAL_PORT" \
    "PORT_JUPYTER=$((INITIAL_PORT + 1))" \
    "PORT_NGINX=$((INITIAL_PORT + 2))" \
    "PORT_PROFILE=$((INITIAL_PORT + 3))" \
    "PORT_STREAMLIT=$((INITIAL_PORT + 4))" \
    "" \
    "# API Keys" \
    "GOOGLE_API_KEY=" \
    "GROQ_API_KEY=" \
    "OPENAI_API_KEY=" \
    "" \
    > "usr_vars"
echo "Successfully created: usr_vars"

