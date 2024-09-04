(* ::Package:: *)

BeginPackage["UncertaintyPropagation`"];


(*Use FileNameJoin[{$UserBaseDirectory, "Autoload"}] to find autoload directory, run InitializationValue[$InitializationContexts] = {"UncertaintyPropagation`"} to automatically load functions every time Mathematica opens*)


uncert::usage = "uncert[f] takes an input function f, and returns the propagated uncertainty based off partial derivatives. The uncertainties will be denoted using \[CapitalDelta].";


uncertPython::usage = "uncertPython[f] takes an input function f, and returns the propagated uncertainty based off partial derivatives in Python compatible form, assuming numpy is imported as np. The uncertainties will be denoted using u.";


Begin["`Private`"];


uncert[f_]:=Module[{var,funcs,uvar},
var=Variables[DeleteDuplicates@Cases[f,_Symbol,\[Infinity]]];
funcs=Complement[Variables[f],var];
uvar=Symbol["\[CapitalDelta]"<>ToString[#]]&/@var;
FullSimplify[Sqrt[Sum[(D[f,var[[i]]]*uvar[[i]])^2,{i,1,Length[var]}]],Assumptions->{var,uvar}\[Element]Reals]]


uncertPython[f_]:=Module[{var,funcs,uvar,temp},
var=Variables[DeleteDuplicates@Cases[f,_Symbol,\[Infinity]]];
uvar=Symbol["u"<>ToString[#]]&/@var;
temp=FullSimplify[Sqrt[Sum[(D[f,var[[i]]]*uvar[[i]])^2,{i,1,Length[var]}]],Assumptions->{var,uvar}\[Element]Reals];
funcs=StringSplit[ToString[InputForm[#]]&/@Complement[Variables[temp],Variables[DeleteDuplicates@Cases[temp,_Symbol,\[Infinity]]]],"["][[;;,1]];
StringReplace[StringReplace[ToString[InputForm[temp]],Join[Thread[ToString/@funcs->Map[StringTemplate["np.`1`"],ToString/@ToLowerCase[funcs]]]]],{"["->"(","]"->")","Sqrt"->"np.sqrt","^"->"**","Pi"->"np.pi","E"->"np.exp(1)"}]]


End[];


EndPackage[];
