"""This module provides the aliases of the input variables of all available models.

This file was automatically created by function |write_sequencealiases|.
"""

# import...
# ...from standard library
from typing import TYPE_CHECKING

# ...from HydPy
from hydpy.core.aliastools import LazyInOutSequenceImport

if TYPE_CHECKING:
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
    from hydpy.models.lland.lland_inputs import (
        SunshineDuration as lland_SunshineDuration,
    )
    from hydpy.models.lland.lland_inputs import Glob as lland_Glob
    from hydpy.models.lland.lland_inputs import (
        RelativeHumidity as lland_RelativeHumidity,
    )
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
else:
    evap_AirTemperature = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="AirTemperature",
        alias="evap_AirTemperature",
        namespace=locals(),
    )
    evap_RelativeHumidity = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="RelativeHumidity",
        alias="evap_RelativeHumidity",
        namespace=locals(),
    )
    evap_WindSpeed = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="WindSpeed",
        alias="evap_WindSpeed",
        namespace=locals(),
    )
    evap_SunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="SunshineDuration",
        alias="evap_SunshineDuration",
        namespace=locals(),
    )
    evap_AtmosphericPressure = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="AtmosphericPressure",
        alias="evap_AtmosphericPressure",
        namespace=locals(),
    )
    hland_P = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_inputs",
        classname="P",
        alias="hland_P",
        namespace=locals(),
    )
    hland_T = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_inputs",
        classname="T",
        alias="hland_T",
        namespace=locals(),
    )
    hland_TN = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_inputs",
        classname="TN",
        alias="hland_TN",
        namespace=locals(),
    )
    hland_EPN = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_inputs",
        classname="EPN",
        alias="hland_EPN",
        namespace=locals(),
    )
    lland_Nied = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="Nied",
        alias="lland_Nied",
        namespace=locals(),
    )
    lland_TemL = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="TemL",
        alias="lland_TemL",
        namespace=locals(),
    )
    lland_SunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="SunshineDuration",
        alias="lland_SunshineDuration",
        namespace=locals(),
    )
    lland_Glob = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="Glob",
        alias="lland_Glob",
        namespace=locals(),
    )
    lland_RelativeHumidity = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="RelativeHumidity",
        alias="lland_RelativeHumidity",
        namespace=locals(),
    )
    lland_WindSpeed = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="WindSpeed",
        alias="lland_WindSpeed",
        namespace=locals(),
    )
    lland_PET = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="PET",
        alias="lland_PET",
        namespace=locals(),
    )
    lland_AtmosphericPressure = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="AtmosphericPressure",
        alias="lland_AtmosphericPressure",
        namespace=locals(),
    )
    wland_T = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="T",
        alias="wland_T",
        namespace=locals(),
    )
    wland_P = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="P",
        alias="wland_P",
        namespace=locals(),
    )
    wland_PET = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="PET",
        alias="wland_PET",
        namespace=locals(),
    )
    wland_FXG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="FXG",
        alias="wland_FXG",
        namespace=locals(),
    )
    wland_FXS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="FXS",
        alias="wland_FXS",
        namespace=locals(),
    )
