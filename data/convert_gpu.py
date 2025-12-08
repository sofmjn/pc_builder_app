import json

INPUT_FILE = "data/gpu.json"
OUTPUT_FILE = "data/gpu_converted.json"

MANUAL_RATE = 77.0 

def estimate_tdp(entry):
   
    memory = entry.get("memory") or 0
    core_clock = entry.get("core_clock") or 0
    boost_clock = entry.get("boost_clock") or core_clock
    tdp = int(memory * 20 + (core_clock + boost_clock)/2 / 10)
    return tdp

def convert_gpu_entry(entry, rate=None):
    name = entry.get("name")
    price_usd = entry.get("price")
    price_rub = round(price_usd * rate, 2) if price_usd and rate else None

    length_mm = entry.get("length") or 250  
    tdp = entry.get("tdp") or estimate_tdp(entry)
    pcie_version = "4.0"  

    return {
        "component": {
            "name": name,
            "type": "gpu",
            "price": price_rub,
            "vendor": name.split()[0]  
        },
        "gpu": {
            "length_mm": length_mm,
            "tdp": tdp,
            "pcie_version": pcie_version
        }
    }

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        gpus = json.load(f)

    converted = [convert_gpu_entry(e, MANUAL_RATE) for e in gpus]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(converted)} GPU → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
