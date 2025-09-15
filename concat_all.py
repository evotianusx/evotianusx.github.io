import os

def concat_md_files(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(f"# {file}\n\n")  # Add a header for each file
                        outfile.write(infile.read())
                        outfile.write("\n\n")  # Add spacing between files

# Example usage
input_directory = './src'  # Replace with your directory path
output_file = 'combined_output.txt'
concat_md_files(input_directory, output_file)
