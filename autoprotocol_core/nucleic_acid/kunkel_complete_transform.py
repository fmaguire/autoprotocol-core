from autoprotocol.util import make_dottable_dict
from autoprotocol_core.nucleic_acid.kunkel_anneal import kunkel_anneal
from autoprotocol_core.nucleic_acid.kunkel_kinase import kunkel_kinase
from autoprotocol_core.nucleic_acid.kunkel_dilute import kunkel_dilute
from autoprotocol_core.nucleic_acid.kunkel_polymerize import kunkel_polymerize
from autoprotocol_core.nucleic_acid.kunkel_transform import kunkel_transform

def kunkel_complete(protocol, params):
    '''
    Template for kunkel_comlplete_config.json file
    **keep container names the same**
    (change or add to defaults for your run):
 {
        "parameters":{
            "oligo_plate": {
                "id": null,
                "type": "96-pcr",
                "storage": "cold_20",
                "discard": false
            },
            "kinased_oligo_plate": {
                "id": null,
                "type": "96-pcr",
                "storage": "cold_20",
                "discard": false
            },
            "diluted_oligo_plate": {
                "id": null,
                "type": "96-flat",
                "storage": "cold_20",
                "discard": false
            },
            "kinase_MM_1": {
                "id": null,
                "type": "micro-1.5",
                "storage": "ambient",
                "discard": false
            },
            "resource_plate_annealing_MM": {
                "id": null,
                "type": "384-pcr",
                "storage": "cold_20",
                "discard": false
            },
            "reaction_plate": {
                "id": null,
                "type": "384-pcr",
                "storage": "ambient",
                "discard": false
            },
            "H2O_1": {
                "id": null,
                "type": "micro-1.5",
                "storage": "ambient",
                "discard": false
            },
            "H2O_2": {
                "id": null,
                "type": "micro-1.5",
                "storage": "ambient",
                "discard": false
            },
            "resource_plate_polymerization_MM": {
                "id": null,
                "type": "384-pcr",
                "storage": "cold_20",
                "discard": false
            },
            "oligo_number": 4,
            "oligo_start": "oligo_plate/C2",
            "kinased_start": "kinased_oligo_plate/B2",
            "kinase_mix_loc": [
                "kinase_MM_1/0"
            ],
            "kinase_incubation_time": "1:hour",
            "kinase_incubation_temp": "37:celsius",
            "kinase_MM_volume": "23:microliter",
            "conc_oligo_volume": "7:microliter",
            "mix_volume": "10:microliter",
            "kinase_time": "60:minute",
            "kinased_oligos": [
                "kinased_oligo_plate/B2",
                "kinased_oligo_plate/C2",
                "kinased_oligo_plate/D2",
                "kinased_oligo_plate/E2"
                ],
            "combos": [[1,2,4],[2,3]],
            "water": [
                "H2O_1/0",
                "H2O_2/0"
            ],
            "water_vol": "198:microliter",
            "dilution_start": "diluted_oligo_plate/A2",
            "oligo_vol": "2:microliter",
            "ssDNA_mix_vol": "2.2:microliter",
            "ssDNA_mix_loc": "resource_plate_annealing_MM/D2",
            "oligo_vol": "2:microliter",
            "oligos": [
                "diluted_oligo_plate/A2",
                "diluted_oligo_plate/B2"
            ],
            "polymerize_MM_vol": "2.2:microliter",
            "polymerize_MM_loc": "resource_plate_polymerization_MM/E2",
            "kunkel_number": 2,
            "reaction_start": "reaction_plate/B1"
        }
    }
    '''
    params = make_dottable_dict(params)

    kunkel_kinase(protocol, params)

    protocol.unseal("kinased_oligo_plate")

    kunkel_dilute(protocol, params)

    kunkel_anneal(protocol, params)

    protocol.unseal("reaction_plate")

    kunkel_polymerize(protocol, params)

    protocol.unseal("reaction_plate")

    kunkel_transform(protocol, params)

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_complete)