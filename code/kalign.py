import subprocess
import time
import csv

def run_docker_for_files(filenames, output, method):
    execution_times = []
    for filename in filenames:
        # Define the Docker command
        docker_command = f"docker run -v C:/Users/Utilizador/Desktop/AB/code/Datasets:/data -v C:/Users/Utilizador/Desktop/AB/code/{output}:/output biocontainers/kalign:v1-2.0320110620-5-deb_cv1 {method} -i /data/{filename} -o /output/{filename.replace('.fna', '_out.fna')}"

        # Measure the time taken by Docker command
        start_time = time.time()
        subprocess.run(docker_command, shell=True)
        docker_execution_time = time.time() - start_time

        # Store the execution time
        execution_times.append((filename, docker_execution_time))

        # Print Docker execution time
        print(f"File {filename} - Docker Execution Time: {docker_execution_time:.2f} seconds")
        
    return execution_times

def write_results_to_csv(results, method, output_file):
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['Filename', 'Algoritmo', 'Tempo (sec)', 'Score', 'Matches', 'Mismatches', 'Gaps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        for filename, execution_time in results:
            writer.writerow({'Filename': filename, 'Algoritmo': method, 'Tempo (sec)': execution_time, 'Score': '', 'Matches': '', 'Mismatches': '', "Gaps": ''})



# List of filenames
filenames = ["EColi_Mala_100.fna", "EColi_Mala_200.fna", "EColi_Mala_300.fna", "EColi_Mala_400.fna", "EColi_Mala_500.fna", 
             "EColi_Meri_100.fna", "EColi_Meri_200.fna", "EColi_Meri_300.fna", "EColi_Meri_400.fna", "EColi_Meri_500.fna",
             "EColi_Metha_100.fna", "EColi_Metha_200.fna", "EColi_Metha_300.fna", "EColi_Metha_400.fna", "EColi_Metha_500.fna",
             "Meri_Mala_100.fna", "Meri_Mala_200.fna", "Meri_Mala_300.fna", "Meri_Mala_400.fna", "Meri_Mala_500.fna",
             "Meri_Metha_100.fna", "Meri_Metha_200.fna", "Meri_Metha_300.fna", "Meri_Metha_400.fna", "Meri_Metha_500.fna",
             "Metha_Mala_100.fna", "Metha_Mala_200.fna", "Metha_Mala_300.fna", "Metha_Mala_400.fna", "Metha_Mala_500.fna"]
output = "Kalign"
method = "kalign"

# Run Docker command for each file and get execution times
execution_times = run_docker_for_files(filenames, output, method)

# Write execution times to CSV file
output_file = "Resultados.csv"
write_results_to_csv(execution_times, method, output_file)

# Print execution times at the end
print("\nExecution times:")
for filename, execution_time in execution_times:
    print(f"File {filename} - Execution Time: {execution_time:.2f} seconds")

print(f"Results written to {output_file}")