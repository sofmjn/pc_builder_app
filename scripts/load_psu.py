import os
import django
import sys
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from components.models import Component, PSU

INPUT_FILE = "data/psu_converted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    psus = json.load(f)

for e in psus:
    comp_data = e["component"]
    psu_data = e["psu"]

    component_obj = Component.objects.create(
        name=comp_data["name"],
        type=comp_data["type"],
        price=comp_data["price"],
        vendor=comp_data["vendor"]
    )

    PSU.objects.create(
        component=component_obj,
        wattage=psu_data["wattage"],
        efficiency=psu_data["efficiency"]
    )

print(f"Import done {len(psus)} PSU")
