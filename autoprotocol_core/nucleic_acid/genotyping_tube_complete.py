from autoprotocol.container import WellGroup
from autoprotocol.util import make_dottable_dict

def genotyping_plate_complete(protocol, params):
    '''
    Template for genotyping_config.json file
    do not change the structure of this config file, make sure that the tubes
    containing your master mix has a key in the format of "mastermixname_MM" and
    the corresponding source DNA samples are a list of well references associated
    with a key in the parameters with the format of "mastermixname_samples"

    (change or add to default values for your run):
{
    "parameters":{
        "tail_plate": {
            "id": null,
            "type": "96-pcr",
            "storage": "cold_4",
            "discard": false
        },
        "lysis_sol": {
            "id": null,
            "type": "micro-1.5",
            "storage": "ambient",
            "discard": false
        },        
        "neut_sol": {
            "id": null,
            "type": "micro-1.5",
            "storage": "ambient",
            "discard": false
        },
        "pcr_plate": {
            "id": null,
            "type": "96-pcr",
            "storage": "cold_4",
            "discard": false
        },
        "pcr_buffer": {
            "id": null,
            "type": "micro-1.5",
            "storage": "ambient",
            "discard": false
        },
        "tail_number": 3,
        "tail_start": "tail_plate/A1",
        "lysis_incubation_time": "40:minute",
        "lysis_incubation_temp": "96:celsius",
        "lysis_sol_volume": "50:microliter",
        "neut_sol_volume": "50:microliter",
        "neut_mix_volume": "25:microliter",
        "pcr_buffer_volume": "14:microliter",
        "lysed_tail_volume": "2:microliter",

        "pcr_cycles": 30,
        "activation_time": "2:minute",
        "activation_temp": "95:celsius",
        "denaturation_time": "10:second",
        "denaturation_temp": "94:celsius",
        "annealing_time": "15:second",
        "annealing_temp": "55:celsius",
        "extension_time": "20:second",
        "extension_temp": "72:celsius"
    }
}

    '''


    params = make_dottable_dict(params)
    refs = make_dottable_dict(params.refs)
    tail_group = []
    for k, v in refs.iteritems():
        if k.startswith("tail"):
            tail_group.append(v.well(0))
    lysed_wells = WellGroup(tail_group)
    tail_number = len(lysed_wells)
    pcr_wells = refs.pcr_plate.wells_from(params.PCR_start, tail_number)


    #Lysis Neutralization
    protocol.transfer(refs.neut_sol.well(0), lysed_wells, params.neut_sol_volume, mix_after=True,
                 mix_vol=params.neut_mix_volume, repetitions=5)
    #PCR - Single Condition 
    protocol.distribute(refs.pcr_buffer.well(0), pcr_wells, params.pcr_buffer_volume, allow_carryover=True)

    protocol.transfer(lysed_wells, pcr_wells, params.lysed_tail_volume, mix_after=True, mix_vol= "5:microliter", repetitions=5)
    protocol.seal("pcr_plate")
    protocol.thermocycle(refs["pcr_plate"], [
        {"cycles": 1,
         "steps": [{
            "temperature": params.activation_temp,
            "duration": params.activation_time,
            }]
         },
         {"cycles": params.pcr_cycles,
             "steps": [
                {"temperature": params.denaturation_temp,
                 "duration": params.denaturation_time},
                {"temperature": params.annealing_temp,
                 "duration": params.annealing_time},
                {"temperature": params.extension_temp,
                 "duration": params.extension_time}
                ]
        }
    ])


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(genotyping_plate_complete)
