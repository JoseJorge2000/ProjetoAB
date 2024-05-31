import csv

# Open the file in read mode
with open("Resultados.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)

# Skip the header row
data = data[1:]

# Create dictionaries to store the sum and count for each file prefix and algorithm
file_sums = {}
file_counts = {}
algorithm_sums = {}
algorithm_counts = {}
number_algorithm_sums = {
    "100": {},
    "200": {},
    "300": {},
    "400": {},
    "500": {}
}
number_algorithm_counts = {
    "100": {},
    "200": {},
    "300": {},
    "400": {},
    "500": {}
}

# Calculate the sums and counts for each file prefix and algorithm
for row in data:
    # Skip rows with less than 7 columns
    if len(row) < 7:
        continue

    filename_prefix = "_".join(row[0].split("_")[:-1])
    algorithm = row[1]
    number = row[0].split("_")[-1][:-4]  # Extract the number from the filename
    key = f"{filename_prefix}_{algorithm}"
    if key not in file_sums:
        file_sums[key] = {"Tempo": 0.0, "Score": 0.0, "Matches": 0, "Mismatches": 0, "Gaps": 0}
        file_counts[key] = 0

    if algorithm not in algorithm_sums:
        algorithm_sums[algorithm] = {"Tempo": 0.0, "Score": 0.0, "Matches": 0, "Mismatches": 0, "Gaps": 0}
        algorithm_counts[algorithm] = 0

    if algorithm not in number_algorithm_sums[number]:
        number_algorithm_sums[number][algorithm] = {"Tempo": 0.0, "Score": 0.0, "Matches": 0, "Mismatches": 0, "Gaps": 0}
        number_algorithm_counts[number][algorithm] = 0

    # Replace empty strings with 0.0 for 'Tempo' and 'Score' columns
    tempo_value = row[2] if len(row) > 2 and row[2] else '0.0'
    score_value = row[3] if len(row) > 3 and row[3] else '0.0'
    file_sums[key]["Tempo"] += float(tempo_value)
    file_sums[key]["Score"] += float(score_value)
    algorithm_sums[algorithm]["Tempo"] += float(tempo_value)
    algorithm_sums[algorithm]["Score"] += float(score_value)
    number_algorithm_sums[number][algorithm]["Tempo"] += float(tempo_value)
    number_algorithm_sums[number][algorithm]["Score"] += float(score_value)

    # Check if 'Matches', 'Mismatches', and 'Gaps' columns are not empty
    if len(row) > 4 and row[4]:
        file_sums[key]["Matches"] += int(row[4])
        algorithm_sums[algorithm]["Matches"] += int(row[4])
        number_algorithm_sums[number][algorithm]["Matches"] += int(row[4])
    if len(row) > 5 and row[5]:
        file_sums[key]["Mismatches"] += int(row[5])
        algorithm_sums[algorithm]["Mismatches"] += int(row[5])
        number_algorithm_sums[number][algorithm]["Mismatches"] += int(row[5])
    if len(row) > 6 and row[6]:
        file_sums[key]["Gaps"] += int(row[6])
        algorithm_sums[algorithm]["Gaps"] += int(row[6])
        number_algorithm_sums[number][algorithm]["Gaps"] += int(row[6])

    file_counts[key] += 1
    algorithm_counts[algorithm] += 1
    number_algorithm_counts[number][algorithm] += 1

# Open the file in append mode
with open("Resultados.csv", "a", newline="") as file:
    writer = csv.writer(file)

    # Write the averages for each file prefix and algorithm
    for key in file_sums.keys():
        filename_prefix, algorithm = key.rsplit("_", 1)
        sums = file_sums[key]
        count = file_counts[key]
        row = [
            f"{filename_prefix}", algorithm,
            sums["Tempo"] / count,
            sums["Score"] / count,
            sums["Matches"] // count if sums["Matches"] else 0,
            sums["Mismatches"] // count if sums["Mismatches"] else 0,
            sums["Gaps"] // count if sums["Gaps"] else 0
        ]
        writer.writerow(row)

    # Write the averages for each algorithm
    for algorithm, sums in algorithm_sums.items():
        count = algorithm_counts[algorithm]
        row = [
            "Algorithm", algorithm,
            sums["Tempo"] / count,
            sums["Score"] / count,
            sums["Matches"] // count if sums["Matches"] else 0,
            sums["Mismatches"] // count if sums["Mismatches"] else 0,
            sums["Gaps"] // count if sums["Gaps"] else 0
        ]
        writer.writerow(row)

    # Write the averages for each algorithm and number (100, 200, 300, 400, 500)
    for number in number_algorithm_sums:
        for algorithm, sums in number_algorithm_sums[number].items():
            count = number_algorithm_counts[number][algorithm]
            row = [
                f"Number_{number}", algorithm,
                sums["Tempo"] / count,
                sums["Score"] / count,
                sums["Matches"] // count if sums["Matches"] else 0,
                sums["Mismatches"] // count if sums["Mismatches"] else 0,
                sums["Gaps"] // count if sums["Gaps"] else 0
            ]
            writer.writerow(row)