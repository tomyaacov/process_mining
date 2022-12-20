import pm4py
from pm4py.algo.analysis.woflan import algorithm as woflan

models = [
"AD14_models/ad14_model_inductive.pnml",
"AD14_models/ad14_model_alpha.pnml",
"AD14_models/ad14_model_alpha_plus.pnml",
"AD14_models/ad14_model_heuristic.pnml",
"ttt_models/ttt_model_inductive.pnml",
"ttt_models/ttt_model_alpha.pnml",
"ttt_models/ttt_model_alpha_plus.pnml",
"ttt_models/ttt_model_heuristic.pnml",
]

for name in models:
    net, initial_marking, final_marking = pm4py.read_pnml(name)
    is_sound = woflan.apply(net, initial_marking, final_marking,
                            parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
                                        woflan.Parameters.PRINT_DIAGNOSTICS: False,
                                        woflan.Parameters.RETURN_DIAGNOSTICS: False})
    print(name)
    print("is_sound:", is_sound)





