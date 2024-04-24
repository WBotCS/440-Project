import tkinter as tk
from tkinter import filedialog, messagebox
import os
import spacy
import matplotlib.pyplot as plt
from docx import Document

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_headers(text):
    doc = nlp(text)
    # Find sentences starting with capital letters
    headers = [sent.text.strip() for sent in doc.sents if sent.text[0].isupper()]
    return "\n".join(headers)

def extract_function(text):
    doc = nlp(text)
    # Find mathematical expressions using dependency parsing
    math_expressions = [token.text for token in doc if token.dep_ == "amod"]
    return " ".join(math_expressions)

def convert_to_pdf(text_file):
    # Read the text file
    with open(text_file, 'r') as file:
        function_text = file.read()

    # Extract headers
    headers = extract_headers(function_text)

    # Extract the function
    function = extract_function(function_text)

    # Create a plot using matplotlib with a fixed figure size
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # A4 size (approx.)

    # Check if there are headers
    if headers:
        # Render headers with a larger font size
        ax.text(0.5, 0.9, headers, fontsize=16, ha='center')

    # Check if the extracted function is empty (no mathematical expressions)
    if function:
        # Use LaTeX rendering for mathematical expressions
        ax.text(0.5, 0.5, f"${function}$", fontsize=12, ha='center')
    else:
        # Use default text rendering for general text
        ax.text(0.5, 0.5, function_text, fontsize=12, ha='center')

    ax.axis('off')

    # Save the plot as a PDF file
    pdf_file = os.path.splitext(text_file)[0] + '.pdf'
    plt.savefig(pdf_file, bbox_inches='tight', pad_inches=0.1)
    plt.close()

    print(f"PDF file saved as: {pdf_file}")


def convert_to_docx(text_file):
    document = Document()
    with open(text_file, 'r') as file:
        content = file.read()
        document.add_paragraph(content)
    
    docx_file = os.path.splitext(text_file)[0] + '.docx'
    document.save(docx_file)
    print(f"Word document saved as: {docx_file}")

# Function to open a file dialog and get the file path for PDF conversion
def open_file_for_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        convert_to_pdf(file_path)
        messagebox.showinfo("Success", f"PDF file has been created successfully!")

# Function to open a file dialog and get the file path for Word conversion
def open_file_for_docx():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        convert_to_docx(file_path)
        messagebox.showinfo("Success", f"Word document has been created successfully!")

# Function to open a file dialog and get the file path for HTML conversion
def open_file_for_html():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        convert_to_html(file_path)
        messagebox.showinfo("Success", f"HTML file has been created successfully!")

def convert_to_html(text_file):
    with open(text_file, 'r') as file:
        content = file.read()
    
    # Escape HTML characters in content
    content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Wrap content in basic HTML structure
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<pre>{content}</pre>
</body>
</html>
'''

    html_file = os.path.splitext(text_file)[0] + '.html'
    with open(html_file, 'w') as file:
        file.write(html_content)
    
    print(f"HTML file saved as: {html_file}")

# Set up the main application window
root = tk.Tk()
root.title("Text-File Converter")

# Window set-up
root.geometry('600x300')  # Width x Height
root.configure(bg='White')

# Configure the button size and font size to make them bigger
button_options = {
    'padx': 10,  # Add some padding on x axis
    'pady': 10,  # Add some padding on y axis
    'font': ('Roboto', 16),  # Increase the font size
    'bg': 'White'
}

# Add a button to open the file dialog for PDF conversion
open_button_pdf = tk.Button(root, text="Convert Text to PDF", command=open_file_for_pdf, **button_options)
open_button_pdf.pack(expand=True)

# Add a button to open the file dialog for Word conversion
open_button_docx = tk.Button(root, text="Convert Text to Word", command=open_file_for_docx, **button_options)
open_button_docx.pack(expand=True)

# Add a button for html conversion.
open_button_html = tk.Button(root, text="Convert Text to HTML", command=open_file_for_html, **button_options)
open_button_html.pack(expand=True)

# Start the Tkinter event loop
root.mainloop()