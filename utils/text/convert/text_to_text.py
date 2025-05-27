import re


def markdown_to_latex(latex_text):
    latex_text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', latex_text, flags=re.MULTILINE)
    latex_text = re.sub(r'^## (.+)$', r'\\subsection{\1}', latex_text, flags=re.MULTILINE)
    latex_text = re.sub(r'^# (.+)$', r'\\section{\1}', latex_text, flags=re.MULTILINE)

    latex_text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', latex_text)

    latex_text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', latex_text)
    
    return latex_text