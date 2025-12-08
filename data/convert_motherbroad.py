import json
import re

INPUT_FILE = "data/motherboard.json"

OUTPUT_FILE = "data/motherboards_converted.json"


MANUAL_RATE = 77.0

def convert_mb_entry(entry, rate=None):
    name = entry.get("name")
    price_usd = entry.get("price")
    price_rub = round(price_usd * rate, 2) if price_usd and rate else price_usd

   
    chipset_match = re.search(r"(B\d{2,3}|X\d{2,3}|A\d{2,3})", name)
    chipset = chipset_match.group(0) if chipset_match else ""

    socket = entry.get("socket", "").upper()

      # RAM type based in socket
    if socket.startswith("AM5") or socket.startswith("LGA17"):  # Intel 12/13 gen
        ram_type = "DDR5"
        base_freq = 4800
    else:
        ram_type = "DDR4"
        base_freq = 3200

    # max_ram_freq — add on max_memory
    max_memory = entry.get("max_memory")
    if max_memory:
        # add: every 16 gb → +100 mGh
        increment = (max_memory // 16) * 100
        max_ram_freq = base_freq + increment
    else:
        max_ram_freq = base_freq

    return {
        "component": {
            "name": name,
            "type": "motherboard",
            "price": price_rub,
            "vendor": name.split()[0] 
        },
        "motherboard": {
            "socket": entry.get("socket", ""),
            "chipset": chipset,
            "ram_type": ram_type,
            "max_ram_freq": max_ram_freq,
            "form_factor": entry.get("form_factor", "")
        }
    }

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        mbs = json.load(f)

    converted = [convert_mb_entry(e, MANUAL_RATE) for e in mbs]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)

    print(f"Converted {len(converted)} motherboards → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
