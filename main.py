# with open('../itksnap/label_description.txt', 'r') as f:
#     for line in f:
#         if line.startswith('#'):
#             continue
#         columns = line.split()
#         print(f"{columns[0]}\t{' '.join(columns[7:])}")



# with open('../itksnap/label_description.txt', 'r') as f:
#     for line in f:
#         if line.startswith('#'):
#             continue
#         columns = line.split()
#         label = ' '.join(columns[7:])
#         label = label.strip('"')
#         print(f"{columns[0]}\t{label}")



# # Read label descriptions from file
# with open('../itksnap/label_description.txt', 'r') as f:
#     labels = {}
#     for line in f:
#         if line.startswith('#'):
#             continue
#         columns = line.split()
#         label_num = int(columns[0])
#         label = ' '.join(columns[7:])
#         label = label.strip('"')
#         labels[label_num] = label
#
# # Print labels and ask user to choose one or more
# chosen_labels = []
# while True:
#     for label_num, label_desc in labels.items():
#         print(f"{label_num}\t{label_desc}")
#     label_num = int(input("Choose a label number (enter -1 to exit): "))
#     if label_num == -1:
#         break
#     if label_num not in labels:
#         print("Invalid label number")
#     else:
#         chosen_labels.append((label_num, labels[label_num]))
#         print(f"You chose label {label_num}: {labels[label_num]}")
#         input("Press enter to continue...")
#     print()  # print a blank line for spacing
#
# # Print the chosen labels
# print("You chose the following labels:")
# for label_num, label_desc in chosen_labels:
#     print(f"{label_num}\t{label_desc}")

import tkinter as tk

# Read label descriptions from file
with open('itksnap/label_description.txt', 'r') as f:
    labels = {}
    for line in f:
        if line.startswith('#'):
            continue
        columns = line.split()
        label_num = int(columns[0])
        label = ' '.join(columns[7:])
        label = label.strip('"')
        labels[label_num] = label

# Create the GUI
window = tk.Tk()
window.title("Label Selector")

# Set the window size and add padding
window.geometry("400x500")
window.config(padx=20, pady=20)

# Add a title to the GUI
title = tk.Label(window, text="Choose one or more labels", font=("Helvetica", 18))
title.pack(pady=10)

# Add checkboxes for each label to the GUI
checkboxes_frame = tk.Frame(window)
checkboxes_frame.pack(pady=10)

checkboxes = {}
for label_num, label_desc in labels.items():
    var = tk.IntVar()
    checkbox = tk.Checkbutton(checkboxes_frame, text=f"{label_num}: {label_desc}", variable=var, font=("Helvetica", 14))
    checkbox.pack(anchor="w")
    checkboxes[label_num] = var

# Add a button to the GUI to submit the chosen labels
def submit_labels():
    chosen_labels = []
    for label_num, var in checkboxes.items():
        if var.get() == 1:
            chosen_labels.append((label_num, labels[label_num]))
    if len(chosen_labels) == 0:
        error_label.config(text="Please choose at least one label", fg="red")
    else:
        error_label.config(text="")
        chosen_labels_str = "\n".join([f"{label_num}\t{label_desc}" for label_num, label_desc in chosen_labels])
        chosen_labels_label.config(text=chosen_labels_str)
        chosen_labels_label.pack(pady=10)
        submit_button.config(state="disabled")

submit_button = tk.Button(window, text="Submit", font=("Helvetica", 14), command=submit_labels)
submit_button.pack(pady=10)

# Add an error label to display if no labels are chosen
error_label = tk.Label(window, text="", font=("Helvetica", 14))
error_label.pack()

# Add a label to display the chosen labels
chosen_labels_label = tk.Label(window, text="", font=("Helvetica", 14))

# Start the GUI event loop
window.mainloop()