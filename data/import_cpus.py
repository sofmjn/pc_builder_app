import json
import requests  # pip install requests
import os

INPUT_FILE = "data/cpu.json"  

OUTPUT_FILE = "data/cpus_converted.json"  


MANUAL_RATE = 77  

def get_usd_to_rub_rate():
    if MANUAL_RATE is not None:
        return MANUAL_RATE
    try:
        resp = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=RUB")
        data = resp.json()
        return data["rates"]["RUB"]
    except Exception as e:
        print("Not found course:", e)
        return None

def convert_cpu_entry(entry, rate):
    name = entry.get("name")
    price_usd = entry.get("price")
    if price_usd is None:
        price_rub = None
    else:
        price_rub = round(price_usd * rate, 2) if rate else None

   
    name_lower = name.lower()
    if "ryzen" in name_lower or "amd" in name_lower:
        socket = "AM5"
        chipset_support = ["A620", "B650", "B650E", "X670", "X670E"]
        vendor = "AMD"
    elif "intel" in name_lower:
        # пример, может зависеть от поколения
        socket = "LGA1700"
        chipset_support = ["B760", "Z790", "Z690"]
        vendor = "Intel"
    else:
        socket = ""
        chipset_support = []
        vendor = ""

    return {
        "component": {
            "name": name,
            "type": "cpu",
            "price": price_rub,
            "vendor": vendor
        },
        "cpu": {
            "socket": socket,
            "tdp": entry.get("tdp"),
            "chipset_support": chipset_support
        }
    }

def main():
    if not os.path.exists(INPUT_FILE):
        print("file", INPUT_FILE, "not found")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        cpus = json.load(f)

    rate = get_usd_to_rub_rate()
    print("Course USD→RUB:", rate)

    converted = []
    for e in cpus:
        converted.append(convert_cpu_entry(e, rate))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print("Done", len(converted), "CPU in", OUTPUT_FILE)

if __name__ == "__main__":
    main()
