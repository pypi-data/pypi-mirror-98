"""This module provides the aliases of the input variables of all available models.

This file was automatically created by function |write_sequencealiases|.
"""

# import...
# ...from HydPy
import hydpy
from hydpy.models.evap.evap_inputs import AirTemperature as evap_AirTemperature
from hydpy.models.evap.evap_inputs import RelativeHumidity as evap_RelativeHumidity
from hydpy.models.evap.evap_inputs import WindSpeed as evap_WindSpeed
from hydpy.models.evap.evap_inputs import SunshineDuration as evap_SunshineDuration
from hydpy.models.evap.evap_inputs import (
    AtmosphericPressure as evap_AtmosphericPressure,
)
from hydpy.models.hland.hland_inputs import P as hland_P
from hydpy.models.hland.hland_inputs import T as hland_T
from hydpy.models.hland.hland_inputs import TN as hland_TN
from hydpy.models.hland.hland_inputs import EPN as hland_EPN
from hydpy.models.lland.lland_inputs import Nied as lland_Nied
from hydpy.models.lland.lland_inputs import TemL as lland_TemL
from hydpy.models.lland.lland_inputs import SunshineDuration as lland_SunshineDuration
from hydpy.models.lland.lland_inputs import Glob as lland_Glob
from hydpy.models.lland.lland_inputs import RelativeHumidity as lland_RelativeHumidity
from hydpy.models.lland.lland_inputs import WindSpeed as lland_WindSpeed
from hydpy.models.lland.lland_inputs import PET as lland_PET
from hydpy.models.lland.lland_inputs import (
    AtmosphericPressure as lland_AtmosphericPressure,
)
from hydpy.models.wland.wland_inputs import T as wland_T
from hydpy.models.wland.wland_inputs import P as wland_P
from hydpy.models.wland.wland_inputs import PET as wland_PET
from hydpy.models.wland.wland_inputs import FXG as wland_FXG
from hydpy.models.wland.wland_inputs import FXS as wland_FXS

hydpy.sequence2alias[evap_AirTemperature] = "evap_AirTemperature"
hydpy.sequence2alias[evap_RelativeHumidity] = "evap_RelativeHumidity"
hydpy.sequence2alias[evap_WindSpeed] = "evap_WindSpeed"
hydpy.sequence2alias[evap_SunshineDuration] = "evap_SunshineDuration"
hydpy.sequence2alias[evap_AtmosphericPressure] = "evap_AtmosphericPressure"
hydpy.sequence2alias[hland_P] = "hland_P"
hydpy.sequence2alias[hland_T] = "hland_T"
hydpy.sequence2alias[hland_TN] = "hland_TN"
hydpy.sequence2alias[hland_EPN] = "hland_EPN"
hydpy.sequence2alias[lland_Nied] = "lland_Nied"
hydpy.sequence2alias[lland_TemL] = "lland_TemL"
hydpy.sequence2alias[lland_SunshineDuration] = "lland_SunshineDuration"
hydpy.sequence2alias[lland_Glob] = "lland_Glob"
hydpy.sequence2alias[lland_RelativeHumidity] = "lland_RelativeHumidity"
hydpy.sequence2alias[lland_WindSpeed] = "lland_WindSpeed"
hydpy.sequence2alias[lland_PET] = "lland_PET"
hydpy.sequence2alias[lland_AtmosphericPressure] = "lland_AtmosphericPressure"
hydpy.sequence2alias[wland_T] = "wland_T"
hydpy.sequence2alias[wland_P] = "wland_P"
hydpy.sequence2alias[wland_PET] = "wland_PET"
hydpy.sequence2alias[wland_FXG] = "wland_FXG"
hydpy.sequence2alias[wland_FXS] = "wland_FXS"
