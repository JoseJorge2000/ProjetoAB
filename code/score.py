from Bio.Align import substitution_matrices
import csv
import os

# Define the function to extract the sequence
def extract_sequence_between_markers(file_path, start_marker, end_marker=None):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    extracting = False
    sequence = []

    for line in lines:
        if start_marker in line:
            extracting = True
            continue  # Skip the line with the start marker
        elif end_marker and end_marker in line:
            extracting = False
            break  # Stop reading when the end marker is found

        if extracting:
            # Split the line by whitespace and join columns
            columns = line.split()
            sequence.append(''.join(columns).upper())  # Convert to uppercase here

    return ''.join(sequence)

def calculate_alignment_score(seq1, seq2):
    # Load the BLOSUM62 substitution matrix
    matrix = substitution_matrices.load("BLOSUM62")

    gap_penalty = -5  # Adjust gap penalty as needed

    score = 0
    matches = 0
    mismatches = 0
    gaps = 0

    for i in range(len(seq1)):
        if seq1[i] == seq2[i]:
            if seq1[i] != '-':
                matches += 1
                score += matrix[seq1[i], seq1[i]]
        elif seq1[i] == '-' or seq2[i] == '-':
            gaps += 1
            score += gap_penalty
        else:
            mismatches += 1
            score += matrix[seq1[i], seq2[i]]

    return score, matches, mismatches, gaps

def write_results_to_csv(filename, method, score, matches, mismatches, gaps, output_file):
    filename = filename.replace("_out.fna", ".fna")  # Replace the output file name with the original file name
    
    # Read existing data
    rows = []
    try:
        with open(output_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        pass

    # Check if we need to update an existing row
    row_updated = False
    for row in rows:
        if row['Filename'] == filename and row['Algoritmo'] == method:
            row['Score'] = score
            row['Matches'] = matches
            row['Mismatches'] = mismatches
            row['Gaps'] = gaps
            row_updated = True
            break

    # Add new row if no existing row was updated
    if not row_updated:
        rows.append({
            'Filename': filename,
            'Algoritmo': method,
            'Tempo (sec)': '',
            'Score': score,
            'Matches': matches,
            'Mismatches': mismatches,
            'Gaps': gaps
        })

    # Write the data back to the file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'Algoritmo', 'Tempo (sec)', 'Score', 'Matches', 'Mismatches', 'Gaps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
#--------------------------------------------Before Alignment--------------------------------------------

# Define directories
data_dir = "Datasets/"
kalign_dir = "Kalign/"
muscle_dir = "Muscle/"
tcoffee_dir = "TCoffee/"
clustalw_dir = "ClustalW/"

# Define file names
file_names = ["EColi_Mala_100.fna", "EColi_Mala_200.fna", "EColi_Mala_300.fna", "EColi_Mala_400.fna", "EColi_Mala_500.fna", 
             "EColi_Meri_100.fna", "EColi_Meri_200.fna", "EColi_Meri_300.fna", "EColi_Meri_400.fna", "EColi_Meri_500.fna",
             "EColi_Metha_100.fna", "EColi_Metha_200.fna", "EColi_Metha_300.fna", "EColi_Metha_400.fna", "EColi_Metha_500.fna",
             "Meri_Mala_100.fna", "Meri_Mala_200.fna", "Meri_Mala_300.fna", "Meri_Mala_400.fna", "Meri_Mala_500.fna",
             "Meri_Metha_100.fna", "Meri_Metha_200.fna", "Meri_Metha_300.fna", "Meri_Metha_400.fna", "Meri_Metha_500.fna",
             "Metha_Mala_100.fna", "Metha_Mala_200.fna", "Metha_Mala_300.fna", "Metha_Mala_400.fna", "Metha_Mala_500.fna"]

# Before Alignment file paths
before_alignment_files = [data_dir + name for name in file_names]

# After Alignment Kalign file paths
after_alignment_kalign_files = [kalign_dir + name.replace(".fna", "_out.fna") for name in file_names]

# After Alignment Muscle file paths
after_alignment_muscle_files = [muscle_dir + name.replace(".fna", "_out.fna") for name in file_names]

# After Alignment TCoffee file paths
after_alignment_tcoffee_files = [tcoffee_dir + name.replace(".fna", "_out.fna") for name in file_names]

# After Alignment ClustalW file paths
after_alignment_clustalw_files = [clustalw_dir + name.replace(".fna", "_out.fna") for name in file_names]

#---------------------------------------------- Outputs --------------------------------------------------------

start_seq1 = '>Sequence1'
start_seq2 = '>Sequence2'
EOF = None

#------------------------------------------- Alignment ---------------------------------------------------------
output_file = "Resultados_test.csv"
print(before_alignment_files)

def process_alignment(file_paths, alignment_tool):
    for file_path in file_paths:
        print(file_path)
        sequence1 = extract_sequence_between_markers(file_path, start_seq1, start_seq2)
        sequence2 = extract_sequence_between_markers(file_path, start_seq2, EOF)

        alignment_name = alignment_tool
        score, matches, mismatches, gaps = calculate_alignment_score(sequence1, sequence2)
        print(f"Depois do alinhamento usando o {alignment_name}")
        print(f"Score de alinhamento: {score}")
        print(f"Matches: {matches}")
        print(f"Mismatches: {mismatches}")
        print(f"Gaps: {gaps}")
        print("\n----------------------------------------------------------------------------\n")
        
        filename = os.path.basename(file_path)  # Extract the base name from the file path
        write_results_to_csv(filename, alignment_name, score, matches, mismatches, gaps, output_file)

# Before Alignment
process_alignment(before_alignment_files, "none")

# After Alignment using Kalign
process_alignment(after_alignment_kalign_files, "kalign")

# After Alignment using Muscle
process_alignment(after_alignment_muscle_files, "muscle")

# After Alignment using TCoffee
process_alignment(after_alignment_tcoffee_files, "t_coffee")

# After Alignment using ClustalW
process_alignment(after_alignment_clustalw_files, "clustalw")