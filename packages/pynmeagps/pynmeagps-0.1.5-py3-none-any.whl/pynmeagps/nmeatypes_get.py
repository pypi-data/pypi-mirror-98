"""
NMEA Protocol Output payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _GET_ MESSAGES _FROM_ THE RECEIVER
(i.e. Periodic Navigation Data, Poll Responses, Info messages)

NB: Attribute names must be unique within each message id

NB: Repeating groups must be defined as a tuple thus
    'group': ('numr', {dict})
    where
    - 'numr' is either:
       a) an integer representing a fixed number of repeats e.g 32
       b) a string representing the name of a preceding attribute
          containing the number of repeats e.g. 'numCh'
       c) 'None' for an indeterminate repeating group
          (only one such group is permitted per message type)
    - {dict} is the nested dictionary containing the repeating
      attributes

Created on 4 Mar Sep 2021

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import (
    CH,
    DE,
    DT,
    HX,
    IN,
    LA,
    LN,
    ST,
    TM,
)

NMEA_PAYLOADS_GET = {
    # *********************************************
    # STANDARD MESSAGES
    # *********************************************
    "DTM": {
        "datum": ST,
        "subDatum": ST,
        "latOfset": DE,
        "NS": CH,
        "lonOfset": DE,
        "EW": CH,
        "alt": DE,
        "refDatum": ST,
    },
    "GBS": {
        "time": TM,
        "errLat": DE,
        "effLon": DE,
        "errAlt": DE,
        "svid": IN,
        "prob": DE,
        "bias": DE,
        "stddev": DE,
        "systemId": IN,  # NMEA >=4.10 only
        "signalId": IN,  # NMEA >=4.10 only
    },
    "GGA": {
        "time": TM,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "quality": IN,
        "numSV": IN,
        "HDOP": DE,
        "alt": DE,  # altitude above sea level in m
        "altUnit": CH,
        "sep": DE,
        "sepUnit": CH,
        "diffAge": IN,
        "diffStation": IN,
    },
    "GLL": {
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "time": TM,
        "status": ST,
        "posMode": ST,
    },
    "GNS": {
        "time": TM,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "posMode": ST,
        "numSV": IN,
        "HDOP": DE,
        "alt": DE,
        "sep": DE,
        "diffAge": DE,
        "diffStation": IN,
        "navStatus": CH,  # NMEA >=4.10 only
    },
    "GRS": {
        "time": TM,
        "mode": IN,
        "groupSV": (
            12,
            {  # repeating group * 12
                "residual": DE,
            },
        ),
        "systemId": IN,  # NMEA >=4.10 only
        "signalId": IN,  # NMEA >=4.10 only
    },
    "GSA": {
        "opMode": CH,
        "navMode": IN,
        "groupSV": (
            12,
            {  # repeating group * 12
                "svid": IN,
            },
        ),
        "PDOP": DE,
        "HDOP": DE,
        "VDOP": DE,
        "systemId": IN,  # NMEA >=4.10 only
    },
    "GST": {
        "time": TM,
        "rangeRms": DE,
        "stdMajor": DE,
        "stdMinor": DE,
        "orient": DE,
        "stdLat": DE,
        "stdLong": DE,
        "stdAlt": DE,
    },
    "GSV": {
        "numMsg": IN,
        "msgNum": IN,
        "numSV": IN,
        "group_sv": (
            "None",
            {  # repeating group * 1..4
                "svid": IN,
                "elv": DE,  # elevation
                "az": IN,  # azimuth
                "cno": IN,  # signal strength
            },
        ),
        "signalID": IN,  # NMEA >=4.10 only
    },
    "RLM": {
        "beacon": HX,
        "time": TM,
        "code": CH,
        "body": HX,
    },
    "RMC": {
        "time": TM,
        "status": CH,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "spd": DE,  # speed in knots
        "cog": DE,  # course over ground
        "date": DT,
        "mv": DE,
        "mvEW": ST,
        "posMode": CH,
        "navStatus": CH,  # NMEA >=4.10 only
    },
    "TXT": {
        "numMsg": IN,
        "msgNum": IN,
        "msgType": IN,
        "text": ST,
    },
    "VLW": {
        "twd": DE,
        "twdUnit": CH,
        "wd": DE,
        "wdUnit": CH,
        "tgd": DE,  # NMEA >=4.00 only
        "tgdUnit": CH,  # NMEA >=4.00 only
        "gd": DE,  # NMEA >=4.00 only
        "gdUnit": CH,  # NMEA >=4.00 only
    },
    "VTG": {
        "cogT": DE,  # course over ground (true)
        "cogtUnit": CH,
        "cogm": DE,  # course over ground (magnetic)
        "cogmUnit": CH,
        "sogn": DE,  # speed over ground knots
        "sognUnit": CH,
        "sogk": DE,  # speed over ground kmph
        "sogkUnit": CH,
        "posMode": CH,  # NMEA >=2.3 only
    },
    "ZDA": {
        "time": TM,
        "day": IN,
        "month": IN,
        "year": IN,
        "ltzh": ST,
        "ltzn": ST,
    },
    # *********************************************
    # GARMIN PROPRIETARY MESSAGES
    # *********************************************
    "PGRME": {  # estimated error information
        "HPE": DE,
        "VPE": DE,
        "EPE": DE,
    },
    "PGRMF": {  # GPS fix data sentence
        "week": IN,
        "secs": IN,
        "date": DT,
        "time": TM,
        "leapsec": IN,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "mode": CH,
        "fix": IN,
        "spd": DE,
        "course": IN,
        "PDOP": DE,
        "TDOP": DE,
    },
    "PGRMH": {  # aviation height and VNAV data
        "status": CH,
        "vspd": DE,
        "verr": DE,
        "spdtgt": DE,
        "spdwpt": DE,
        "height": DE,
        "trk": DE,
        "course": DE,
    },
    "PGRMM": {  # map datum
        "dtm": ST,
    },
    "PGRMT": {  # sensor status information
        "ver": ST,
        "ROMtest": CH,
        "rcvrtest": CH,
        "stortest": CH,
        "rtctest": CH,
        "osctest": CH,
        "datatest": CH,
        "temp": DE,
        "cfgdata": CH,
    },
    "PGRMV": {  # 3D velocity information
        "velE": DE,
        "velN": DE,
        "velZ": DE,
    },
    "PGRMZ": {  # altitude
        "alt": DE,
        "fix": IN,
    },
    "PGRMB": {  # DGPS Beacon information
        "freq": DE,
        "bps": IN,
        "snr": IN,
        "quality": IN,
        "dist": DE,
        "status": IN,
        "fixsrc": CH,
        "mode": CH,
    },
    # *********************************************
    # U-BLOX PROPRIETARY MESSAGES
    # *********************************************
    "PUBX00": {
        "msgId": IN,  # 00
        "time": TM,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "altRef": DE,
        "navStat": ST,
        "hAcc": DE,
        "vAcc": DE,
        "SOG": DE,
        "COG": DE,
        "vVel": DE,
        "diffAge": DE,
        "HDOP": DE,
        "VDOP": DE,
        "PDOP": DE,
        "numSVs": IN,
        "reserved": IN,
        "DR": IN,
    },
    "PUBX03": {
        "msgId": IN,  # 03
        "numSv": IN,
        "groupSV": (
            "numSv",
            {  # repeating group * numSv
                "svid": IN,
                "status": CH,
                "azi": DE,
                "ele": DE,
                "cno": IN,
                "lck": IN,
            },
        ),
    },
    "PUBX04": {
        "msgId": IN,  # 04
        "time": TM,
        "date": DT,
        "utcTow": ST,
        "utcWk": ST,
        "leapSec": ST,
        "clkBias": DE,
        "clkDrift": DE,
        "tpGran": IN,
    },
    "PUBX05": {  # deprecated, for backwards compat only
        "msgId": IN,  # 05
        "pulses": IN,
        "period": IN,
        "gyroMean": IN,
        "temperature": DE,
        "direction": CH,
        "pulseScaleCS": IN,
        "gyroScaleCS": IN,
        "gyroBiasCS": IN,
        "pulseScale": DE,
        "gyroBias": DE,
        "gyroScale": DE,
        "pulseScaleAcc": IN,
        "gyroBiasAcc": IN,
        "gyroScaleAcc": IN,
        "measUsed": HX,
    },
    # *********************************************
    # Dummy message for error testing
    # *********************************************
    "FOO": {"spam": "Z2", "eggs": "Y1"},
}
