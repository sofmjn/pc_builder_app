import os
import django
import sys
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from components.models import Component, CPU  

INPUT_FILE = "data/cpus_converted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    cpus = json.load(f)

for e in cpus:
    comp_data = e["component"]
    cpu_data = e["cpu"]

   
    component_obj, created = Component.objects.get_or_create(
        name=comp_data["name"],
        type=comp_data["type"],
        defaults={
            "price": comp_data.get("price"),
            "vendor": comp_data.get("vendor"),
        }
    )

    
    if not hasattr(component_obj, "cpu"):
        CPU.objects.create(
            component=component_obj,
            socket=cpu_data.get("socket", ""),
            tdp=cpu_data.get("tdp"),
            chipset_support=cpu_data.get("chipset_support", [])
        )
print(f"Import done {len(cpus)} CPU")
