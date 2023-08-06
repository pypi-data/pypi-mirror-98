import pickle
from pysb.simulator import SimulationResult
from pysb.simulator.base import _patch_model_setstate
from pysb.importers.sbml import model_from_biomodels

## TO Pickle:
##


def test_unpickle():
    with open('earm_1_0.pkl', 'rb') as f:
        with _patch_model_setstate():
            pickle.load(f)

def test_unpickle_pysb_1_6():
    with open('earm_1_0_pysb1.6.pkl', 'rb') as f:
        with _patch_model_setstate():
            pickle.load(f)

def test_load_legacy_h5():
    SimulationResult.load('earm_1_0_scipyodesimulator.h5')


def test_load_legacy_h5_pysb_1_6():
    SimulationResult.load('earm_1_0_scipyodesimulator_pysb1.6.h5')

def test_import_albeck_biomodels():
    model_from_biomodels('BIOMD0000000220')
