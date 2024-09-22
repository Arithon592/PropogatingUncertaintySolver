import subprocess

def latex_print(formatted_latex_result):
    fileName = input("Please type the file name you would like to print to: ") + ".tex"
    # latex template
    document_template = r"""
    \documentclass{article}
    \usepackage{amsmath}
    \begin{document}

    The equation is given by:
    %s

    \end{document}
    """

    document_content = document_template % formatted_latex_result

    # Write into tex file
    with open(fileName, 'w') as f: 
        f.write(document_content)

    # Compile file to PDF
    subprocess.run(['pdflatex', fileName])
