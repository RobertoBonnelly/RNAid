import os
import sys
import subprocess

if len(sys.argv) < 2:
    print("Usage: python script.py <input_dir_or_file>")
    sys.exit(1)

input_path = sys.argv[1]

def run_2ndscore(input_file, output_dir="../Dataset/hairpins/"):
    os.makedirs(output_dir, exist_ok=True)  # ensure output folder exists
    output_file = os.path.join(output_dir, os.path.basename(input_file).replace(".fasta", ".out"))

    cmd = ["2ndscore", "--no-rvs", input_file]
    with open(output_file, "w") as outfile:
        subprocess.run(cmd, stdout=outfile, stderr=subprocess.PIPE)
    print(f"Processed {input_file} -> {output_file}")

# Case 1: input is a directory
if os.path.isdir(input_path):
    for filename in os.listdir(input_path):
        if filename.endswith(".fasta"):
            run_2ndscore(os.path.join(input_path, filename))

# Case 2: input is a single file
elif os.path.isfile(input_path) and input_path.endswith(".fasta"):
    run_2ndscore(input_path)

else:
    print("Error: input must be a .fasta file or a directory containing .fasta files.")
    sys.exit(1)
