def generate_files(input_file, lengths):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    seq1_lines = []
    seq2_lines = []
    current_seq = None

    for line in lines:
        if line.startswith('>'):
            current_seq = int(line.split()[0].split('Sequence')[1])
        else:
            if current_seq == 1:
                seq1_lines.append(line)
            elif current_seq == 2:
                seq2_lines.append(line)

    for length in lengths:
        new_seq1 = seq1_lines[:-length]
        new_seq2 = seq2_lines[:-length]
        output_file = input_file.replace('500', str(500 - length))
        with open(output_file, 'w') as f:
            f.write(f'>Sequence1\n')
            f.write(''.join(new_seq1))
            f.write(f'>Sequence2\n')
            f.write(''.join(new_seq2))

input_file = "Metha_Mala_500.fna"
lengths = [100, 200, 300, 400]
generate_files(input_file, lengths)