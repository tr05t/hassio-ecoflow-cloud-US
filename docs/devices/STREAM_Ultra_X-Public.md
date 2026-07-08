## STREAM_Ultra_X

*Sensors*
- Solar Power (`powGetPvSum`)
- Grid Power (`gridConnectionPower`)
- Load Power (`powGetSysLoad`)
- Battery Power (`powGetBpCms`)
- Battery Level (`cmsBattSoc`)
- Backup Reserve Level (`backupReverseSoc`)
- Charge Limit (`cmsMaxChgSoc`)
- Discharge Limit (`cmsMinDsgSoc`)
- Feed-in Mode (`feedGridMode`)   _(disabled)_
- Operating Mode: Self-powered (`energyStrategyOperateMode.operateSelfPoweredOpen`)   _(disabled)_
- Operating Mode: AI Mode (`energyStrategyOperateMode.operateIntelligentScheduleModeOpen`)   _(disabled)_
- Solar 1 Watts (`20_1.pv1InputWatts`)
- Solar 1 Input Voltage (`20_1.pv1InputVolt`)
- Solar 1 Current (`20_1.pv1InputCur`)
- Solar 1 Temperature (`20_1.pv1Temp`)
- Solar 1 Status (`20_1.pv1Statue`)   _(disabled)_
- Solar 1 Error Code (`20_1.pv1ErrCode`)   _(disabled)_
- Solar 2 Watts (`20_1.pv2InputWatts`)
- Solar 2 Input Voltage (`20_1.pv2InputVolt`)
- Solar 2 Current (`20_1.pv2InputCur`)
- Solar 2 Temperature (`20_1.pv2Temp`)
- Solar 2 Status (`20_1.pv2Statue`)   _(disabled)_
- Solar 2 Error Code (`20_1.pv2ErrCode`)   _(disabled)_
- Battery Voltage (`20_1.batInputVolt`)
- Battery Current (`20_1.batInputCur`)
- Battery Temperature (`20_1.batTemp`)
- Battery Charge (WN511) (`20_1.batSoc`)
- Battery Status (`20_1.batStatue`)   _(disabled)_
- Battery Error Code (`20_1.batErrCode`)   _(disabled)_
- LLC Input Voltage (`20_1.llcInputVolt`)   _(disabled)_
- LLC Temperature (`20_1.llcTemp`)
- LLC Status (`20_1.llcStatue`)   _(disabled)_
- LLC Error Code (`20_1.llcErrCode`)   _(disabled)_
- Inverter On/Off Status (`20_1.invOnOff`)
- Inverter Output Watts (`20_1.invOutputWatts`)
- Inverter Frequency (`20_1.invFreq`)
- Inverter Temperature (`20_1.invTemp`)
- Inverter Status (`20_1.invStatue`)   _(disabled)_
- Inverter Error Code (`20_1.invErrCode`)   _(disabled)_
- Charge Remaining Time (`20_1.chgRemainTime`)
- Discharge Remaining Time (`20_1.dsgRemainTime`)
- Discharge Limit (WN511) (`20_1.lowerLimit`)   _(disabled)_
- Charge Limit (WN511) (`20_1.upperLimit`)   _(disabled)_
- Rated Power (`20_1.ratedPower`)   _(disabled)_
- LED Brightness (`20_1.invBrightness`)   _(disabled)_
- Status

*Switches*
- AC 1 (`relay2Onoff` -> `{"sn": "SN", "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": true, "params": {"cfgRelay2Onoff": "VALUE"}}`)
- AC 2 (`relay3Onoff` -> `{"sn": "SN", "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": true, "params": {"cfgRelay3Onoff": "VALUE"}}`)

*Sliders (numbers)*
- Backup Reserve Level (`backupReverseSoc` -> `{"sn": "SN", "cmdId": 17, "cmdFunc": 254, "dirDest": 1, "dirSrc": 1, "dest": 2, "needAck": true, "params": {"cfgBackupReverseSoc": "VALUE"}}` [3 - 95])
- Min Discharge Level (`20_1.lowerLimit` -> `{"sn": "SN", "cmdCode": "WN511_SET_BAT_LOWER_PACK", "params": {"lowerLimit": "VALUE"}}` [1 - 30])
- Max Charge Level (`20_1.upperLimit` -> `{"sn": "SN", "cmdCode": "WN511_SET_BAT_UPPER_PACK", "params": {"upperLimit": "VALUE"}}` [70 - 100])
- Brightness (`20_1.invBrightness` -> `{"sn": "SN", "cmdCode": "WN511_SET_BRIGHTNESS_PACK", "params": {"brightness": "VALUE"}}` [0 - 1023])
- Custom Load Power (`20_1.permanentWatts` -> `{"sn": "SN", "cmdCode": "WN511_SET_PERMANENT_WATTS_PACK", "params": {"permanentWatts": "VALUE"}}` [0 - 600])

*Selects*
- Power Supply Priority (`20_1.supplyPriority` -> `{"sn": "SN", "cmdCode": "WN511_SET_SUPPLY_PRIORITY_PACK", "params": {"supplyPriority": "VALUE"}}` [Supply Priority Power (0), Supply Priority Battery (1)])

