
from autoprotocol.util import make_dottable_dict

def kunkel_transform(protocol, params):
    '''
    Template for kunkel_polymerize_config.json config file
    (change or add to defaults for your run):
    {
        "parameters":{
            "resource_plate": {
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
            "polymerize_MM_vol": "2.2:microliter",
            "polymerize_MM_loc": "resource_plate/E1",
            "kunkel_number": 10,
            "reaction_start": "reaction_plate/A1"
        }
    }
    '''
    params = make_dottable_dict(params)
    refs = params.refs

    reactions = refs["reaction_plate"].wells_from(params.reaction_start, params.kunkel_number, columnwise = True)
    cell_plate = refs["cell_plate"].wells_from(params.cell_start, params.kunkel_number, columnwise=True)

    protocol.distribute(params.cells.set_volume(params.cell_tube_capacity), cell_plate, params.cell_vol_transfer, allow_carryover = True)

    protocol.transfer(reactions, cell_plate, params.DNA_transform_vol, mix_after=False)

    protocol.seal("cell_plate")

    protocol.incubate("cell_plate", "cold_4", "15:minute", shaking=False)


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_transform)
