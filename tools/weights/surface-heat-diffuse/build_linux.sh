#!/bin/bash
# Build the Surface Heat Diffuse Skinning solver for Linux.
# Upstream ships bin/Linux empty (gitignored) — compile from src/ with g++.
set -e
cd "$(dirname "$0")/src"
g++ *.cpp -static-libgcc -static-libstdc++ -std=c++11 -pthread -O2 \
  -o ../addon/surface_heat_diffuse_skinning/bin/Linux/shd
chmod 755 ../addon/surface_heat_diffuse_skinning/bin/Linux/shd
ls -la ../addon/surface_heat_diffuse_skinning/bin/Linux/shd
