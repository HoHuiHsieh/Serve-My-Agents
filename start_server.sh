#!/bin/bash

# Start the FastAPI server with Hypercorn

echo "Starting AI Agents API with Hypercorn..."
hypercorn main:app --config python:hypercorn_config
