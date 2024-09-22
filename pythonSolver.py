from mathematicaFunctions import evaluate_mathematica_expression, evaluate_np_eq
from latexInterp import latex_print

def main(mathematica_expression):

    # Eval + convert
    latex_result = evaluate_mathematica_expression(mathematica_expression)
    print(latex_result)
    # latex wrap 
    formatted_latex_result = f"\\[{latex_result}\\]"

    pythonicPrint = input("Would you like the equation to be converted into a numpy expression, type 'y' if yes, otherwise enter any other key:")
    if pythonicPrint == "y":
        print(evaluate_np_eq(mathematica_expression))

    latexCompile = input("Would you like the latex equation to be compiled, type 'y' if yes, otherwise enter any other key: ")

    if latexCompile == "y":
        latex_print(formatted_latex_result)

if __name__ == "__main__":
    # Run the main function
    # e.g.,(Place to edit expression input)
    mathematicaFunctionExpr = "A*Cos[b]+c*e+Exp[f]*Log[m]"

    main(mathematicaFunctionExpr)
