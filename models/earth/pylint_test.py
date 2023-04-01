import os

SOURCE_LIST = (
    'constants.py',
    'utils.py',
    'xmlconverters.py',
    'logger.py',
    'language.py',
    'data.py',
    'errors.py',
    'plotgraph.py',
    'simulation.py',
    'abstractmodel.py',
    'mission.py',
    'calcmodels/ballistics.py',
    'calcmodels/control.py',
    'calcmodels/load.py',
    'calcmodels/mechanics.py',
    'calcmodels/planet.py',
    'calcmodels/power.py',
    'calcmodels/radio.py',
    'calcmodels/telemetry.py',
    'calcmodels/thermodynamics.py',
    'missions/test1',
    'missions/test2',
    'missions/test3',
    'missions/dzz',
    'missions/sms',
    'missions/inspect',
    'missions/crystal',
    'missions/molniya',
    'missions/early_warning'
    )

for src in SOURCE_LIST:
    res = os.system('pylint ' + src)
    print(src)
    assert res == 0
