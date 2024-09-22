# Run "pip install wolframclient" in your terminal before running the below code

# Run this file and then compile the latex document

import subprocess
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl,wlexpr

def evaluate_mathematica_expression(mathematica_expression):
    with WolframLanguageSession() as session:
        session.evaluate(wlexpr('''
        uncert[f_] := 
        Module[{var, uvar}, 
        var = Variables[DeleteDuplicates@Cases[f, _Symbol, \[Infinity]]]; 
        uvar = Symbol["\[CapitalDelta]" <> ToString[#]] & /@ var; 
        ToString[TeXForm[FullSimplify[Sqrt[
        Sum[(D[f, var[[i]]]*uvar[[i]])^2, {i, 1, Length[var]}]], 
        Assumptions -> var \[Element] Reals]]]]'''))

        uncert_eq = session.function(wlexpr('uncert'))
        eq = uncert_eq(wlexpr(mathematica_expression))
    return eq

def evaluate_np_eq(mathematica_expression):
    with WolframLanguageSession() as session:
        session.evaluate(wlexpr('''
                                uncertPython[f_] := Module[{var, funcs, uvar, temp},
  var = Variables[DeleteDuplicates@Cases[f, _Symbol, \[Infinity]]];
  uvar = Symbol["u" <> ToString[#]] & /@ var;
  temp = 
   FullSimplify[Sqrt[
    Sum[(D[f, var[[i]]]*uvar[[i]])^2, {i, 1, Length[var]}]], 
    Assumptions -> var \[Element] Reals];
  funcs = 
   StringSplit[
     ToString[InputForm[#]] & /@ 
      Complement[Variables[temp], 
       Variables[DeleteDuplicates@Cases[temp, _Symbol, \[Infinity]]]],
      "["][[;; , 1]];
  StringReplace[
   StringReplace[ToString[InputForm[temp]], 
    Join[Thread[
      ToString /@ funcs -> 
       Map[StringTemplate["np.`1`"], 
        ToString /@ ToLowerCase[funcs]]]]], {"[" -> "(", "]" -> ")", 
    "Sqrt" -> "np.sqrt", "^" -> "**", "Pi" -> "np.pi", 
    "E" -> "np.exp(1)"}]]'''))
        uncert_py_expr = session.function(wlexpr('uncertPython'))
        eq = uncert_py_expr(wlexpr(mathematica_expression))
    return eq

def create_latex_document(mathematica_expression):
    
    # Eval + convert
    latex_result = evaluate_mathematica_expression(mathematica_expression)
    print(latex_result)
    # latex wrap 
    formatted_latex_result = f"\\[{latex_result}\\]"
    
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
    with open('latexEquation.tex', 'w') as f: # Alter this line and 51 to change the output file name
        f.write(document_content)

    # Compile file to PDF
    subprocess.run(['pdflatex', 'latexEquation.tex'])

def python_eq(mathematica_expression):
    result = evaluate_np_eq(mathematica_expression)
    print(result)

if __name__ == "__main__":
    # Run the main function
    # e.g.,(Place to edit expression input)
    create_latex_document("A*Cos[b]+c*e+Exp[f]*Log[m]")

    # Alternate functionality, create the np equation 
    python_eq("A*Cos[b]+c*e+Exp[f]*Log[m]")
