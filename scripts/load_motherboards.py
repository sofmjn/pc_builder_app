import os
import django
import sys
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from components.models import Component, Motherboard

INPUT_FILE = "data/motherboards_converted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    mbs = json.load(f)

for e in mbs:
    comp_data = e["component"]
    mb_data = e["motherboard"]

    component_obj = Component.objects.create(
        name=comp_data["name"],
        type=comp_data["type"],
        price=comp_data["price"],
        vendor=comp_data["vendor"]
    )

    Motherboard.objects.create(
        component=component_obj,
        socket=mb_data["socket"],
        chipset=mb_data["chipset"],
        ram_type=mb_data["ram_type"],
        max_ram_freq=mb_data["max_ram_freq"],
        form_factor=mb_data["form_factor"]
    )

print(f"Import done {len(mbs)} motherboards")
