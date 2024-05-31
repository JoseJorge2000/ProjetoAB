import subprocess
import time
import csv
import re

def run_docker_for_files(filenames, output, method):
    dir = f"C:/Users/Utilizador/Desktop/"
    execution_times_and_scores = []
    for filename in filenames:
        # Define the Docker command
        docker_command = f"docker run -v {dir}ProjetoAB/code/Datasets:/data -v {dir}AB/code/{output}:/output biocontainers/{method}:v2.1lgpl-6-deb_cv1 {method} -INFILE=/data/{filename} -OUTFILE=/output/{filename.replace('.fna', '_out.aln')}"

        # Measure the time taken by Docker command
        start_time = time.time()
        result = subprocess.run(docker_command, shell=True, capture_output=True, text=True)
        docker_execution_time = time.time() - start_time

        # Capture the output from the Docker command
        output_text = result.stdout

        # Extract the alignment score from the output
        score_match = re.search(r"Alignment Score (\d+)", output_text)
        alignment_score = int(score_match.group(1)) if score_match else None

        # Store the execution time and score
        execution_times_and_scores.append((filename, docker_execution_time, alignment_score))

        # Print Docker execution time and alignment score
        print(f"File {filename} - Docker Execution Time: {docker_execution_time:.2f} seconds")
        print(f"Alignment Score: {alignment_score}")
        
    return execution_times_and_scores

def write_results_to_csv(results, method, output_file):
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['Filename', 'Algoritmo', 'Tempo (sec)', 'Score', 'Matches', 'Mismatches', 'Gaps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        for filename, execution_time, score in results:
            writer.writerow({'Filename': filename, 'Algoritmo': method, 'Tempo (sec)': execution_time, 'Score': score, 'Matches': '', 'Mismatches': '', "Gaps": ''})

# List of filenames
filenames = ["EColi_Mala_100.fna", "EColi_Mala_200.fna", "EColi_Mala_300.fna", "EColi_Mala_400.fna", "EColi_Mala_500.fna", 
             "EColi_Meri_100.fna", "EColi_Meri_200.fna", "EColi_Meri_300.fna", "EColi_Meri_400.fna", "EColi_Meri_500.fna",
             "EColi_Metha_100.fna", "EColi_Metha_200.fna", "EColi_Metha_300.fna", "EColi_Metha_400.fna", "EColi_Metha_500.fna",
             "Meri_Mala_100.fna", "Meri_Mala_200.fna", "Meri_Mala_300.fna", "Meri_Mala_400.fna", "Meri_Mala_500.fna",
             "Meri_Metha_100.fna", "Meri_Metha_200.fna", "Meri_Metha_300.fna", "Meri_Metha_400.fna", "Meri_Metha_500.fna",
             "Metha_Mala_100.fna", "Metha_Mala_200.fna", "Metha_Mala_300.fna", "Metha_Mala_400.fna", "Metha_Mala_500.fna"]
output = "ClustalW"
method = "clustalw"

# Run Docker command for each file and get execution times
execution_times_and_scores  = run_docker_for_files(filenames, output, method)

# Write execution times to CSV file
output_file = "Resultados.csv"
write_results_to_csv(execution_times_and_scores , method, output_file)

# Print execution times at the end
print("\nExecution times:")
for filename, execution_time, score in execution_times_and_scores:
    print(f"File {filename} - Execution Time: {execution_time:.2f} seconds - Alignment Score: {score}")

print(f"Results written to {output_file}")