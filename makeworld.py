#!/usr/bin/env python3
import sys
from itertools import product
from math import ceil

# ===================== Input =====================
if len(sys.argv) < 4:
    print("Usage: python3 generate.py elemen1,elemen2,... output_basename mode(normal/hard/extrim)")
    sys.exit(1)

elements_input = sys.argv[1].split(",")
output_base = sys.argv[2]
mode = sys.argv[3].lower()

# ===================== Mode settings =====================
if mode == "normal":
    min_combo, max_combo = 2, 3
    uppercase_variation = False
    spasi_opsional = False
    max_lines_per_file = None  # single file
elif mode == "hard":
    min_combo, max_combo = 2, 4
    uppercase_variation = True
    spasi_opsional = True
    max_lines_per_file = None  # single file
elif mode == "extrim":
    min_combo, max_combo = 2, 6
    uppercase_variation = True
    spasi_opsional = True
    max_lines_per_file = 1_000_000  # default, nanti dihitung ulang jika >20GB
else:
    print("Mode harus salah satu dari: normal, hard, extrim")
    sys.exit(1)

# ===================== Pisahkan nama & elemen lain =====================
nama = [e for e in elements_input if e.isalpha()]
other_elements = [e for e in elements_input if not e.isalpha()]

# Variasi tanggal lahir
tgl_bulan_thn = [e for e in elements_input if e.isdigit()]
tgl_variations = set()
for e in tgl_bulan_thn:
    if len(e) == 8:
        tgl_variations.update([e, e[2:], e[4:], e[:2], e[:4]])
    elif len(e) == 6:
        tgl_variations.update([e, e[2:], e[:2], e[:4]])
    else:
        tgl_variations.add(e)

all_elements = nama + list(tgl_variations) + [e for e in elements_input if not e.isalpha() and e not in tgl_variations]

# ===================== Fungsi variasi huruf =====================
def variasi_huruf(word):
    if word in nama:
        variations = [word.lower(), word.capitalize()]
        if uppercase_variation:
            variations.append(word.upper())
        return variations
    return [word]

# ===================== Estimasi ukuran realistis =====================
num_variations_per_element = [len(variasi_huruf(e)) for e in all_elements]
avg_len = sum(len(e)+1 for e in all_elements)/len(all_elements)  # +1 untuk spasi opsional

total_combos = 0
for n in range(min_combo, max_combo+1):
    total_combos += (sum(num_variations_per_element) ** n)

estimated_gb = total_combos * avg_len / (1024**3)

# ===================== Penyesuaian max_lines_per_file =====================
if mode == "extrim" and estimated_gb > 20:
    # hitung baris kira-kira per 20GB
    avg_line_size = avg_len  # byte per line aproksimasi
    lines_per_20gb = int(20 * 1024**3 / avg_line_size)
    max_lines_per_file = lines_per_20gb
else:
    max_lines_per_file = None  # single file

print(f"Perkiraan ukuran wordlist: {estimated_gb:.2f} GB")
proceed = input("Lanjutkan? (y/n): ").lower()
if proceed != "y":
    sys.exit(0)

# ===================== Generate wordlist =====================
file_count = 1
line_count = 0
if max_lines_per_file:
    f = open(f"{output_base}_{file_count}.txt", "w")
else:
    f = open(f"{output_base}.txt", "w")

for n in range(min_combo, max_combo+1):
    for combo in product(all_elements, repeat=n):
        variants_list = [variasi_huruf(e) for e in combo]
        stack = [("", 0)]
        while stack:
            current_str, idx = stack.pop()
            if idx == len(variants_list):
                if len(current_str.replace(" ","")) >= 6:
                    f.write(current_str + "\n")
                    line_count += 1
                    if max_lines_per_file and line_count >= max_lines_per_file:
                        f.close()
                        file_count += 1
                        line_count = 0
                        f = open(f"{output_base}_{file_count}.txt", "w")
                continue
            for variant in variants_list[idx]:
                stack.append((current_str + variant, idx + 1))
                if spasi_opsional and current_str:
                    stack.append((current_str + " " + variant, idx + 1))

f.close()
if max_lines_per_file:
    print(f"Wordlist selesai dibuat, total file: {file_count}")
else:
    print(f"Wordlist selesai dibuat: {output_base}.txt")
