#!/bin/bash

# ---------- Build Docker images ----------
# 1. EXTRACT
docker build -f dags/vivino_pipeline/extract/Dockerfile -t vivino_extract:latest ./dags/vivino_pipeline/extract;
# 2. TRANSFORM
docker build -f dags/vivino_pipeline/transform/Dockerfile -t vivino_transform:latest ./dags/vivino_pipeline/transform;
# 3. LOAD
docker build -f dags/vivino_pipeline/load/Dockerfile -t vivino_load:latest ./dags/vivino_pipeline/load;
