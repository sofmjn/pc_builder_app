import json

INPUT_FILE = "data/psu.json"
OUTPUT_FILE = "data/psu_converted.json"

MANUAL_RATE = 77.0  

def convert_psu_entry(entry, rate=None):
    name = entry.get("name")
    price_usd = entry.get("price")
    price_rub = round(price_usd * rate, 2) if price_usd and rate else price_usd

    return {
        "component": {
            "name": name,
            "type": "psu",
            "price": price_rub,
            "vendor": name.split()[0]  
        },
        "psu": {
            "wattage": entry.get("wattage"),
            "efficiency": entry.get("efficiency")
        }
    }

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        psus = json.load(f)

    converted = [convert_psu_entry(e, MANUAL_RATE) for e in psus]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(converted)} PSU → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
