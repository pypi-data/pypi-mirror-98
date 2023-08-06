"""This module provides the aliases of the output variables of all available models.

This file was automatically created by function |write_sequencealiases|.
"""

# import...
# ...from standard library
from typing import TYPE_CHECKING

# ...from HydPy
from hydpy.core.aliastools import LazyInOutSequenceImport

if TYPE_CHECKING:
    from hydpy.models.arma.arma_fluxes import QIn as arma_QIn
    from hydpy.models.arma.arma_fluxes import QOut as arma_QOut
    from hydpy.models.conv.conv_fluxes import ActualConstant as conv_ActualConstant
    from hydpy.models.conv.conv_fluxes import ActualFactor as conv_ActualFactor
    from hydpy.models.dam.dam_fluxes import Inflow as dam_Inflow
    from hydpy.models.dam.dam_fluxes import (
        TotalRemoteDischarge as dam_TotalRemoteDischarge,
    )
    from hydpy.models.dam.dam_fluxes import (
        NaturalRemoteDischarge as dam_NaturalRemoteDischarge,
    )
    from hydpy.models.dam.dam_fluxes import RemoteDemand as dam_RemoteDemand
    from hydpy.models.dam.dam_fluxes import RemoteFailure as dam_RemoteFailure
    from hydpy.models.dam.dam_fluxes import (
        RequiredRemoteRelease as dam_RequiredRemoteRelease,
    )
    from hydpy.models.dam.dam_fluxes import (
        AllowedRemoteRelieve as dam_AllowedRemoteRelieve,
    )
    from hydpy.models.dam.dam_fluxes import (
        RequiredRemoteSupply as dam_RequiredRemoteSupply,
    )
    from hydpy.models.dam.dam_fluxes import (
        PossibleRemoteRelieve as dam_PossibleRemoteRelieve,
    )
    from hydpy.models.dam.dam_fluxes import (
        ActualRemoteRelieve as dam_ActualRemoteRelieve,
    )
    from hydpy.models.dam.dam_fluxes import RequiredRelease as dam_RequiredRelease
    from hydpy.models.dam.dam_fluxes import TargetedRelease as dam_TargetedRelease
    from hydpy.models.dam.dam_fluxes import ActualRelease as dam_ActualRelease
    from hydpy.models.dam.dam_fluxes import (
        MissingRemoteRelease as dam_MissingRemoteRelease,
    )
    from hydpy.models.dam.dam_fluxes import (
        ActualRemoteRelease as dam_ActualRemoteRelease,
    )
    from hydpy.models.dam.dam_fluxes import FloodDischarge as dam_FloodDischarge
    from hydpy.models.dam.dam_fluxes import Outflow as dam_Outflow
    from hydpy.models.dam.dam_states import WaterVolume as dam_WaterVolume
    from hydpy.models.dummy.dummy_fluxes import Q as dummy_Q
    from hydpy.models.evap.evap_fluxes import (
        AdjustedWindSpeed as evap_AdjustedWindSpeed,
    )
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
    from hydpy.models.lland.lland_fluxes import (
        DailyWindSpeed2m as lland_DailyWindSpeed2m,
    )
    from hydpy.models.lland.lland_fluxes import WindSpeed10m as lland_WindSpeed10m
    from hydpy.models.lland.lland_fluxes import (
        SolarDeclination as lland_SolarDeclination,
    )
    from hydpy.models.lland.lland_fluxes import TSA as lland_TSA
    from hydpy.models.lland.lland_fluxes import TSU as lland_TSU
    from hydpy.models.lland.lland_fluxes import (
        EarthSunDistance as lland_EarthSunDistance,
    )
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
else:
    arma_QIn = LazyInOutSequenceImport(
        modulename="hydpy.models.arma.arma_fluxes",
        classname="QIn",
        alias="arma_QIn",
        namespace=locals(),
    )
    arma_QOut = LazyInOutSequenceImport(
        modulename="hydpy.models.arma.arma_fluxes",
        classname="QOut",
        alias="arma_QOut",
        namespace=locals(),
    )
    conv_ActualConstant = LazyInOutSequenceImport(
        modulename="hydpy.models.conv.conv_fluxes",
        classname="ActualConstant",
        alias="conv_ActualConstant",
        namespace=locals(),
    )
    conv_ActualFactor = LazyInOutSequenceImport(
        modulename="hydpy.models.conv.conv_fluxes",
        classname="ActualFactor",
        alias="conv_ActualFactor",
        namespace=locals(),
    )
    dam_Inflow = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="Inflow",
        alias="dam_Inflow",
        namespace=locals(),
    )
    dam_TotalRemoteDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="TotalRemoteDischarge",
        alias="dam_TotalRemoteDischarge",
        namespace=locals(),
    )
    dam_NaturalRemoteDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="NaturalRemoteDischarge",
        alias="dam_NaturalRemoteDischarge",
        namespace=locals(),
    )
    dam_RemoteDemand = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RemoteDemand",
        alias="dam_RemoteDemand",
        namespace=locals(),
    )
    dam_RemoteFailure = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RemoteFailure",
        alias="dam_RemoteFailure",
        namespace=locals(),
    )
    dam_RequiredRemoteRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RequiredRemoteRelease",
        alias="dam_RequiredRemoteRelease",
        namespace=locals(),
    )
    dam_AllowedRemoteRelieve = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="AllowedRemoteRelieve",
        alias="dam_AllowedRemoteRelieve",
        namespace=locals(),
    )
    dam_RequiredRemoteSupply = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RequiredRemoteSupply",
        alias="dam_RequiredRemoteSupply",
        namespace=locals(),
    )
    dam_PossibleRemoteRelieve = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="PossibleRemoteRelieve",
        alias="dam_PossibleRemoteRelieve",
        namespace=locals(),
    )
    dam_ActualRemoteRelieve = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualRemoteRelieve",
        alias="dam_ActualRemoteRelieve",
        namespace=locals(),
    )
    dam_RequiredRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RequiredRelease",
        alias="dam_RequiredRelease",
        namespace=locals(),
    )
    dam_TargetedRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="TargetedRelease",
        alias="dam_TargetedRelease",
        namespace=locals(),
    )
    dam_ActualRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualRelease",
        alias="dam_ActualRelease",
        namespace=locals(),
    )
    dam_MissingRemoteRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="MissingRemoteRelease",
        alias="dam_MissingRemoteRelease",
        namespace=locals(),
    )
    dam_ActualRemoteRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualRemoteRelease",
        alias="dam_ActualRemoteRelease",
        namespace=locals(),
    )
    dam_FloodDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="FloodDischarge",
        alias="dam_FloodDischarge",
        namespace=locals(),
    )
    dam_Outflow = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="Outflow",
        alias="dam_Outflow",
        namespace=locals(),
    )
    dam_WaterVolume = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_states",
        classname="WaterVolume",
        alias="dam_WaterVolume",
        namespace=locals(),
    )
    dummy_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dummy.dummy_fluxes",
        classname="Q",
        alias="dummy_Q",
        namespace=locals(),
    )
    evap_AdjustedWindSpeed = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="AdjustedWindSpeed",
        alias="evap_AdjustedWindSpeed",
        namespace=locals(),
    )
    evap_SaturationVapourPressure = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="SaturationVapourPressure",
        alias="evap_SaturationVapourPressure",
        namespace=locals(),
    )
    evap_SaturationVapourPressureSlope = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="SaturationVapourPressureSlope",
        alias="evap_SaturationVapourPressureSlope",
        namespace=locals(),
    )
    evap_ActualVapourPressure = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="ActualVapourPressure",
        alias="evap_ActualVapourPressure",
        namespace=locals(),
    )
    evap_EarthSunDistance = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="EarthSunDistance",
        alias="evap_EarthSunDistance",
        namespace=locals(),
    )
    evap_SolarDeclination = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="SolarDeclination",
        alias="evap_SolarDeclination",
        namespace=locals(),
    )
    evap_SunsetHourAngle = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="SunsetHourAngle",
        alias="evap_SunsetHourAngle",
        namespace=locals(),
    )
    evap_SolarTimeAngle = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="SolarTimeAngle",
        alias="evap_SolarTimeAngle",
        namespace=locals(),
    )
    evap_ExtraterrestrialRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="ExtraterrestrialRadiation",
        alias="evap_ExtraterrestrialRadiation",
        namespace=locals(),
    )
    evap_PossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="PossibleSunshineDuration",
        alias="evap_PossibleSunshineDuration",
        namespace=locals(),
    )
    evap_ClearSkySolarRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="ClearSkySolarRadiation",
        alias="evap_ClearSkySolarRadiation",
        namespace=locals(),
    )
    evap_GlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="GlobalRadiation",
        alias="evap_GlobalRadiation",
        namespace=locals(),
    )
    evap_NetShortwaveRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="NetShortwaveRadiation",
        alias="evap_NetShortwaveRadiation",
        namespace=locals(),
    )
    evap_NetLongwaveRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="NetLongwaveRadiation",
        alias="evap_NetLongwaveRadiation",
        namespace=locals(),
    )
    evap_NetRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="NetRadiation",
        alias="evap_NetRadiation",
        namespace=locals(),
    )
    evap_SoilHeatFlux = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="SoilHeatFlux",
        alias="evap_SoilHeatFlux",
        namespace=locals(),
    )
    evap_PsychrometricConstant = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="PsychrometricConstant",
        alias="evap_PsychrometricConstant",
        namespace=locals(),
    )
    evap_ReferenceEvapotranspiration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="ReferenceEvapotranspiration",
        alias="evap_ReferenceEvapotranspiration",
        namespace=locals(),
    )
    hbranch_Input = LazyInOutSequenceImport(
        modulename="hydpy.models.hbranch.hbranch_fluxes",
        classname="Input",
        alias="hbranch_Input",
        namespace=locals(),
    )
    hland_TMean = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="TMean",
        alias="hland_TMean",
        namespace=locals(),
    )
    hland_ContriArea = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="ContriArea",
        alias="hland_ContriArea",
        namespace=locals(),
    )
    hland_InUZ = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="InUZ",
        alias="hland_InUZ",
        namespace=locals(),
    )
    hland_Perc = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="Perc",
        alias="hland_Perc",
        namespace=locals(),
    )
    hland_Q0 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="Q0",
        alias="hland_Q0",
        namespace=locals(),
    )
    hland_Q1 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="Q1",
        alias="hland_Q1",
        namespace=locals(),
    )
    hland_InUH = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="InUH",
        alias="hland_InUH",
        namespace=locals(),
    )
    hland_OutUH = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="OutUH",
        alias="hland_OutUH",
        namespace=locals(),
    )
    hland_QT = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="QT",
        alias="hland_QT",
        namespace=locals(),
    )
    hland_UZ = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_states",
        classname="UZ",
        alias="hland_UZ",
        namespace=locals(),
    )
    hland_LZ = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_states",
        classname="LZ",
        alias="hland_LZ",
        namespace=locals(),
    )
    llake_QZ = LazyInOutSequenceImport(
        modulename="hydpy.models.llake.llake_fluxes",
        classname="QZ",
        alias="llake_QZ",
        namespace=locals(),
    )
    llake_QA = LazyInOutSequenceImport(
        modulename="hydpy.models.llake.llake_fluxes",
        classname="QA",
        alias="llake_QA",
        namespace=locals(),
    )
    llake_V = LazyInOutSequenceImport(
        modulename="hydpy.models.llake.llake_states",
        classname="V",
        alias="llake_V",
        namespace=locals(),
    )
    llake_W = LazyInOutSequenceImport(
        modulename="hydpy.models.llake.llake_states",
        classname="W",
        alias="llake_W",
        namespace=locals(),
    )
    lland_QZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QZ",
        alias="lland_QZ",
        namespace=locals(),
    )
    lland_QZH = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QZH",
        alias="lland_QZH",
        namespace=locals(),
    )
    lland_TemLTag = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="TemLTag",
        alias="lland_TemLTag",
        namespace=locals(),
    )
    lland_DailyRelativeHumidity = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailyRelativeHumidity",
        alias="lland_DailyRelativeHumidity",
        namespace=locals(),
    )
    lland_DailySunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailySunshineDuration",
        alias="lland_DailySunshineDuration",
        namespace=locals(),
    )
    lland_WindSpeed2m = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="WindSpeed2m",
        alias="lland_WindSpeed2m",
        namespace=locals(),
    )
    lland_DailyWindSpeed2m = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailyWindSpeed2m",
        alias="lland_DailyWindSpeed2m",
        namespace=locals(),
    )
    lland_WindSpeed10m = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="WindSpeed10m",
        alias="lland_WindSpeed10m",
        namespace=locals(),
    )
    lland_SolarDeclination = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="SolarDeclination",
        alias="lland_SolarDeclination",
        namespace=locals(),
    )
    lland_TSA = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="TSA",
        alias="lland_TSA",
        namespace=locals(),
    )
    lland_TSU = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="TSU",
        alias="lland_TSU",
        namespace=locals(),
    )
    lland_EarthSunDistance = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="EarthSunDistance",
        alias="lland_EarthSunDistance",
        namespace=locals(),
    )
    lland_ExtraterrestrialRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="ExtraterrestrialRadiation",
        alias="lland_ExtraterrestrialRadiation",
        namespace=locals(),
    )
    lland_PossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="PossibleSunshineDuration",
        alias="lland_PossibleSunshineDuration",
        namespace=locals(),
    )
    lland_DailyPossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailyPossibleSunshineDuration",
        alias="lland_DailyPossibleSunshineDuration",
        namespace=locals(),
    )
    lland_DailyGlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailyGlobalRadiation",
        alias="lland_DailyGlobalRadiation",
        namespace=locals(),
    )
    lland_SP = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="SP",
        alias="lland_SP",
        namespace=locals(),
    )
    lland_GlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="GlobalRadiation",
        alias="lland_GlobalRadiation",
        namespace=locals(),
    )
    lland_AdjustedGlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="AdjustedGlobalRadiation",
        alias="lland_AdjustedGlobalRadiation",
        namespace=locals(),
    )
    lland_QDGZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QDGZ",
        alias="lland_QDGZ",
        namespace=locals(),
    )
    lland_QAH = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QAH",
        alias="lland_QAH",
        namespace=locals(),
    )
    lland_QA = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QA",
        alias="lland_QA",
        namespace=locals(),
    )
    lland_QDGZ1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QDGZ1",
        alias="lland_QDGZ1",
        namespace=locals(),
    )
    lland_QDGZ2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QDGZ2",
        alias="lland_QDGZ2",
        namespace=locals(),
    )
    lland_QIGZ1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QIGZ1",
        alias="lland_QIGZ1",
        namespace=locals(),
    )
    lland_QIGZ2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QIGZ2",
        alias="lland_QIGZ2",
        namespace=locals(),
    )
    lland_QBGZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QBGZ",
        alias="lland_QBGZ",
        namespace=locals(),
    )
    lland_QDGA1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QDGA1",
        alias="lland_QDGA1",
        namespace=locals(),
    )
    lland_QDGA2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QDGA2",
        alias="lland_QDGA2",
        namespace=locals(),
    )
    lland_QIGA1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QIGA1",
        alias="lland_QIGA1",
        namespace=locals(),
    )
    lland_QIGA2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QIGA2",
        alias="lland_QIGA2",
        namespace=locals(),
    )
    lland_QBGA = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="QBGA",
        alias="lland_QBGA",
        namespace=locals(),
    )
    lstream_QZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lstream.lstream_fluxes",
        classname="QZ",
        alias="lstream_QZ",
        namespace=locals(),
    )
    lstream_QZA = LazyInOutSequenceImport(
        modulename="hydpy.models.lstream.lstream_fluxes",
        classname="QZA",
        alias="lstream_QZA",
        namespace=locals(),
    )
    lstream_QA = LazyInOutSequenceImport(
        modulename="hydpy.models.lstream.lstream_fluxes",
        classname="QA",
        alias="lstream_QA",
        namespace=locals(),
    )
    test_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.test.test_fluxes",
        classname="Q",
        alias="test_Q",
        namespace=locals(),
    )
    test_S = LazyInOutSequenceImport(
        modulename="hydpy.models.test.test_states",
        classname="S",
        alias="test_S",
        namespace=locals(),
    )
    wland_PC = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PC",
        alias="wland_PC",
        namespace=locals(),
    )
    wland_PES = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PES",
        alias="wland_PES",
        namespace=locals(),
    )
    wland_PS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PS",
        alias="wland_PS",
        namespace=locals(),
    )
    wland_PV = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PV",
        alias="wland_PV",
        namespace=locals(),
    )
    wland_PQ = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PQ",
        alias="wland_PQ",
        namespace=locals(),
    )
    wland_ETV = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ETV",
        alias="wland_ETV",
        namespace=locals(),
    )
    wland_ES = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ES",
        alias="wland_ES",
        namespace=locals(),
    )
    wland_ET = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ET",
        alias="wland_ET",
        namespace=locals(),
    )
    wland_FXS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FXS",
        alias="wland_FXS",
        namespace=locals(),
    )
    wland_FXG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FXG",
        alias="wland_FXG",
        namespace=locals(),
    )
    wland_CDG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="CDG",
        alias="wland_CDG",
        namespace=locals(),
    )
    wland_FGS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FGS",
        alias="wland_FGS",
        namespace=locals(),
    )
    wland_FQS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FQS",
        alias="wland_FQS",
        namespace=locals(),
    )
    wland_RH = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="RH",
        alias="wland_RH",
        namespace=locals(),
    )
    wland_R = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="R",
        alias="wland_R",
        namespace=locals(),
    )
    wland_DV = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="DV",
        alias="wland_DV",
        namespace=locals(),
    )
    wland_DG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="DG",
        alias="wland_DG",
        namespace=locals(),
    )
    wland_HQ = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="HQ",
        alias="wland_HQ",
        namespace=locals(),
    )
    wland_HS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="HS",
        alias="wland_HS",
        namespace=locals(),
    )
