import json

INPUT_FILE = "data/ram.json"
OUTPUT_FILE = "data/ram_converted.json"

MANUAL_RATE = 77.0 

def convert_ram_entry(entry, rate=None):
    name = entry.get("name")
    price_usd = entry.get("price")
    price_rub = round(price_usd * rate, 2) if price_usd and rate else price_usd

    
    speed = entry.get("speed", [])
    if isinstance(speed, int):
        # если просто число, превращаем в список [0, число], чтобы второй элемент был частотой
        speed = [0, speed]
    if speed and len(speed) > 1:
        frequency = speed[1]  # берем второе значение, как MHz
        ram_type = "DDR5" if frequency >= 4800 else "DDR4"
    else:
        frequency = None
        ram_type = "DDR4"

    # capacity_gb —  modules
    modules = entry.get("modules", [])
    if modules and len(modules) == 2:
        num_modules, size_per_module = modules
        capacity_gb = num_modules * size_per_module
    else:
        capacity_gb = None

    return {
        "component": {
            "name": name,
            "type": "ram",
            "price": price_rub,
            "vendor": name.split()[0] 
        },
        "ram": {
            "ram_type": ram_type,
            "frequency": frequency,
            "capacity_gb": capacity_gb
        }
    }

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        rams = json.load(f)

    converted = [convert_ram_entry(e, MANUAL_RATE) for e in rams]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(converted)} RAM → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
