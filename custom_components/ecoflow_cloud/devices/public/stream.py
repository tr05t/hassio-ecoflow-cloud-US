"""Public API device implementations for EcoFlow STREAM family."""

from .data_bridge import to_plain
from .. import BaseDevice, const
from ...api import EcoflowApiClient
from ...entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, BaseSelectEntity
from ...number import MinBatteryLevelEntity, MaxBatteryLevelEntity, BrightnessLevelEntity, DeciChargingPowerEntity
from ...select import PowerDictSelectEntity
from ...sensor import (
    StatusSensorEntity,
    InWattsSolarSensorEntity,
    DecivoltSensorEntity,
    DeciampSensorEntity,
    DecicelsiusSensorEntity,
    MiscSensorEntity,
    LevelSensorEntity,
    DeciwattsSensorEntity,
    RemainSensorEntity,
    DecihertzSensorEntity,
    WattsSensorEntity,
)
from ...switch import EnabledEntity

# Options for STREAM operating mode (mutually exclusive pair)
STREAM_OPERATING_MODE_OPTIONS = {
    "Self-powered": 0,
    "AI Mode": 1,
}

# Options for STREAM feed-in control (1 = off, 2 = on per manufacturer docs)
STREAM_FEED_IN_OPTIONS = {
    "Off": 1,
    "On": 2,
}


class WattFloatSensorEntity(WattsSensorEntity):
    """Sensor for STREAM aggregate quota power fields reported as float watts."""

    def _update_value(self, val) -> bool:
        return super()._update_value(round(float(val), 1))


class StreamBaseDevice(BaseDevice):
    """Common telemetry and controls shared by all STREAM models.

    Aggregate STREAM quota fields (flat dict on the /quota topic):
        powGetPvSum       — system PV power (W, float)
        gridConnectionPower — grid port active power, positive=import, negative=export (W, float)
        powGetSysLoad     — system load power (W, float)
        powGetBpCms       — aggregated battery power, positive=charging, negative=discharging (W, float)
        cmsBattSoc        — battery state-of-charge (%, float)
        backupReverseSoc  — backup reserve level (int, %)
        cmsMaxChgSoc      — charge limit (int, %)
        cmsMinDsgSoc      — discharge limit (int, %)
        feedGridMode      — feed-in control (int, 1=off, 2=on)
        energyStrategyOperateMode.operateSelfPoweredOpen      — bool
        energyStrategyOperateMode.operateIntelligentScheduleModeOpen — bool

    WN511-style heartbeat fields (prefix 20_1.*) for compatible models:
        20_1.lowerLimit   — discharge limit
        20_1.upperLimit   — charge limit
        20_1.invBrightness — LED brightness
        20_1.permanentWatts — custom load power (0.1 W unit)
        20_1.supplyPriority — power supply priority
        (plus voltage/current/temperature diagnostics from PowerStream docs)
    """

    def sensors(self, client: EcoflowApiClient) -> list[BaseSensorEntity]:
        return [
            # --- Aggregate STREAM quota sensors ---
            WattFloatSensorEntity(client, self, "powGetPvSum", "Solar Power"),
            WattFloatSensorEntity(client, self, "gridConnectionPower", "Grid Power"),
            WattFloatSensorEntity(client, self, "powGetSysLoad", "Load Power"),
            WattFloatSensorEntity(client, self, "powGetBpCms", "Battery Power"),
            LevelSensorEntity(client, self, "cmsBattSoc", "Battery Level"),
            MiscSensorEntity(client, self, "backupReverseSoc", "Backup Reserve Level"),
            MiscSensorEntity(client, self, "cmsMaxChgSoc", "Charge Limit"),
            MiscSensorEntity(client, self, "cmsMinDsgSoc", "Discharge Limit"),
            MiscSensorEntity(client, self, "feedGridMode", "Feed-in Mode", False),
            MiscSensorEntity(
                client, self,
                "energyStrategyOperateMode.operateSelfPoweredOpen",
                "Operating Mode: Self-powered", False
            ),
            MiscSensorEntity(
                client, self,
                "energyStrategyOperateMode.operateIntelligentScheduleModeOpen",
                "Operating Mode: AI Mode", False
            ),

            # --- WN511-style micro-inverter sensors (present on STREAM-compatible nodes) ---
            InWattsSolarSensorEntity(client, self, "20_1.pv1InputWatts", "Solar 1 Watts"),
            DecivoltSensorEntity(client, self, "20_1.pv1InputVolt", "Solar 1 Input Voltage"),
            DeciampSensorEntity(client, self, "20_1.pv1InputCur", "Solar 1 Current"),
            DecicelsiusSensorEntity(client, self, "20_1.pv1Temp", "Solar 1 Temperature"),
            MiscSensorEntity(client, self, "20_1.pv1Statue", "Solar 1 Status", False),
            MiscSensorEntity(client, self, "20_1.pv1ErrCode", "Solar 1 Error Code", False),

            InWattsSolarSensorEntity(client, self, "20_1.pv2InputWatts", "Solar 2 Watts"),
            DecivoltSensorEntity(client, self, "20_1.pv2InputVolt", "Solar 2 Input Voltage"),
            DeciampSensorEntity(client, self, "20_1.pv2InputCur", "Solar 2 Current"),
            DecicelsiusSensorEntity(client, self, "20_1.pv2Temp", "Solar 2 Temperature"),
            MiscSensorEntity(client, self, "20_1.pv2Statue", "Solar 2 Status", False),
            MiscSensorEntity(client, self, "20_1.pv2ErrCode", "Solar 2 Error Code", False),

            DecivoltSensorEntity(client, self, "20_1.batInputVolt", "Battery Voltage"),
            DeciampSensorEntity(client, self, "20_1.batInputCur", "Battery Current"),
            DecicelsiusSensorEntity(client, self, "20_1.batTemp", "Battery Temperature"),
            LevelSensorEntity(client, self, "20_1.batSoc", "Battery Charge (WN511)"),
            MiscSensorEntity(client, self, "20_1.batStatue", "Battery Status", False),
            MiscSensorEntity(client, self, "20_1.batErrCode", "Battery Error Code", False),

            DecivoltSensorEntity(client, self, "20_1.llcInputVolt", "LLC Input Voltage", False),
            DecicelsiusSensorEntity(client, self, "20_1.llcTemp", "LLC Temperature"),
            MiscSensorEntity(client, self, "20_1.llcStatue", "LLC Status", False),
            MiscSensorEntity(client, self, "20_1.llcErrCode", "LLC Error Code", False),

            MiscSensorEntity(client, self, "20_1.invOnOff", "Inverter On/Off Status"),
            DeciwattsSensorEntity(client, self, "20_1.invOutputWatts", "Inverter Output Watts"),
            DecihertzSensorEntity(client, self, "20_1.invFreq", "Inverter Frequency"),
            DecicelsiusSensorEntity(client, self, "20_1.invTemp", "Inverter Temperature"),
            MiscSensorEntity(client, self, "20_1.invStatue", "Inverter Status", False),
            MiscSensorEntity(client, self, "20_1.invErrCode", "Inverter Error Code", False),

            RemainSensorEntity(client, self, "20_1.chgRemainTime", "Charge Remaining Time"),
            RemainSensorEntity(client, self, "20_1.dsgRemainTime", "Discharge Remaining Time"),

            MiscSensorEntity(client, self, "20_1.lowerLimit", "Discharge Limit (WN511)", False),
            MiscSensorEntity(client, self, "20_1.upperLimit", "Charge Limit (WN511)", False),
            MiscSensorEntity(client, self, "20_1.ratedPower", "Rated Power", False),
            MiscSensorEntity(client, self, "20_1.invBrightness", "LED Brightness", False),

            StatusSensorEntity(client, self),
        ]

    def numbers(self, client: EcoflowApiClient) -> list[BaseNumberEntity]:
        return [
            # Backup reserve (system-level STREAM command)
            MinBatteryLevelEntity(
                client, self, "backupReverseSoc", "Backup Reserve Level", 3, 95,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "cmdFunc": 254,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "dest": 2,
                    "needAck": True,
                    "params": {"cfgBackupReverseSoc": value},
                },
            ),
            # WN511-style discharge limit
            MinBatteryLevelEntity(
                client, self, "20_1.lowerLimit", "Min Discharge Level", 1, 30,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "WN511_SET_BAT_LOWER_PACK",
                    "params": {"lowerLimit": value},
                },
            ),
            # WN511-style charge limit
            MaxBatteryLevelEntity(
                client, self, "20_1.upperLimit", "Max Charge Level", 70, 100,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "WN511_SET_BAT_UPPER_PACK",
                    "params": {"upperLimit": value},
                },
            ),
            # LED brightness
            BrightnessLevelEntity(
                client, self, "20_1.invBrightness", const.BRIGHTNESS, 0, 1023,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "WN511_SET_BRIGHTNESS_PACK",
                    "params": {"brightness": value},
                },
            ),
            # Custom load power (0.1 W unit, WN511 style)
            DeciChargingPowerEntity(
                client, self, "20_1.permanentWatts", "Custom Load Power", 0, 600,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "WN511_SET_PERMANENT_WATTS_PACK",
                    "params": {"permanentWatts": value},
                },
            ),
        ]

    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return [
            # WN511-style power supply priority
            PowerDictSelectEntity(
                client, self, "20_1.supplyPriority", "Power Supply Priority",
                const.POWER_SUPPLY_PRIORITY_OPTIONS,
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdCode": "WN511_SET_SUPPLY_PRIORITY_PACK",
                    "params": {"supplyPriority": value},
                },
            ),
        ]

    def _prepare_data(self, raw_data) -> dict[str, any]:
        res = super()._prepare_data(raw_data)
        res = to_plain(res)
        return res


class StreamDualAc(StreamBaseDevice):
    """STREAM Ultra, STREAM Pro, STREAM AC Pro, STREAM Ultra X, STREAM Ultra (US).

    These models expose two independent AC relay switches (AC1 = relay2, AC2 = relay3)
    plus all shared STREAM telemetry and controls.

    The AC switch commands target the individual device SN, not the main system SN,
    as documented by the manufacturer for multi-device BKW systems.
    """

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return [
            EnabledEntity(
                client, self, "relay2Onoff", "AC 1",
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "cmdFunc": 254,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "dest": 2,
                    "needAck": True,
                    "params": {"cfgRelay2Onoff": bool(value)},
                },
            ),
            EnabledEntity(
                client, self, "relay3Onoff", "AC 2",
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "cmdFunc": 254,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "dest": 2,
                    "needAck": True,
                    "params": {"cfgRelay3Onoff": bool(value)},
                },
            ),
        ]


class StreamMax(StreamBaseDevice):
    """STREAM Max.

    This model has a single AC relay switch (AC = relay2).
    It does NOT support a second AC switch (relay3).
    """

    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return [
            EnabledEntity(
                client, self, "relay2Onoff", "AC",
                lambda value: {
                    "sn": self.device_info.sn,
                    "cmdId": 17,
                    "cmdFunc": 254,
                    "dirDest": 1,
                    "dirSrc": 1,
                    "dest": 2,
                    "needAck": True,
                    "params": {"cfgRelay2Onoff": bool(value)},
                },
            ),
        ]
