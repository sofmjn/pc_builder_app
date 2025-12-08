from django.db import models
class CompatibilityChecker:

    def check_cpu_mobo(self, cpu, mobo):
        cpu_spec = cpu.get("specific", {})
        mobo_spec = mobo.get("specific", {})
        
        # Проверка сокета
        if cpu_spec.get("socket") != mobo_spec.get("socket"):
            return False, "Socket mismatch"
        # Проверка поддержки чипсета
        if mobo_spec.get("chipset") not in cpu_spec.get("chipset_support", []):
            return False, "Motherboard chipset is not supported by CPU"
        return True, "CPU and Motherboard are compatible"

    def check_ram_mobo(self, ram, mobo):
        ram_spec = ram.get("specific", {})
        mobo_spec = mobo.get("specific", {})
        
        if ram_spec.get("ram_type") != mobo_spec.get("ram_type"):
            return False, "RAM type mismatch"
        if ram_spec.get("frequency", 0) > mobo_spec.get("max_ram_freq", 0):
            return False, "RAM frequency too high"
        return True, "RAM fits motherboard"

    def check_gpu_case(self, gpu, case):
        gpu_spec = gpu.get("specific", {})
        case_spec = case.get("specific", {})
        
        if gpu_spec.get("length_mm", 0) > case_spec.get("max_gpu_length", 0):
            return False, "GPU does not fit case (too long)"
        return True, "GPU fits in case"

    def check_psu_power(self, cpu, gpu, psu):
        cpu_spec = cpu.get("specific", {})
        gpu_spec = gpu.get("specific", {})
        psu_spec = psu.get("specific", {})

        total_tdp = cpu_spec.get("tdp", 0) + gpu_spec.get("tdp", 0)
        if psu_spec.get("wattage", 0) < total_tdp * 1.4:
            return False, f"PSU not strong enough, need at least {int(total_tdp*1.4)}W"
        return True, "PSU wattage is sufficient"

    def check_build(self, cpu=None, gpu=None, ram=None, mobo=None, psu=None, case=None):
        result = []

        if cpu and mobo:
            result.append(self.check_cpu_mobo(cpu, mobo))
        if ram and mobo:
            result.append(self.check_ram_mobo(ram, mobo))
        if gpu and case:
            result.append(self.check_gpu_case(gpu, case))
        if psu and cpu and gpu:
            result.append(self.check_psu_power(cpu, gpu, psu))

        return result

