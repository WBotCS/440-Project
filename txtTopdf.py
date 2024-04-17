import spacy
import matplotlib.pyplot as plt
import os

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

    # Create a plot using matplotlib
    fig, ax = plt.subplots()

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

# Example usage
convert_to_pdf("Test.txt")
