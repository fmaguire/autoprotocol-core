import json
from autoprotocol.util import make_dottable_dict

def genotyping_lysis(protocol, params):
    params = make_dottable_dict(params)
    refs = make_dottable_dict(params.refs)
    lysed_wells = refs.tail_plate.wells_from(params.tail_start, params.tail_number)


    protocol.distribute(refs.lysis_sol.well(0), lysed_wells, params.lysis_sol_volume, allow_carryover=False)
    
    protocol.seal("tail_plate")

    protocol.thermocycle("tail_plate", [
        {"cycles": 1, "steps": [
            {"temperature": params.lysis_incubation_temp, "duration": params.lysis_incubation_time},
        ]},
    ])

    protocol.unseal("tail_plate")

    protocol.transfer(refs.neut_sol.well(0), lysed_wells, params.neut_sol_volume, mix_after=True,
                 mix_vol=params.neut_mix_volume, repetitions=5)

    protocol.seal("pcr_plate")

    protocol.seal("tail_plate")


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(genotyping_lysis)