#!/usr/bin/env python3
import sys
from itertools import product

if len(sys.argv) < 4:
    print("Usage: python3 buat.py input.txt output.txt mode(normal/hard/extrim)")
    sys.exit(1)

# ===================== Input =====================
input_file = sys.argv[1]
output_base = sys.argv[2]
mode = sys.argv[3].lower()

with open(input_file, "r") as f:
    elements = [w.strip() for w in f if w.strip()]

# ===================== Mode settings =====================
if mode == "normal":
    min_combo, max_combo = 2, 3
    uppercase_variation = False
    spasi_opsional = False
    max_lines_per_file = None
elif mode == "hard":
    min_combo, max_combo = 2, 4
    uppercase_variation = True
    spasi_opsional = True
    max_lines_per_file = None
elif mode == "extrim":
    min_combo, max_combo = 2, 6
    uppercase_variation = True
    spasi_opsional = True
    # asumsi rata2 panjang line ~ 12 byte (perkiraan sederhana)
    avg_line_size = 12
    max_lines_per_file = int(20 * 1024**3 / avg_line_size)  
else:
    print("Mode harus salah satu dari: normal, hard, extrim")
    sys.exit(1)

# ===================== Variasi huruf =====================
def variasi_huruf(word):
    variations = [word.lower(), word.capitalize()]
    if uppercase_variation:
        variations.append(word.upper())
    return list(set(variations))

# ===================== Generate wordlist =====================
file_count = 1
line_count = 0

if max_lines_per_file:
    f = open(f"{output_base}_{file_count}.txt", "w")
else:
    f = open(f"{output_base}.txt", "w")

for n in range(min_combo, max_combo + 1):
    for combo in product(elements, repeat=n):
        variants_list = [variasi_huruf(e) for e in combo]

        stack = [("", 0)]
        while stack:
            current_str, idx = stack.pop()
            if idx == len(variants_list):
                if len(current_str.replace(" ", "")) >= 6:
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
print(f"Wordlist selesai dibuat. Total file: {file_count}" if max_lines_per_file else f"Wordlist selesai dibuat: {output_base}.txt")
