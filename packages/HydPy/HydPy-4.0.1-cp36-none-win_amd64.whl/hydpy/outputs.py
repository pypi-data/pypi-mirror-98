"""This module provides the aliases of the output variables of all available models.

This file was automatically created by function |write_sequencealiases|.
"""

# import...
# ...from HydPy
import hydpy
from hydpy.models.arma.arma_fluxes import QIn as arma_QIn
from hydpy.models.arma.arma_fluxes import QOut as arma_QOut
from hydpy.models.conv.conv_fluxes import ActualConstant as conv_ActualConstant
from hydpy.models.conv.conv_fluxes import ActualFactor as conv_ActualFactor
from hydpy.models.dam.dam_fluxes import Inflow as dam_Inflow
from hydpy.models.dam.dam_fluxes import TotalRemoteDischarge as dam_TotalRemoteDischarge
from hydpy.models.dam.dam_fluxes import (
    NaturalRemoteDischarge as dam_NaturalRemoteDischarge,
)
from hydpy.models.dam.dam_fluxes import RemoteDemand as dam_RemoteDemand
from hydpy.models.dam.dam_fluxes import RemoteFailure as dam_RemoteFailure
from hydpy.models.dam.dam_fluxes import (
    RequiredRemoteRelease as dam_RequiredRemoteRelease,
)
from hydpy.models.dam.dam_fluxes import AllowedRemoteRelieve as dam_AllowedRemoteRelieve
from hydpy.models.dam.dam_fluxes import RequiredRemoteSupply as dam_RequiredRemoteSupply
from hydpy.models.dam.dam_fluxes import (
    PossibleRemoteRelieve as dam_PossibleRemoteRelieve,
)
from hydpy.models.dam.dam_fluxes import ActualRemoteRelieve as dam_ActualRemoteRelieve
from hydpy.models.dam.dam_fluxes import RequiredRelease as dam_RequiredRelease
from hydpy.models.dam.dam_fluxes import TargetedRelease as dam_TargetedRelease
from hydpy.models.dam.dam_fluxes import ActualRelease as dam_ActualRelease
from hydpy.models.dam.dam_fluxes import MissingRemoteRelease as dam_MissingRemoteRelease
from hydpy.models.dam.dam_fluxes import ActualRemoteRelease as dam_ActualRemoteRelease
from hydpy.models.dam.dam_fluxes import FloodDischarge as dam_FloodDischarge
from hydpy.models.dam.dam_fluxes import Outflow as dam_Outflow
from hydpy.models.dam.dam_states import WaterVolume as dam_WaterVolume
from hydpy.models.dummy.dummy_fluxes import Q as dummy_Q
from hydpy.models.evap.evap_fluxes import AdjustedWindSpeed as evap_AdjustedWindSpeed
from hydpy.models.evap.evap_fluxes import (
    SaturationVapourPressure as evap_SaturationVapourPressure,
)
from hydpy.models.evap.evap_fluxes import (
    SaturationVapourPressureSlope as evap_SaturationVapourPressureSlope,
)
from hydpy.models.evap.evap_fluxes import (
    ActualVapourPressure as evap_ActualVapourPressure,
)
from hydpy.models.evap.evap_fluxes import EarthSunDistance as evap_EarthSunDistance
from hydpy.models.evap.evap_fluxes import SolarDeclination as evap_SolarDeclination
from hydpy.models.evap.evap_fluxes import SunsetHourAngle as evap_SunsetHourAngle
from hydpy.models.evap.evap_fluxes import SolarTimeAngle as evap_SolarTimeAngle
from hydpy.models.evap.evap_fluxes import (
    ExtraterrestrialRadiation as evap_ExtraterrestrialRadiation,
)
from hydpy.models.evap.evap_fluxes import (
    PossibleSunshineDuration as evap_PossibleSunshineDuration,
)
from hydpy.models.evap.evap_fluxes import (
    ClearSkySolarRadiation as evap_ClearSkySolarRadiation,
)
from hydpy.models.evap.evap_fluxes import GlobalRadiation as evap_GlobalRadiation
from hydpy.models.evap.evap_fluxes import (
    NetShortwaveRadiation as evap_NetShortwaveRadiation,
)
from hydpy.models.evap.evap_fluxes import (
    NetLongwaveRadiation as evap_NetLongwaveRadiation,
)
from hydpy.models.evap.evap_fluxes import NetRadiation as evap_NetRadiation
from hydpy.models.evap.evap_fluxes import SoilHeatFlux as evap_SoilHeatFlux
from hydpy.models.evap.evap_fluxes import (
    PsychrometricConstant as evap_PsychrometricConstant,
)
from hydpy.models.evap.evap_fluxes import (
    ReferenceEvapotranspiration as evap_ReferenceEvapotranspiration,
)
from hydpy.models.hbranch.hbranch_fluxes import Input as hbranch_Input
from hydpy.models.hland.hland_fluxes import TMean as hland_TMean
from hydpy.models.hland.hland_fluxes import ContriArea as hland_ContriArea
from hydpy.models.hland.hland_fluxes import InUZ as hland_InUZ
from hydpy.models.hland.hland_fluxes import Perc as hland_Perc
from hydpy.models.hland.hland_fluxes import Q0 as hland_Q0
from hydpy.models.hland.hland_fluxes import Q1 as hland_Q1
from hydpy.models.hland.hland_fluxes import InUH as hland_InUH
from hydpy.models.hland.hland_fluxes import OutUH as hland_OutUH
from hydpy.models.hland.hland_fluxes import QT as hland_QT
from hydpy.models.hland.hland_states import UZ as hland_UZ
from hydpy.models.hland.hland_states import LZ as hland_LZ
from hydpy.models.llake.llake_fluxes import QZ as llake_QZ
from hydpy.models.llake.llake_fluxes import QA as llake_QA
from hydpy.models.llake.llake_states import V as llake_V
from hydpy.models.llake.llake_states import W as llake_W
from hydpy.models.lland.lland_fluxes import QZ as lland_QZ
from hydpy.models.lland.lland_fluxes import QZH as lland_QZH
from hydpy.models.lland.lland_fluxes import TemLTag as lland_TemLTag
from hydpy.models.lland.lland_fluxes import (
    DailyRelativeHumidity as lland_DailyRelativeHumidity,
)
from hydpy.models.lland.lland_fluxes import (
    DailySunshineDuration as lland_DailySunshineDuration,
)
from hydpy.models.lland.lland_fluxes import WindSpeed2m as lland_WindSpeed2m
from hydpy.models.lland.lland_fluxes import DailyWindSpeed2m as lland_DailyWindSpeed2m
from hydpy.models.lland.lland_fluxes import WindSpeed10m as lland_WindSpeed10m
from hydpy.models.lland.lland_fluxes import SolarDeclination as lland_SolarDeclination
from hydpy.models.lland.lland_fluxes import TSA as lland_TSA
from hydpy.models.lland.lland_fluxes import TSU as lland_TSU
from hydpy.models.lland.lland_fluxes import EarthSunDistance as lland_EarthSunDistance
from hydpy.models.lland.lland_fluxes import (
    ExtraterrestrialRadiation as lland_ExtraterrestrialRadiation,
)
from hydpy.models.lland.lland_fluxes import (
    PossibleSunshineDuration as lland_PossibleSunshineDuration,
)
from hydpy.models.lland.lland_fluxes import (
    DailyPossibleSunshineDuration as lland_DailyPossibleSunshineDuration,
)
from hydpy.models.lland.lland_fluxes import (
    DailyGlobalRadiation as lland_DailyGlobalRadiation,
)
from hydpy.models.lland.lland_fluxes import SP as lland_SP
from hydpy.models.lland.lland_fluxes import GlobalRadiation as lland_GlobalRadiation
from hydpy.models.lland.lland_fluxes import (
    AdjustedGlobalRadiation as lland_AdjustedGlobalRadiation,
)
from hydpy.models.lland.lland_fluxes import QDGZ as lland_QDGZ
from hydpy.models.lland.lland_fluxes import QAH as lland_QAH
from hydpy.models.lland.lland_fluxes import QA as lland_QA
from hydpy.models.lland.lland_states import QDGZ1 as lland_QDGZ1
from hydpy.models.lland.lland_states import QDGZ2 as lland_QDGZ2
from hydpy.models.lland.lland_states import QIGZ1 as lland_QIGZ1
from hydpy.models.lland.lland_states import QIGZ2 as lland_QIGZ2
from hydpy.models.lland.lland_states import QBGZ as lland_QBGZ
from hydpy.models.lland.lland_states import QDGA1 as lland_QDGA1
from hydpy.models.lland.lland_states import QDGA2 as lland_QDGA2
from hydpy.models.lland.lland_states import QIGA1 as lland_QIGA1
from hydpy.models.lland.lland_states import QIGA2 as lland_QIGA2
from hydpy.models.lland.lland_states import QBGA as lland_QBGA
from hydpy.models.lstream.lstream_fluxes import QZ as lstream_QZ
from hydpy.models.lstream.lstream_fluxes import QZA as lstream_QZA
from hydpy.models.lstream.lstream_fluxes import QA as lstream_QA
from hydpy.models.test.test_fluxes import Q as test_Q
from hydpy.models.test.test_states import S as test_S
from hydpy.models.wland.wland_fluxes import PC as wland_PC
from hydpy.models.wland.wland_fluxes import PES as wland_PES
from hydpy.models.wland.wland_fluxes import PS as wland_PS
from hydpy.models.wland.wland_fluxes import PV as wland_PV
from hydpy.models.wland.wland_fluxes import PQ as wland_PQ
from hydpy.models.wland.wland_fluxes import ETV as wland_ETV
from hydpy.models.wland.wland_fluxes import ES as wland_ES
from hydpy.models.wland.wland_fluxes import ET as wland_ET
from hydpy.models.wland.wland_fluxes import FXS as wland_FXS
from hydpy.models.wland.wland_fluxes import FXG as wland_FXG
from hydpy.models.wland.wland_fluxes import CDG as wland_CDG
from hydpy.models.wland.wland_fluxes import FGS as wland_FGS
from hydpy.models.wland.wland_fluxes import FQS as wland_FQS
from hydpy.models.wland.wland_fluxes import RH as wland_RH
from hydpy.models.wland.wland_fluxes import R as wland_R
from hydpy.models.wland.wland_states import DV as wland_DV
from hydpy.models.wland.wland_states import DG as wland_DG
from hydpy.models.wland.wland_states import HQ as wland_HQ
from hydpy.models.wland.wland_states import HS as wland_HS

hydpy.sequence2alias[arma_QIn] = "arma_QIn"
hydpy.sequence2alias[arma_QOut] = "arma_QOut"
hydpy.sequence2alias[conv_ActualConstant] = "conv_ActualConstant"
hydpy.sequence2alias[conv_ActualFactor] = "conv_ActualFactor"
hydpy.sequence2alias[dam_Inflow] = "dam_Inflow"
hydpy.sequence2alias[dam_TotalRemoteDischarge] = "dam_TotalRemoteDischarge"
hydpy.sequence2alias[dam_NaturalRemoteDischarge] = "dam_NaturalRemoteDischarge"
hydpy.sequence2alias[dam_RemoteDemand] = "dam_RemoteDemand"
hydpy.sequence2alias[dam_RemoteFailure] = "dam_RemoteFailure"
hydpy.sequence2alias[dam_RequiredRemoteRelease] = "dam_RequiredRemoteRelease"
hydpy.sequence2alias[dam_AllowedRemoteRelieve] = "dam_AllowedRemoteRelieve"
hydpy.sequence2alias[dam_RequiredRemoteSupply] = "dam_RequiredRemoteSupply"
hydpy.sequence2alias[dam_PossibleRemoteRelieve] = "dam_PossibleRemoteRelieve"
hydpy.sequence2alias[dam_ActualRemoteRelieve] = "dam_ActualRemoteRelieve"
hydpy.sequence2alias[dam_RequiredRelease] = "dam_RequiredRelease"
hydpy.sequence2alias[dam_TargetedRelease] = "dam_TargetedRelease"
hydpy.sequence2alias[dam_ActualRelease] = "dam_ActualRelease"
hydpy.sequence2alias[dam_MissingRemoteRelease] = "dam_MissingRemoteRelease"
hydpy.sequence2alias[dam_ActualRemoteRelease] = "dam_ActualRemoteRelease"
hydpy.sequence2alias[dam_FloodDischarge] = "dam_FloodDischarge"
hydpy.sequence2alias[dam_Outflow] = "dam_Outflow"
hydpy.sequence2alias[dam_WaterVolume] = "dam_WaterVolume"
hydpy.sequence2alias[dummy_Q] = "dummy_Q"
hydpy.sequence2alias[evap_AdjustedWindSpeed] = "evap_AdjustedWindSpeed"
hydpy.sequence2alias[evap_SaturationVapourPressure] = "evap_SaturationVapourPressure"
hydpy.sequence2alias[
    evap_SaturationVapourPressureSlope
] = "evap_SaturationVapourPressureSlope"
hydpy.sequence2alias[evap_ActualVapourPressure] = "evap_ActualVapourPressure"
hydpy.sequence2alias[evap_EarthSunDistance] = "evap_EarthSunDistance"
hydpy.sequence2alias[evap_SolarDeclination] = "evap_SolarDeclination"
hydpy.sequence2alias[evap_SunsetHourAngle] = "evap_SunsetHourAngle"
hydpy.sequence2alias[evap_SolarTimeAngle] = "evap_SolarTimeAngle"
hydpy.sequence2alias[evap_ExtraterrestrialRadiation] = "evap_ExtraterrestrialRadiation"
hydpy.sequence2alias[evap_PossibleSunshineDuration] = "evap_PossibleSunshineDuration"
hydpy.sequence2alias[evap_ClearSkySolarRadiation] = "evap_ClearSkySolarRadiation"
hydpy.sequence2alias[evap_GlobalRadiation] = "evap_GlobalRadiation"
hydpy.sequence2alias[evap_NetShortwaveRadiation] = "evap_NetShortwaveRadiation"
hydpy.sequence2alias[evap_NetLongwaveRadiation] = "evap_NetLongwaveRadiation"
hydpy.sequence2alias[evap_NetRadiation] = "evap_NetRadiation"
hydpy.sequence2alias[evap_SoilHeatFlux] = "evap_SoilHeatFlux"
hydpy.sequence2alias[evap_PsychrometricConstant] = "evap_PsychrometricConstant"
hydpy.sequence2alias[
    evap_ReferenceEvapotranspiration
] = "evap_ReferenceEvapotranspiration"
hydpy.sequence2alias[hbranch_Input] = "hbranch_Input"
hydpy.sequence2alias[hland_TMean] = "hland_TMean"
hydpy.sequence2alias[hland_ContriArea] = "hland_ContriArea"
hydpy.sequence2alias[hland_InUZ] = "hland_InUZ"
hydpy.sequence2alias[hland_Perc] = "hland_Perc"
hydpy.sequence2alias[hland_Q0] = "hland_Q0"
hydpy.sequence2alias[hland_Q1] = "hland_Q1"
hydpy.sequence2alias[hland_InUH] = "hland_InUH"
hydpy.sequence2alias[hland_OutUH] = "hland_OutUH"
hydpy.sequence2alias[hland_QT] = "hland_QT"
hydpy.sequence2alias[hland_UZ] = "hland_UZ"
hydpy.sequence2alias[hland_LZ] = "hland_LZ"
hydpy.sequence2alias[llake_QZ] = "llake_QZ"
hydpy.sequence2alias[llake_QA] = "llake_QA"
hydpy.sequence2alias[llake_V] = "llake_V"
hydpy.sequence2alias[llake_W] = "llake_W"
hydpy.sequence2alias[lland_QZ] = "lland_QZ"
hydpy.sequence2alias[lland_QZH] = "lland_QZH"
hydpy.sequence2alias[lland_TemLTag] = "lland_TemLTag"
hydpy.sequence2alias[lland_DailyRelativeHumidity] = "lland_DailyRelativeHumidity"
hydpy.sequence2alias[lland_DailySunshineDuration] = "lland_DailySunshineDuration"
hydpy.sequence2alias[lland_WindSpeed2m] = "lland_WindSpeed2m"
hydpy.sequence2alias[lland_DailyWindSpeed2m] = "lland_DailyWindSpeed2m"
hydpy.sequence2alias[lland_WindSpeed10m] = "lland_WindSpeed10m"
hydpy.sequence2alias[lland_SolarDeclination] = "lland_SolarDeclination"
hydpy.sequence2alias[lland_TSA] = "lland_TSA"
hydpy.sequence2alias[lland_TSU] = "lland_TSU"
hydpy.sequence2alias[lland_EarthSunDistance] = "lland_EarthSunDistance"
hydpy.sequence2alias[
    lland_ExtraterrestrialRadiation
] = "lland_ExtraterrestrialRadiation"
hydpy.sequence2alias[lland_PossibleSunshineDuration] = "lland_PossibleSunshineDuration"
hydpy.sequence2alias[
    lland_DailyPossibleSunshineDuration
] = "lland_DailyPossibleSunshineDuration"
hydpy.sequence2alias[lland_DailyGlobalRadiation] = "lland_DailyGlobalRadiation"
hydpy.sequence2alias[lland_SP] = "lland_SP"
hydpy.sequence2alias[lland_GlobalRadiation] = "lland_GlobalRadiation"
hydpy.sequence2alias[lland_AdjustedGlobalRadiation] = "lland_AdjustedGlobalRadiation"
hydpy.sequence2alias[lland_QDGZ] = "lland_QDGZ"
hydpy.sequence2alias[lland_QAH] = "lland_QAH"
hydpy.sequence2alias[lland_QA] = "lland_QA"
hydpy.sequence2alias[lland_QDGZ1] = "lland_QDGZ1"
hydpy.sequence2alias[lland_QDGZ2] = "lland_QDGZ2"
hydpy.sequence2alias[lland_QIGZ1] = "lland_QIGZ1"
hydpy.sequence2alias[lland_QIGZ2] = "lland_QIGZ2"
hydpy.sequence2alias[lland_QBGZ] = "lland_QBGZ"
hydpy.sequence2alias[lland_QDGA1] = "lland_QDGA1"
hydpy.sequence2alias[lland_QDGA2] = "lland_QDGA2"
hydpy.sequence2alias[lland_QIGA1] = "lland_QIGA1"
hydpy.sequence2alias[lland_QIGA2] = "lland_QIGA2"
hydpy.sequence2alias[lland_QBGA] = "lland_QBGA"
hydpy.sequence2alias[lstream_QZ] = "lstream_QZ"
hydpy.sequence2alias[lstream_QZA] = "lstream_QZA"
hydpy.sequence2alias[lstream_QA] = "lstream_QA"
hydpy.sequence2alias[test_Q] = "test_Q"
hydpy.sequence2alias[test_S] = "test_S"
hydpy.sequence2alias[wland_PC] = "wland_PC"
hydpy.sequence2alias[wland_PES] = "wland_PES"
hydpy.sequence2alias[wland_PS] = "wland_PS"
hydpy.sequence2alias[wland_PV] = "wland_PV"
hydpy.sequence2alias[wland_PQ] = "wland_PQ"
hydpy.sequence2alias[wland_ETV] = "wland_ETV"
hydpy.sequence2alias[wland_ES] = "wland_ES"
hydpy.sequence2alias[wland_ET] = "wland_ET"
hydpy.sequence2alias[wland_FXS] = "wland_FXS"
hydpy.sequence2alias[wland_FXG] = "wland_FXG"
hydpy.sequence2alias[wland_CDG] = "wland_CDG"
hydpy.sequence2alias[wland_FGS] = "wland_FGS"
hydpy.sequence2alias[wland_FQS] = "wland_FQS"
hydpy.sequence2alias[wland_RH] = "wland_RH"
hydpy.sequence2alias[wland_R] = "wland_R"
hydpy.sequence2alias[wland_DV] = "wland_DV"
hydpy.sequence2alias[wland_DG] = "wland_DG"
hydpy.sequence2alias[wland_HQ] = "wland_HQ"
hydpy.sequence2alias[wland_HS] = "wland_HS"
