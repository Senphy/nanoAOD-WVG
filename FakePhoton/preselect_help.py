import os
import sys
import json

def preselect_json_load(jsoninput):
    with open(jsoninput, "r") as f:
        jsons = json.load(f)
        f.close()

    cutstring = ""
    for __i in jsons:
        __temp_cutstring = ""
        for __j in jsons[__i]:
            __temp_cutstring += (" && (" + jsons[__i][__j] + ")")
        cutstring += "(" + __temp_cutstring.lstrip(" &") + ") && "

    # utils cut && with others
    # __temp_cutstring = ""
    # for __i in jsons["utils"]:
    #     __temp_cutstring += (" && (" + jsons["utils"][__i] + ")")
    # cutstring += "(" + __temp_cutstring.lstrip(" &") + ") && "

    # # lepton object (muon || electron) && with others
    # __temp_cutstring = ""
    # for __i in jsons["electron"]:
    #     __temp_cutstring += (" && (" + jsons["electron"][__i] + ")")
    # cutstring += "( (" + __temp_cutstring.lstrip(" &") + ") || "
    # __temp_cutstring = ""
    # for __i in jsons["muon"]:
    #     __temp_cutstring += (" && (" + jsons["muon"][__i] + ")")
    # cutstring += "(" + __temp_cutstring.lstrip(" &") + ") ) && "

    # # photon object && with others
    # __temp_cutstring = ""
    # for __i in jsons["photon"]:
    #     __temp_cutstring += (" && (" + jsons["photon"][__i] + ")")
    # cutstring += "(" + __temp_cutstring.lstrip(" &") + ") && "


    cutstring = cutstring.rstrip(" &")
    return(cutstring)

if __name__ == "__main__":
    preselect_json_load(sys.argv[1])

