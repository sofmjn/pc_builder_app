# scripts/load_gpu.py
import os
import django
import sys
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from components.models import Component, GPU

INPUT_FILE = "data/gpu_converted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    gpus = json.load(f)

for e in gpus:
    comp_data = e["component"]
    gpu_data = e["gpu"]

    component_obj = Component.objects.create(
        name=comp_data["name"],
        type=comp_data["type"],
        price=comp_data["price"],
        vendor=comp_data["vendor"]
    )

    GPU.objects.create(
        component=component_obj,
        length_mm=gpu_data["length_mm"],
        tdp=gpu_data["tdp"],
        pcie_version=gpu_data["pcie_version"]
    )

print(f"Import done {len(gpus)} GPU")
