READ_DATA = 0x0
WRITE_DATA = 0x1
INVALID_DATA = 0x2
RESERVED = 0x3
READ_ACK = 0x4
WRITE_ACK = 0x5
DATA_INVALID = 0x6
UNKNOWN_DATAID = 0x7

msg_type = {
    READ_DATA: "READ_DAT",
    WRITE_DATA: "WRITE_DAT",
    INVALID_DATA: "INVALID_DATA",
    RESERVED: "RESERVED",
    READ_ACK: "READ_ACK",
    WRITE_ACK: "WRITE_ACK",
    DATA_INVALID: "DATA_INVALID",
    UNKNOWN_DATAID: "UNKNOWN_DATAID"
}

def formatFloat(bh, bl):
    return "{:2.2f}".format(float((int(bh, 16) << 8) + int(bl, 16)) / 256)

def formatBinary(bh, bl):
    # return ""
    return "0x{:0^8b} 0x{:0^8b}".format(int(bh, 16), int(bl, 16))

def formatBinaryBitfield(bh, bl):
    return [1 if digit=='1' else 0 for digit in "{0:08b}{1:08b}".format(int(bh, 16), int(bl, 16))]


def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

data_id = {
    0: ("Status", "Master and Slave Status flags. "),
    1: ("TSet", "Control setpoint ie CH water temperature setpoint (C) ", formatFloat, "ControlSetpoint"),
    2: ("M-Config / M-MemberIDcode", "Master Configuration Flags / Master MemberID Code ", formatBinary, "MConfig"),
    3: ("S-Config / S-MemberIDcode", "Slave Configuration Flags / Slave MemberID Code ", formatBinary, "SConfig"),
    4: ("Command", "Remote Command"),
    5: ("ASF-flags / OEM-fault-code", "Application-specific fault flags and OEM fault code ", formatBinary, "AsfFlags"),
    6: ("RBP-flags", "Remote boiler parameter transfer-enable & read/write flags "),
    7: ("Cooling-control", "Cooling control signal (%) "),
    8: ("TsetCH2", "Control setpoint for 2e CH circuit (C) ", formatFloat, "TsetCH2"),
    9: ("TrOverride", "Remote override room setpoint ", formatFloat, "ConstantRoomSetpointOverride"),
    10: ("TSP", "Number of Transparent-Slave-Parameters supported by slave "),
    11: ("TSP-index / TSP-value", "Index number / Value of referred-to transparent slave parameter. "),
    12: ("FHB-size", "Size of Fault-History-Buffer supported by slave "),
    13: ("FHB-index / FHB-value", "Index number / Value of referred-to fault-history buffer entry. "),
    14: ("Max-rel-mod-level-setting", "Maximum relative modulation level setting (%) ", formatFloat, "Max-rel-mod-level-setting"),
    15: ("Max-Capacity / Min-Mod-Level", "Maximum boiler capacity (kW) / Minimum boiler modulation level(%) ", formatFloat,"Max-Capacity"),
    16: ("TrSet", "Room Setpoint (C) ", formatFloat, "RoomSetpoint"),
    17: ("Rel.-mod-level", "Relative Modulation Level (%) ", formatFloat, "RelativeModulationLevel"),
    18: ("CH-pressure", "Water pressure in CH circuit (bar) ", formatFloat, "CentralHeatingWaterPressure"),
    19: ("DHW-flow-rate", "Water flow rate in DHW circuit. (litres/minute) "),
    20: ("Day-Time", "Day of Week and Time of Day "),
    21: ("Date", "Calendar date "),
    22: ("Year", "Calendar year "),
    23: ("TrSetCH2", "Room Setpoint for 2nd CH circuit (C) ", formatFloat, "TrSetCH2"),
    24: ("Tr", "Room temperature (C) ", formatFloat, "RoomTemperature"),
    25: ("Tboiler", "Boiler flow water temperature (C) ", formatFloat, "BoilerWaterTemperature"),
    26: ("Tdhw", "DHW temperature (C) ", formatFloat, "HotWaterTemperature"),
    27: ("Toutside", "Outside temperature (C) ", formatFloat, "OutsideTemperature"),
    28: ("Tret", "Return water temperature (C) ", formatFloat, "ReturnWaterTemperature"),
    29: ("Tstorage", "Solar storage temperature (C) ", formatFloat, "Tstorage"),
    30: ("Tcollector", "Solar collector temperature (C) ", formatFloat, "Tcollector"),
    31: ("TflowCH2", "Flow water temperature CH2 circuit (C) ", formatFloat, "TflowCH2"),
    32: ("Tdhw2", "Domestic hot water temperature 2 (C) ", formatFloat, "Tdhw2"),
    33: ("Texhaust", "Boiler exhaust temperature (C) ", formatFloat, "Texhaust"),
    48: ("TdhwSet-UB / TdhwSet-LB", "DHW setpoint upper & lower bounds for adjustment (C) "),
    49: ("MaxTSet-UB / MaxTSet-LB", "Max CH water setpoint upper & lower bounds for adjustment (C) "),
    50: ("Hcratio-UB / Hcratio-LB", "OTC heat curve ratio upper & lower bounds for adjustment "),
    56: ("TdhwSet", "DHW setpoint (C) (Remote parameter 1) "),
    57: ("MaxTSet", "Max CH water setpoint (C) (Remote parameters 2) ", formatFloat, "MaxCHWaterSetpoint"),
    58: ("Hcratio", "OTC heat curve ratio (C) (Remote parameter 3) "),
    100: ("Remote override function", "Function of manual and program changes in master and remote room setpoint. "),
    115: ("OEM diagnostic code", "OEM-specific diagnostic/service code "),
    116: ("Burner starts", "Number of starts burner "),
    117: ("CH pump starts", "Number of starts CH pump "),
    118: ("DHW pump/valve starts", "Number of starts DHW pump/valve "),
    119: ("DHW burner starts", "Number of starts burner during DHW mode "),
    120: ("Burner operation hours", "Number of hours that burner is in operation (i.e. flame on) "),
    121: ("CH pump operation hours", "Number of hours that CH pump has been running "),
    122: ("DHW pump/valve operation hours", "Number of hours that DHW pump has been running or DHW valve has been opened "),
    123: ("DHW burner operation hours", "Number of hours that burner is in operation during DHW mode "),
    124: ("OpenTherm version Master", "The implemented version of the OpenTherm Protocol Specification in the master. "),
    125: ("OpenTherm version Slave", "The implemented version of the OpenTherm Protocol Specification in the slave. "),
    126: ("Master-version", "Master product version number and type "),
    127: ("Slave-version", "Slave product version number and type "),
    128: ("SmartPower", "Smart power level change."),
    140: ("Flags140", "Flasgs140", formatBinaryBitfield, "Flags140"),
    141: ("Flags141", "Flasgs141", formatBinaryBitfield, "Flags141"),
    150: ("Flags150", "Flasgs150", formatBinaryBitfield, "Flags150"),
    155: ("Flags155", "Flasgs155", formatBinaryBitfield, "Flags155"),
    156: ("Flags156", "Flasgs156", formatBinaryBitfield, "Flags156"),
    157: ("Flags157", "Flasgs157", formatBinaryBitfield, "Flags157"),
    170: ("Flags170", "Flasgs170", formatBinaryBitfield, "Flags170"),
    171: ("Flags171", "Flasgs171", formatBinaryBitfield, "Flags171"),
    172: ("Flags172", "Flasgs172", formatBinaryBitfield, "Flags172")
 }