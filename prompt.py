file_path = "components.txt"
new_file_path = "prompt.txt"
# Open the file in read mode
with open(file_path, "r") as file:
    # Read the lines of the file
    lines = file.readlines()

# Remove line breaks and join the lines into a single line
data_line = " ".join(line.strip() for line in lines)

# Replace "yellow" with "park"
data_line = data_line.replace("green", "park,")
data_line = data_line.replace("yellow", "office,")
data_line = data_line.replace("orange", "school,")
data_line = data_line.replace("blue", "house,")


with open(new_file_path, "w") as file:
    file.write(data_line+" take coordinate with map view")

