import os
import django
import sys
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from components.models import Component, RAM

INPUT_FILE = "data/ram_converted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    rams = json.load(f)

for e in rams:
    comp_data = e["component"]
    ram_data = e["ram"]

    component_obj = Component.objects.create(
        name=comp_data["name"],
        type=comp_data["type"],
        price=comp_data["price"],
        vendor=comp_data["vendor"]
    )

    RAM.objects.create(
        component=component_obj,
        ram_type=ram_data["ram_type"],
        frequency=ram_data["frequency"],
        capacity_gb=ram_data["capacity_gb"]
    )

print(f"Import done {len(rams)} RAM")
