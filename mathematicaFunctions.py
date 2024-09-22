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