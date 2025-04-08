import sys
import string
import random
import argparse

"""  
python 3.x must be installed to run this script.

scenarios generated from this script need to be used with TacView version '10583-TacViewC2_16_X-16.1.0', dated July 2023 or later, otherwise you will more than likely get an error saying the value is not supported. 
 
by default 100 tracks will be created with the lat long starting at 33.0,-117.0

to change the number of tracks, lat/long run the script from the command line with the following arguments: 
-n xxx -lat xx.x -long -xxx.x 
-h will show examples

(e.g.: py all_tracks_generator.py -n 100 -lat 33.3 -long -118.1) 
"""

track_field_template = """
<createtrack name='${name}' profile='${profile}'>
    <field name='${callsign_name}' value='${callsign}'/>
    <field name='Latitude' value='${lat}'/>
    <field name='Longitude' value='${lon}'/>
    <field name='${course_name}' value='${course}'/>
    <field name='${speed_name}' value='${speed}'/>
    <field name='${alt_type}' value='${alt}'/>
    <field name='${land_type_name}' value='${land_type}'/>
    <field name='${env_cat_name}' value='${env_cat}'/>
    <field name='${platform_name}' value='${platform}'/>
    <field name='${activity_name}' value='${activity}'/>
    <field name='${track3454ind}' value='${trackind}'/>
    <field name='${spec_type_name}' value='${spec_type}'/>
    <field name='${strength_name}' value='${strength_type}'/>
    <field name='SPI' value='${spi}'/>
    <field name='${identity_name}' value='${identity}'/>
    <field name='${time_function_name}' value='${time_function}'/>
    <field name='${hour_name}' value='${hour}'/>
    <field name='${minute_name}' value='${minute}'/>
    <field name='${seconds_name}' value='${second}'/>
    <field name='${boost_name}' value='${boost}'/>
    <field name='${lost_name}' value='${lost}'/>
    <field name='${mode_1_name}' value='${mode_1}'/>
    <field name='${mode_2_name}' value='${mode_2}'/>
    <field name='${mode_3_name}' value='${mode_3}'/>
    <field name='${mode_4_indicator_name}' value='${mode_4_indicator_type}'/>
    <field name='${mode_5_indicator_name}' value='${mode_5_indicator_type}'/>
    <field name='${mode_5_name}' value='${mode_5_nationality_name}'/>
    <field name='${mode_5_platform_name}' value='${mode_5_platform_id}'/>
    <field name='${mode_1_enhanced_name}' value='${mode_1_enhanced_id}'/>
    <field name='${mode_s_aircraft_name}' value='${mode_s_aircraft}'/>
    <field name='${amplification_name}' value='${amplification}'/>
    <field name='${amplification_amb_name}' value='${amplification_amb}'/>
    <field name='${bearing_origin_name}' value='${bearing_origin}'/>
    <field name='${subsurface_sensor_name}' value='${subsurface_sensor}'/>
    <field name='${audio_name}' value='${audio}'/>
    <field name='${sensor_depth_name}' value='${sensor_depth}'/>
    <field name='${broadband_noise_name}' value='${broadband_noise}'/>
    <field name='${confidence_level_name}' value='${confidence_level}'/>
    <field name='${depth_contact_name}' value='${depth_contact}'/>
    <field name='${sound_prop_name}' value='${sound_prop}'/>
    <field name='${doppler_name}' value='${doppler}'/>
    <field name='Track Label' value='${track_number}'/>
</createtrack>
"""

delay_line = """<wait seconds="1"/>"""

air_platform = (
    "N.S.",
    "Fighter",
    "Fighter Bomber",
    "Attack",
    "Bomber",
    "Reconnaissance",
    "Tanker",
    "Tanker (Boom Only)",
    "Tanker (Drogue Only)",
    "Interceptor",
    "Transport",
    "Airborne Command Post (ACP)",
    "Missile",
    "Electronic Warfare (EW)",
    "Antisubmarine Warfare (ASW)",
    "Airborne Early Warning and Control (AEW)",
    "Maritime Patrol Aircraft (MPA)",
    "Search and Rescue (SAR)",
    "Drone",
    "Remotely Piloted Vehicle (RPV)",
    "Fixed Wing Gunship",
    "Civil, Airliner",
    "Civil, General",
    "Lighter than Air (LTA)",
    "Glider",
    "Decoy",
    "Helicopter (HELO)",
    "Attack Helicopter",
    "Helicopter Gunship",
    "Antisubmarine Warfare Helicopter (ASW HELO)",
    "Mine Warfare Helicopter",
    "Transport Helicopter",
    "Tactical Support",
    "Patrol",
    "Miscellaneous Fixed Wing",
    "Missile Control Unit",
    "Surface-to-Air Missile (SAM)",
    "Air-to-Surface Missile (ASM)",
    "Surface-to-Surface Missile (SSM)",
    "Logistic",
    "Air-to-Air Missile (AAM)",
    "Subsurface-to-Surface Missile",
    "Surface-to-Subsurface Missile",
    "Cruise Missile",
    "Ballistic Missile",
    "Airborne Land Surveillance",
    "Airborne Laser",
    "Unmanned Aerial Vehicle (UAV)",
    "Active Electronic Decoy",
    "Infrared Decoy",
    "Chaff Decoy",
    "Hypersonic Vehicle",
    "Network Enabled Weapon",
    "RESET TO NO STATEMENT",
)

air_activity_type = (
    "N.S.",
    "Reconnaissance",
    "Over the Horizon Targeting (OTHT)",
    "Training",
    "Logistics Support",
    "Antisurface Warfare",
    "Electronic Warfare (EW)",
    "Surveillance",
    "Search and Rescue (SAR)",
    "Escorting",
    "Minelaying",
    "Transiting",
    "Special Weapons Attack",
    "Intruding",
    "Electronic Warfare Support (ES)",
    "Communications Relay",
    "Patrol (Ocean Surveillance)",
    "Airlift (Transport)",
    "Antisubmarine Warfare (ASW)",
    "Towing",
    "Air Assault",
    "Interception",
    "Electronic Attack (EA)",
    "Policing",
    "Conventional Attack",
    "Medical Evacuation (MEDEVAC)",
    "Mine Countermeasures",
    "Search",
    "Refueling/Tanking",
    "Interdiction",
    "Combat Air Patrol (CAP)",
    "Forward Air Controller (FAC)",
    "Very Important Person (VIP) Flight",
    "Noncombatant Operations",
    "Close Air Support (CAS)",
    "Airborne Early Warning (AEW)",
    "Ground Attack Tactics (GAT)",
    "Airborne Command Post (ACP)",
    "Rescue Combat Air Patrol (RESCAP)",
    "Surface Combat Air Patrol (SUCAP)",
    "Spotting",
    "Strike Warfare",
    "Special",
    "Hijack",
    "Jammer",
    "Trooplift",
    "XRay",
    "Antiair Warfare (AAW)",
    "Command and Control",
    "Counter-Air Warfare",
    "Return to Base (RTB)",
    "Mine Warfare",
    "Chaff Laying",
    "Video Data Linking (Targeting)",
    "Dipping",
    "Orbiting",
    "Under Recall",
    "Engaging",
    "Engaging (Priority Kill)",
    "Investigating",
    "Cleared to Drop",
    "Intervening",
    "Diverting",
    "Air-to-Ground",
    "Air-to-Air",
    "Precision Bombing",
    "Laser Designation",
    "Shadowing",
    "Covering",
    "Visual Identification",
    "High Energy Lasing",
    "Electronic Protection (EP)",
    "Special Operations",
    "Nuclear, Biological, Chemical (NBC) Operations",
    "Nuclear Operations",
    "Biological Operations",
    "Chemical Operations",
    "Aborting Mission",
    "Standoff Operations",
    "Combat Search and Rescue (CSAR)",
    "Aborting",
    "Awaiting Release",
    "Air Activity 1",
    "Air Activity 2",
    "Air Activity 3",
    "Air Activity 4",
    "Air Activity 5",
    "Air Activity 6",
    "Air Activity 7",
    "Air Activity 8",
    "Air Activity 9",
    "Air Activity 10",
    "Air Activity 11",
    "Air Activity 12",
    "RESET TO NO STATEMENT",
)

air_specific_type = (
    "N.S.",
    "F-4 PHANTOM II",
    "F-5 TIGER II",
    "F-14 TOMCAT",
    "F-15 EAGLE",
    "F-16 FIGHTING FALCON",
    "F-104 STARFIGHTER",
    "F-111",
    "F/A-18 A/B/C/D HORNET",
    "EFA/TYPHOON",
    "F-100",
    "COMMANDO",
    "J-35 DRAKEN",
    "JAGUAR",
    "SUPER ETENDARD",
    "F-1",
    "F-35XD DRAKEN",
    "TORNADO F3",
    "HF-24 MARUT (WIND SPIRIT)",
    "JA37 VIGGEN",
    "SF-5 FREEDOM FIGHTER",
    "IAR-91 ORAO",
    "KFIR C2",
    "MIRAGE F1",
    "MIRAGE 3",
    "MIRAGE 5",
    "MIRAGE 50",
    "MIRAGE 2000",
    "ALPHA JET",
    "KEFIR",
    "F-6 FARMER",
    "F-8 FISHBED",
    "F-9 FANTAN",
    "F-12 (CHINA)",
    "SU-7 FITTER",
    "SU-9 FISHPOT",
    "SU-11 FISHPOT",
    "SU-15 FLAGON",
    "SU-17 FITTER",
    "SU-19 FENCER",
    "SU-20 FITTER",
    "SU-22 FITTER",
    "SU-24 FENCER",
    "SU-25 FROGFOOT",
    "TU-28 FIDDLER",
    "TU-128 FIDDLER",
    "MIG-21 FISHBED",
    "MIG-23 FLOGGER",
    "MIG-25 FOXBAT",
    "MIG-27 FLOGGER",
    "YAK-28P FIREBAR",
    "YAK-36 FORGER",
    "AAF RAM-J",
    "MIG-15 FAGOT",
    "MIG-17 FRESCO",
    "MIG-19 FARMER",
    "SU-27 FLANKER",
    "MIG-29 FULCRUM",
    "MIG-31 FOXHOUND",
    "YAK-38 FORGER-A",
    "F/A-22 RAPTOR",
    "IDF CHING-KUO (TAIWAN)",
    "JAS-39 GRIPPEN",
    "F-7 JIAN JI-7",
    "F-8 JIAN JI-8-2",
    "F-35A LIGHTNING II",
    "KFIR C7",
    "KFIR 2000",
    "RAFALE",
    "SU-30 FLANKER",
    "SU-33 (SU-27K) FLANKER-D",
    "SU-34 FULLBACK-A",
    "SU-35 FLANKER-E",
    "SU-37 FLANKER-E VAR 2",
    "SU-39 FROGFOOT-C",
    "F-5 FRESCO",
    "J-9",
    "RT33",
    "CF-188 HORNET",
    "UNDEFINED",
    "F/A-18E/F SUPER HORNET",
    "F-5E",
    "F-5F",
    "F-14B TOMCAT",
    "F-14D TOMCAT",
    "F-15E STRIKE EAGLE",
    "F-5A/B/G",
    "SU-32 FLANKER",
    "MIRAGE 2000-5",
    "SU-7A FITTER",
    "SU-7U MOUJIK",
    "SU-15E FLAGON",
    "SU-15F FLAGON",
    "SU-17B FITTER",
    "SU-17C FITTER",
    "SU-17D FITTER",
    "SU-17H FITTER",
    "SU-17K FITTER",
    "SU-21 FLAGON",
    "SU-22F FITTER",
    "SU-22G FITTER",
    "SU-22J FITTER",
    "SU-24A FENCER",
    "SU-24B FENCER",
    "SU-24C FENCER",
    "MIG-21H FISHBED",
    "MIG-21J FISHBED",
    "MIG-21K FISHBED",
    "MIG-21L FISHBED",
    "MIG-21N FISHBED",
    "MIG-23B FLOGGER",
    "MIG-23E FLOGGER",
    "MIG-23F FLOGGER",
    "MIG-23H FLOGGER",
    "MIG-25A FOXBAT",
    "MIG-25B FOXBAT",
    "MIG-25D FOXBAT",
    "MIG-25E FOXBAT",
    "MIG-27D FLOGGER",
    "MIG-27J FLOGGER",
    "YAK-28D BREWER",
    "YAK-28E BREWER",
    "MIG-23G FLOGGER",
    "YAK-28 BREWER",
    "YAK-28U MAESTRO",
    "YAK-38V FORGER",
    "AV-8B HARRIER II",
    "AV-8B NIGHT ATTACK HARRIER",
    "AV-8D NIGHT ATTACK HARRIER",
    "AV-8B HARRIER II PLUS",
    "F-35B LIGHTNING II",
    "F-35C LIGHTNING II",
    "EF-18M HORNET",
    "FIGHTER (VTOL/VSTOL) GENERAL",
    "FIGHTER/FIGHTER BOMBER GENERAL",
    "A-4 SKYHAWK",
    "A-6 INTRUDER",
    "A-7 CORSAIR II",
    "A-10 THUNDERBOLT II",
    "A-37 DRAGONFLY",
    "B-1B LANCER",
    "B-52 STRATOFORTRESS",
    "AC-130 SPECTRE",
    "FB-111 AARDVARK",
    "A-1",
    "TA-28",
    "AC-47",
    "35XD DRAKEN",
    "J-1 HAWK",
    "J-1 JASTREB",
    "S-2",
    "AJ37 VIGGEN",
    "HA220 SUPER SAETA",
    "M.B.326",
    "M.B.339",
    "SF 260 WARRIOR",
    "SK 60",
    "BAC 167 STRIKEMASTER",
    "TORNADO GR-1",
    "IL-28 BEAGLE",
    "TU-16 BADGER",
    "TU-22 BLINDER",
    "TU-22M BACKFIRE",
    "TU-95 BEAR",
    "TU-142 BEAR",
    "TU-160 BLACKJACK",
    "AMX",
    "F-117 NIGHTHAWK",
    "G4 SUPER GALEB",
    "HAWK-2000",
    "HAWK-100",
    "HAWK-200",
    "HAWK-50",
    "HAWK-60",
    "IA-58 PUCARA",
    "IAR-93 ORAO",
    "IAR-99 SOIM",
    "JIAN JI-5M",
    "A-5 FANTAN",
    "L59 ALBATROS",
    "B-2 SPIRIT",
    "B-7 HONGZHA",
    "1050E",
    "HARRIER GR7",
    "TORNADO GR4/4A",
    "A-6E INTRUDER",
    "A-6F INTRUDER",
    "A-7C CORSAIR II",
    "A-7D CORSAIR II",
    "A-7E CORSAIR II",
    "TU-16A BADGER",
    "TU-22A BLINDER",
    "TU-22B BLINDER",
    "TU-95A BEAR",
    "TU-95B BEAR",
    "TU-95C BEAR",
    "TU-95D BEAR",
    "TU-95G BEAR",
    "TU-95H BEAR",
    "L-39ZA ALBATROS",
    "AL-1 AIRBORNE LASER",
    "MIRAGE 2000 N/D",
    "HARRIER GR9/9A",
    "AT-6",
    "BOMBER/ATTACK GENERAL",
    "E-2C HAWKEYE",
    "E-3 SENTRY (AWACS)",
    "E-4 NAOC",
    "EA-6 PROWLER",
    "EC-130 HERCULES",
    "EF-4 WILD WEASEL",
    "EP-3 ORION",
    "KC-10 EXTENDER",
    "KC-130 HERCULES",
    "KC-135 STRATOTANKER",
    "O-1 BIRD DOG",
    "O-2",
    "OV-1 MOHAWK",
    "OV-10 BRONCO",
    "P-3 ORION",
    "RC-130 HERCULES",
    "RC-135",
    "RF-4 PHANTOM II",
    "RF-5",
    "RF-14 TOMCAT",
    "RF-104 STARFIGHTER",
    "RP-3 ORION",
    "RU-21 UTE",
    "S-2 TRACKER",
    "S-3B VIKING",
    "SR-71 BLACKBIRD",
    "U-2",
    "U-4 AERO COMMANDER",
    "U-8 SEMINOLE",
    "U-10 COURIER",
    "UC-12 HURON",
    "U-21 UTE",
    "US-3 VIKING",
    "OA-37 DRAGONFLY",
    "TR-1",
    "WC-130 HERCULES",
    "SEA SCAN",
    "FALCON 20 GUARDIAN",
    "BR 1150 ATL1",
    "RF-35XD DRAKEN",
    "BN-2T MARITIME DEFENDER",
    "CP-140 AURORA",
    "HS.748 COASTGUARDER",
    "NIMROD MR2",
    "MK.3",
    "RJ-1 HAWK",
    "RJ-1 JASTREB",
    "KC-97",
    "AU-24",
    "AU-23",
    "U-17",
    "HU-16",
    "U-9",
    "U-3",
    "NKC-135",
    "RF-111",
    "BE-12 MAIL",
    "IL-38 MAY",
    "TU-126 MOSS",
    "VC10 (TANKER)",
    "AN-12 CUB-A (ELINT)",
    "AN-12 CUB-C (EA)",
    "AN-12 CUB-D (EA)",
    "IL-20 COOT-A (ELINT)",
    "IL-76 MAINSTAY",
    "E-8C (JSTARS)",
    "TORNADO ECR",
    "EMB-111",
    "MU-2S",
    "A40 ALBATROS",
    "BE42 MERMAID",
    "CL215 AMPHIBIAN",
    "IAI 1125",
    "IL22 COOT B",
    "J32 LANSEN",
    "SH5 HARBIN",
    "US1 (SHIN)",
    "CESSNA 550 CITATION II",
    "CESSNA 560 CITATION V",
    "DORNIER 27",
    "NIMROD MRA4",
    "CP-140A ARCTURUS",
    "RC-135 RIVET JOINT",
    "ATL 2",
    "ETENDARD IV P",
    "ALIZE",
    "FALCON 50",
    "MIRAGE IV",
    "BR 1150 GE ATL ASW",
    "BR 1150 GE ATL SIGINT",
    "SENTINEL R1",
    "E-3A SENTRY (AWACS)",
    "E-3B/C SENTRY (AWACS)",
    "E-3D SENTRY (AWACS)",
    "E-3F SENTRY (AWACS)",
    "E-4B NAOC",
    "EA-6B PROWLER",
    "EC-130E HERCULES",
    "EC-130H HERCULES",
    "EC-130J HERCULES",
    "NIMROD R",
    "KC-10A EXTENDER",
    "KC-130J HERCULES",
    "OV-2A SKYMASTER",
    "U-2R",
    "US-3A VIKING",
    "WC-130J HERCULES",
    "U-2S",
    "AN-12 CUB-B (ELINT)",
    "IL-76 CANDID-B",
    "E-6A TACAMO",
    "CL-415 AMPHIBIAN",
    "A-4M SKYHAWK",
    "TU-16B BADGER",
    "TU-16C BADGER",
    "TU-16D BADGER",
    "TU-16E BADGER",
    "TU-16F BADGER",
    "TU-16G BADGER",
    "TU-16H BADGER",
    "TU-16J BADGER",
    "TU-16K BADGER",
    "TU-16M BADGER",
    "TU-22C BLINDER",
    "TU-95E BEAR",
    "TU-95F BEAR",
    "RC-135 COBRA BALL",
    "RC-135 COMBAT SENT",
    "E/A-18G GROWLER",
    "HU-25 GUARDIAN",
    "A310 MRTT",
    "MIRAGE F1 CR",
    "E-6B ABNCP",
    "AN-28 BRYZA B1R",
    "P-8A MMA",
    "A330 MRTT",
    "TRISTAR L1011 K1/KC1 TANKER",
    "TORNADO GR4A RECCE",
    "CASA CN-235 MPA",
    "E-767 (AWACS)",
    "P-1",
    "JLENS AEROSTAT",
    "HC-130J",
    "E-11A",
    "TANKER",
    "RECONNAISSANCE (RECON)",
    "ELECTRONIC WARFARE (EW)",
    "ASW",
    "AEW AND C",
    "MISCELLANEOUS GENERAL",
    "T-2 BUCKEYE",
    "T-28 TROJAN",
    "T-29",
    "T-34 MENTOR",
    "T-37 TWEET",
    "T-38 TALON",
    "T-39 SABRELINER",
    "T-41 MESCALERO",
    "T-42 COCHISE",
    "T-43",
    "T-44 KING AIR",
    "TA-4 SKYHAWK",
    "TA-7 CORSAIR II",
    "T-33",
    "B3LA",
    "C-101 AVIOJET",
    "G2-A GALEB",
    "G2-A SEAGULL",
    "L-29 DELFIN",
    "L-39 ALBATROS",
    "L-70 MILTRAINER",
    "L-450",
    "P.55",
    "T-2",
    "CM 170 MAGISTER",
    "CM AU/MAGISTER",
    "SF-260",
    "SH 37 VIGGEN",
    "SK 37 VIGGEN",
    "TB30 EPSILON",
    "TF-35XD",
    "TJ-1 HAWK",
    "TJ-1 JASTREB",
    "TS.11 SPARK",
    "AW1-2 FAN TRAINER",
    "HJT-16 KIRAN",
    "MBB223 FLAMINGO",
    "SU-11 MAIDEN",
    "SU-15C",
    "MIG-15 MIDGET",
    "MIG-17",
    "MIG-21U MONGOL",
    "MIG-23C",
    "MIG-25C",
    "YAK-11 MOOSE",
    "YAK-18 MAX",
    "YAK-28 MAESTRO",
    "T-46A",
    "EMB-312 TOUCAN",
    "T-45 GOSHAWK",
    "T-47",
    "AS202",
    "CT114 TUTOR",
    "G91T (FIAT JET 1)",
    "K8 (NAMC)",
    "L70 VINKA",
    "STRIKEMASTER",
    "T1 JAYHAWK",
    "T4",
    "CT-142 DASH 8",
    "B-55 BARON",
    "F-33 BONANZA",
    "PILLAN-TAMIZ",
    "CT-133 SILVERSTAR",
    "TU-22D BLINDER",
    "T10 HARRIER",
    "TAV-8B HARRIER",
    "L-39C ALBATROS",
    "L-39MS ALBATROS",
    "L-39Y ALBATROS",
    "L-39ZO ALBATROS",
    "SU-17E FITTER",
    "SU-17G FITTER",
    "YAK-38B FORGER",
    "CT-155 HAWK",
    "CT-156 HARVARD",
    "PZL-130T ORLIK",
    "TB-20",
    "TRAINER GENERAL",
    "GLOBAL HAWK",
    "PREDATOR A",
    "PREDATOR B",
    "SHADOW 200",
    "HUNTER",
    "SILVER FOX",
    "DRAGON EYE",
    "FIRE SCOUT",
    "EAGLE",
    "CRECERELLE",
    "SHARC",
    "HERON",
    "RANGER",
    "SPERWER",
    "PHOENIX",
    "HERMES",
    "DESERT HAWK",
    "BUSTER",
    "WATCHKEEPER",
    "PREDATOR ARMED MQ-1",
    "GRAY EAGLE",
    "MQ-4C TRITON",
    "TACTICAL UNMANNED AERIAL VEHICLE (TUAV) GENERAL",
    "UNMANNED AERIAL VEHICLE (UAV) GENERAL",
    "UNMANNED COMBAT AIR VEHICLE (UCAV) GENERAL",
    "C-1 COD",
    "C-2 GREYHOUND",
    "C-5 GALAXY",
    "C-7 CARIBOU",
    "C-9 NIGHTINGALE",
    "C-12 HURON",
    "C-123 PROVIDER",
    "C-130 HERCULES",
    "C-135 STRATOLIFTER",
    "C-140 JETSTAR",
    "C-141 STARLIFTER",
    "HC-130 HERCULES",
    "VC-6 KING AIR",
    "VC-9 SKYTRAIN II",
    "VC-11 GULFSTREAM",
    "VC-137",
    "B707",
    "B720",
    "B727",
    "B737",
    "B747",
    "B757",
    "B767",
    "L-100 HERCULES",
    "L-1011 TRI STAR",
    "DC-8",
    "DC-9",
    "DC-10",
    "C-119",
    "DC-130",
    "HC-97",
    "C-JM",
    "C-54",
    "C-97",
    "C-118",
    "C-121",
    "C-124",
    "C-131",
    "C-133",
    "VC-47",
    "CV-54",
    "CV-140",
    "ARAVA",
    "BN-2B ISLANDER",
    "SKYVAN",
    "TRIDENT",
    "A300 AIRBUS",
    "A310 AIRBUS",
    "C-160 TRANSALL",
    "C-207 AZOR",
    "C-212 AVIOCAR",
    "F27 FRIENDSHIP",
    "F28 FELLOWSHIP",
    "G222 SAMA",
    "AW.660 ARGOSY",
    "BAC1-11",
    "DHC-5 BUFFALO",
    "DHC-7 DASH",
    "AN-2 COLT",
    "AN-10 CAT",
    "AN-12 CUB",
    "AN-14 CLOD",
    "AN-22 COCK",
    "AN-24 COKE",
    "AN-26 CURL",
    "AN-28 CASH",
    "AN-30 CLANK",
    "AN-32 CLINE",
    "AN-40",
    "AN-72 COALER",
    "IL-12 COACH",
    "IL-18 COOT",
    "IL-62 CLASSIC",
    "IL-76 CANDID",
    "IL-86 CAMBER",
    "TU-114 CLEAT",
    "TU-134 CRUSTY",
    "TU-144 CHARGER",
    "TU-154 CARELESS",
    "YAK-40 CODLING",
    "YAK-42 CLOBBER",
    "TU-104",
    "YAK-27",
    "IL-38",
    "DO-228 LT (TRANSPORT)",
    "AN-74",
    "AN-124 CONDOR",
    "A320 AIRBUS",
    "A321 AIRBUS",
    "A330 AIRBUS",
    "A340 AIRBUS",
    "AN-70",
    "AN-225 COSSACK",
    "BAE-125-600",
    "BAE146",
    "B777",
    "C-17 GLOBEMASTER III",
    "C-20 GULFSTREAM 3/4",
    "C-21 LEARJET 35",
    "C-22",
    "C-23 SHERPA/SHORTS 330",
    "C-26 METRO 3",
    "YS 11",
    "CL-600 CHALLENGER",
    "CL-601 CHALLENGER",
    "CN-235M",
    "EMB-120 BRASILLIA ADV",
    "EMB-145 AMAZON",
    "IL-78 MIDAS",
    "MD-11",
    "MD-80",
    "MD-90",
    "PD-808",
    "TU-44",
    "V-22 OSPREY",
    "VC-25",
    "XC-2",
    "IAI 1124",
    "1900",
    "580",
    "ATR42",
    "C46 COMMANDO",
    "CARAVELL",
    "CC109",
    "DHC2",
    "DHC6 TWIN OTTER",
    "DHC8",
    "EMB110 BANDEIRANTE",
    "EMB121",
    "FALCON 200/FALCON 20",
    "FALCON 900",
    "FH227 FRIENDSHIP",
    "FOKKER 100",
    "FOKKER 50",
    "FOKKER 60",
    "FOKKER 70",
    "GROB G850",
    "GULFSTREAM 1",
    "GULFSTREAM 2",
    "JETSTREAM",
    "JETSTREAM 31",
    "KING AIR",
    "L410 TURBOJET",
    "LEARJET 23",
    "LEARJET 24",
    "LEARJET 25 (IMPROVED VER 28)",
    "LEARJET 35/36",
    "LEARJET 55 (IMPROVED VER 28)",
    "LEARJET 60",
    "MERLIN 2",
    "MERLIN 3",
    "MERLIN 4",
    "METRO 3",
    "SAAB 2000",
    "SAAB 340",
    "SABRELINER",
    "U6 BEAVER",
    "VISCOUNT",
    "Y11",
    "Y12",
    "Y5",
    "CC-115 BUFFALO",
    "CC-130 HERCULES",
    "CC-150 POLARIS",
    "C-235 CASA",
    "CC-138 TWIN OTTER",
    "DO-228 LM (POLLUTION CONTROL)",
    "C-9 SKYTRAIN",
    "C-9B SKYTRAIN II",
    "A319 AIRBUS",
    "A400M AIRBUS",
    "MV-22 OSPREY",
    "MC-130H/J COMBAT TALON",
    "C-130 H-30 HERCULES",
    "C-130 J-30 HERCULES",
    "TBM 700",
    "C-130J HERCULES",
    "M-28",
    "ISLANDER BN2T",
    "C130 HERCULES C1/C3 K",
    "HERCULES C-130 C4/C5(J)",
    "C-27J SPARTAN",
    "LIGHT CIVIL",
    "TRANSPORT/AIRLINER GENERAL",
    "AH-1 COBRA",
    "AH-64 APACHE",
    "CH-3",
    "CH-46 SEA KNIGHT",
    "CH-47 CHINOOK",
    "CH-53 SEA STALLION",
    "CH-54 LARKE (SKYCRANE)",
    "EH-60B QUICK FIX",
    "HH-1 IROQUOIS",
    "HH-2 SEA SPRITE",
    "HH-3 JOLLY GREEN",
    "HH-52",
    "HH-53",
    "OH-6",
    "OH-58 KIOWA",
    "RH-3 SEA KING",
    "RH-53",
    "SH-2 SEA SPRITE",
    "SH-3 SEA KING",
    "SH-60 SEA HAWK",
    "UH-1 IROQUOIS",
    "UH-2 SEA SPRITE",
    "UH-12",
    "UH-46",
    "UH-60 BLACKHAWK",
    "CH-2U",
    "HH-43",
    "A109",
    "A129 MONGOOSE",
    "BO-105",
    "CH-124 SEA KING",
    "SA 315 LAMA",
    "SA 330 PUMA",
    "SA 332 SUPER PUMA",
    "SA 350 ASTAR",
    "SA 360 DAUPHIN",
    "SA 361 DAUPHIN",
    "WG-13 LYNX",
    "KA-18 HOG",
    "KA-20 HARP",
    "KA-25 HORMONE",
    "KA-26 HOODLUM",
    "MI-1 HARE",
    "MI-2 HOPLITE",
    "MI-4 HOUND",
    "MI-6 HOOK",
    "MI-8 HIP",
    "MI-10 HARKE",
    "MI-12 HOMER",
    "MI-14 HAZE",
    "MI-24 HIND",
    "MI-26 HALO",
    "CH-53E SUPER STALLION",
    "MH-53E SEA DRAGON",
    "HH-60 NIGHT HAWK",
    "HH-65A DOLPHIN",
    "KA-27 HELIX-A (ASW)",
    "KA-32 HELIX-C",
    "MI-17 HIP-H",
    "MI-28 HAVOC",
    "AS-355 ECUREUIL/FENNEL/ ESQILO",
    "KA-29 HELIX-B",
    "KA-50 HOKUM",
    "204 BELL",
    "205 BELL",
    "206 BELL",
    "214 BELL",
    "280 ENSTROM",
    "300 SCHWEIZER",
    "406 COMBAT SCOUT",
    "A 109 HIRUNDO",
    "ALOUETTE 3",
    "AS 350 ECUREUIL",
    "AS 532 COUGAR",
    "AS 550 FENNEC",
    "AS 555 FENNEC",
    "AS 565 PANTHER",
    "EH 101",
    "KA-28 HELIX A",
    "MD 500 DEFENDER",
    "MI-22 HOOK",
    "MI-25 HIND",
    "MI-35 HIND-V",
    "MI-9 HIP",
    "SA 341 GAZELLE",
    "SA 342 GAZELLE",
    "SA 365 DAUPHIN 2",
    "Z9",
    "CH-146 GRIFFON",
    "SEA KING ASACS MK7",
    "MERLIN HM1",
    "AB-212 AUGUSTA BELL",
    "HUGHES 3000",
    "SH-70L",
    "CH-113 LABRADOR",
    "NH 90 (C2)",
    "NH 90 (RECCE)",
    "NH 90 (EW/SEAD)",
    "NH 90 (TRANSPORT)",
    "SEA LYNX MK88A",
    "SEA KING MK41",
    "TIGER (HAP)",
    "NH 90 (NAVY)",
    "TIGER (HAC)",
    "SA 341 GAZELLE CANON",
    "AW-520 SAR CORMORANT",
    "W3 SOKOL",
    "AH-1J SEA COBRA",
    "AH-1S SEA COBRA",
    "AH-1T SEA COBRA",
    "AH-64A APACHE",
    "EH-60 BLACKHAWK",
    "UH-60A BLACKHAWK",
    "KA-25A HORMONE",
    "KA-25B HORMONE",
    "KA-25C HORMONE",
    "KA-27 HELIX",
    "MI-8C HIP",
    "MI-8D-HIP",
    "MI-8E HIP",
    "MI-8F HIP",
    "MI-8H HIP",
    "MI-8J HIP",
    "MI-8K HIP",
    "MI-14 HAZE-A",
    "MI-14 HAZE-B",
    "MI-24 HIND-A",
    "MI-24 HIND-B",
    "MI-24 HIND-C",
    "MI-24 HIND-D",
    "MI-24 HIND-E",
    "MH-68A STINGRAY",
    "EC-725 CARACAL",
    "MH-60R",
    "MH-60S",
    "W-3W",
    "W-3SRR",
    "W-3PPD",
    "MI-17 MEDEVAC",
    "LYNX AH1",
    "LYNX HAS3",
    "LYNX HMA8",
    "MERLIN HC3",
    "SEA KING HC4",
    "SEA KING HAR3/3A",
    "SEA KING HAR5",
    "SEA KING HAS6",
    "SEA KING HAS7",
    "APACHE AH1",
    "GRIFFIN HT1",
    "MRH 90",
    "GAZELLE AH1",
    "APACHE LONGBOW AH1",
    "BELL 212 HPAH1",
    "LYNX HAS2",
    "AGUSTA A109A/E",
    "PUMA HC1",
    "PUMA C2",
    "COUGAR C2",
    "HELICOPTER GENERAL",
    "AIM-7 SPARROW",
    "AIM-9 SIDEWINDER",
    "AIM-54 PHOENIX",
    "AIM-120 AMRAAM",
    "ASLAM",
    "R.550 MAGIC 2",
    "S.530 SUPER 530",
    "ASPIDE",
    "SHAFRIR",
    "SKY FLASH",
    "AA-2 ATOLL",
    "AA-3 ANAB",
    "AA-5 ASH",
    "AA-6 ACRID",
    "AA-7 APEX",
    "AA-8 APHID",
    "AA-9 AMOS",
    "AA-XP-1/2",
    "AQM-34",
    "AQM-91",
    "BGM-34 FIREBEE/MQM34",
    "AIM-132 ASRAAM",
    "MICA IR",
    "PL-2A",
    "PL-5B",
    "PL-7",
    "PL-9",
    "PYTHON 3",
    "PYTHON 4",
    "AA-10 ALAMO",
    "AA-11 ARCHER",
    "AA-12 ADDER",
    "AA-1 ALKALI",
    "AAM-1",
    "MICA EM",
    "BQM-34 FIREBEE",
    "IRIS-T",
    "METEOR",
    "AIR-TO-AIR MISSILE GENERAL",
    "AGM-65 MAVERICK",
    "AGM-84 HARPOON",
    "AGM-86 ALCM",
    "AGM-88 HARM",
    "AGM-109 TOMAHAWK",
    "AM 39 EXOCET",
    "AGM-119 PENGUIN",
    "AS 11 KILTER",
    "AS 12 KEGLER",
    "AS 15 KENT",
    "AS 30",
    "RB 05",
    "RB 08",
    "ADVANCED ASM",
    "AS-1 KENNEL",
    "AS-2 KIPPER",
    "AS-3 KANGAROO",
    "AS-4 KITCHEN",
    "AS-5 KELT",
    "AS-6 KINGFISH",
    "AS-7 KERRY",
    "AS-10 KAREN",
    "AS-9 KYLE",
    "AS 34 KORMORAN",
    "ASM GABRIEL",
    "ASM SEA SKUA",
    "ASMP",
    "AT-2 SWATTER",
    "AT-3 SAGGER",
    "AT-6 SPIRAL",
    "C-601",
    "C-611",
    "C-801",
    "C-802",
    "CSS-2",
    "CSS-3",
    "CSS-N-3",
    "CSS-4",
    "FL-2 SILKWORM",
    "FL-7",
    "HY-2",
    "HY-3",
    "M-9/11",
    "WS-1",
    "AS-13 KINGBOLT",
    "AS-14 KEDGE",
    "AS-16 KICKBACK",
    "AS-17 KRYPTON",
    "AS-18 KAZOO",
    "AT-4 SPIGOT",
    "AT-5 SPANDREL",
    "AT-7 SAXHORN",
    "AT-10 STABBER",
    "AT-11 SNIPER",
    "AT-12",
    "AT-13",
    "AT-14",
    "FROG-7",
    "SS-11 SEGO",
    "SS-13 SAVAGE",
    "SS-18 SATAN",
    "SS-19 STILETTO",
    "SS-24 SCALPEL",
    "SS-25 SICKLE",
    "SS-N-2 STYX",
    "SS-N-3C SHADDOCK",
    "SS-N-6 SAWFLY",
    "SS-N-7 STARBRIGHT",
    "SS-N-8 SAWFLY",
    "SS-N-9 SIREN",
    "SS-N-12 SANDBOX",
    "SS-N-18 STINGRAY",
    "SS-N-19 SHIPWRECK",
    "SS-N-20 STURGEON",
    "SS-N-21 SAMPSON",
    "SS-N-22 SUNBURN",
    "SS-N-23 SKIFF",
    "SS-N-26 YAKHONT",
    "AGNI",
    "PRITHVI",
    "TOW",
    "AGM-114 HELLFIRE",
    "MLRS",
    "HOT",
    "MILAN",
    "TRIGAT",
    "OTOMAT",
    "RBS-15M",
    "ARMAT",
    "ALARM",
    "AGM-62A WALLEYE",
    "AGM-123A SKIPPER II",
    "APACHE (ASM)",
    "AS 8",
    "AT-1 SNAPPER",
    "CAS1",
    "KH-41 MOSKIT",
    "MARTIN PESCADOR",
    "MAS1 CARCARA",
    "RB 04E",
    "STAR",
    "MM 38",
    "MM 40",
    "SM 39",
    "AS 34 KORMORAN II",
    "SS-1-B (SCUD-A)",
    "SS-1-C (SCUD-B)",
    "SS-1-D (SCUD-C)",
    "SS-1-E (SCUD-D)",
    "SS-N-3",
    "SS-N-3B SEPAL",
    "SS-N-2C STYX",
    "SS-N-5 SARK",
    "PRITHVI-I",
    "PRITHVI-II",
    "SS-N-25 SWITCHBLADE",
    "SS-N-27 ALFA",
    "SS-N-29 MEDVEDKA",
    "SS-NX-30 BULAVA",
    "AS-30 L",
    "SCALP-EG",
    "TAURUS",
    "SUBSURFACE-SURFACE MISSILE GENERAL",
    "SURFACE-SURFACE MISSILE (SSM) GENERAL",
    "AIR-SURFACE MISSILE (ASM) GENERAL",
    "ANTI-RADIATION MISSILE (ARM) GENERAL",
    "GROUND-GROUND MISSILE GENERAL",
    "AIR-GROUND MISSILE GENERAL",
    "FIM-92 STINGER",
    "MIM-23 HAWK",
    "MIM-104 PATRIOT",
    "RIM-7 SEA SPARROW",
    "RIM-66 STANDARD MISSILE",
    "RIM-67 STANDARD MISSILE",
    "BLOWPIPE",
    "SEA DART",
    "SEA WOLF",
    "S 440 CROTALE EDIR",
    "RAPIER",
    "RBS-70",
    "SAM ROLAND",
    "SA-2 GUIDELINE",
    "SA-3 GOA",
    "SA-4 GANEF",
    "SA-N-3 GOBLET",
    "SA-5 GAMMON",
    "SA-N-4 GECKO",
    "SA-6 GAINFUL",
    "SA-N-6 GRUMBLE",
    "SA-7 GRAIL",
    "SA-8 GECKO",
    "SA-9 GASKIN",
    "SA-10 GRUMBLE",
    "SA-11 GADFLY",
    "SA-13 GOPHER",
    "MISTRAL",
    "SA-N-7 GADFLY",
    "SA-N-8 GREMLIN",
    "SA-16 GIMLET",
    "SA-N-5 GRAIL",
    "SA-N-11 GRISOM",
    "SA-12A GLADIATOR",
    "SA-12B GIANT",
    "SA-14 GREMLIN",
    "SA-15 GAUNTLET",
    "SA-17 GRIZZLY",
    "SA-N-12 GRIZZLY",
    "SA-18 GROUSE",
    "SA-19 GRISOM",
    "RIM-116 RAM",
    "ADATS",
    "JAVELIN",
    "STARBURST",
    "STARSTREAK",
    "I-HAWK",
    "ROLAND II",
    "SM-2 BLOCK II",
    "SM-2 BLOCK III",
    "SM-2 BLOCK IIIA",
    "SM-2 BLOCK IIIB",
    "SM-2 BLOCK IV",
    "SM-2 BLOCK IVA",
    "SM-3",
    "AKASH",
    "ANZA",
    "ANZA II",
    "CSA-1",
    "CSA-N-2",
    "CSA-4",
    "CSA-5",
    "FM-80",
    "HN-5",
    "NK-7",
    "NK-16",
    "SA-22 GREYHOUND",
    "RAPIER 2000/JERNAS",
    "RBS-90",
    "SAKR",
    "SAVA",
    "SHANINE",
    "SKYGUARD ASPIDE",
    "SPADA",
    "SA-N-1 GOA",
    "SA-N-9 GAUNTLET",
    "SA-N-10",
    "ALBATROS/ASPIDE",
    "SM-1",
    "VT1 CROTALE",
    "MASURCA",
    "ASTER 15",
    "ASTER 30 B1",
    "SA-20 GARGOYLE",
    "SM-6 BLOCK I",
    "SM-6 DUAL II",
    "PATRIOT ASOJ",
    "PATRIOT PAC-2 ATM",
    "PATRIOT ATM",
    "PATRIOT ATM1 (GEM)",
    "PATRIOT ATM1C",
    "PATRIOT ATM1T",
    "PATRIOT ATM2",
    "SM-6 DUAL I",
    "ASTER 30 B1NT",
    "RESET TO NO STATEMENT",
    "SURFACE-TO-AIR MISSILE GENERAL",
)

callsign_list = (
    "N.S.",
    "Soy Boi",
    "9 Lives",
    "Abnegation",
    "Adventurer",
    "Akula",
    "Alpha",
    "Angel",
    "Apex",
    "Archon",
    "Bad Luck",
    "BadKarma",
    "Banshee",
    "Bassman",
    "Batman",
    "Bazinga",
    "Bear",
    "Beast",
    "Berserker",
    "Blacksheep",
    "Blackskull",
    "Blackwolf",
    "Blue Fox",
    "Bobkat",
    "Bojay",
    "Bolo",
    "Bones",
    "Book",
    "Boomer",
    "Boy Scout",
    "Browncoat",
    "BullDog",
    "Demon",
    "Digger",
    "Diver",
    "Doc",
    "Dogsbody",
    "Dog Robber",
    "Donovan",
    "Dragonfire",
    "Dragonlady",
    "Druid",
    "Dynamo",
    "EMTDuck",
    "Ender",
    "Erudite",
    "Excalibur",
    "Hopper",
    "Hunter",
    "Huntress",
    "Hyema",
    "Iceman",
    "Inferno",
    "Irish",
    "Iron Patroit",
    "Islander",
    "J-Dawg",
    "Jailbreak",
    "Jaws",
    "Jester",
    "Joker",
    "Kaiserina",
    "Kiwi",
    "Knight",
    "Ladder",
    "Lanky",
    "Lemonhead",
    "Leprechaun",
    "Lifesaver",
    "Mystic",
    "Nehadi",
    "Nemesis",
    "Nightingale",
    "Night Raven",
    "Nightwing",
    "Nitehawk",
    "Northstar",
    "Odin",
    "Ogre",
    "Old Man",
    "Paladin",
    "Papa Bear",
    "Pappy",
    "Patchwork",
    "Payback",
    "Phoenix",
    "Piedra",
    "Pirate",
    "Pit Bull",
    "PixelDust",
    "Po",
    "Poindexter",
    "Prowler",
    "Psycho",
    "Top Doc",
    "Trouble",
    "Tusker",
    "Upchuck",
    "Vengi 57",
    "Viking",
    "Viper",
    "Warboy",
    "Wardog",
    "Whig",
    "Whizkid",
    "Wild Card",
    "Wildcat",
    "Wildrose",
    "Witchdoctor",
    "Wolf",
    "Wolverine",
    "Wraith",
)

ew_environment = ("Air", "Land", "Surface", "Subsurface", "Space")

ew_ind_name = (
    "J3.7 Track(EW Product Info)",
    "J3.7 Track(EW Product Info) with J14.0 Parametric Info",
    "J14.0 Track(EW Parametrics)",
)

tracktype35 = ("TRACK", "POINT")

land_platform = (
	"N.S.",
)

land_activity_type = (
	"N.S.",
)

land_specific_type = (
	"N.S.",
)

reference_track_point_name = (
    "Emergency",
    "Hazard",
    "Reference Point (General)",
    "Station (General)",
    "Station (Air)",
    "Area (General)",
    "Area (Hazard)",
    "ASW",
    "ASW, 1",
)

emergency_amp = (
    "N.S.",
)


reference_amp = (
    "N.S.",
)

general_station_amp = (
    "N.S.",
)

air_station_amp = (
    "N.S.",
)

general_area_amp = (
    "N.S.",
)

hazard_area_amp = (
    "N.S.",
)

asw_amp = (
    "N.S.",
)

asw1_amp = ("N.S.", "Charted Wreck", "Bottomed Nonsubmarine", "ASW Station")

hazard_amp = (
    "N.S."
)

track_ind_name = ("J3.4 Track(ASW)", "J5.4 Track(ASW Acoustic Bearing/Range)")

space_platform = (
	"N.S.",
)

space_specific_type = (
	"N.S.",
)

space_activity_type = (
	"N.S.",
)

space_amp = (
	"N.S.",
)

space_boost_indicator = ("NOT IN BOOST PHASE", "IN BOOST PHASE")

space_lost = ("Tracking", "Lost")

subsurface_platform = (
	"N.S.",
)

subsurface_activity_type = (
	"N.S.",
)

subsurface_specific_type = (
	"N.S.",
)

doppler_type_list = ("N.S.", "NO DOPPLER", "UP DOPPLER", "DOWN DOPPLER")

sound_prop_list = (
    "N.S.",
)

sensor_depth_list = ("N.S.", "ABOVE LAYER", "BELOW LAYER")

audio_list = ("N.S.", "AUDIO")

broadband_noise_list = ("N.S.", "BROADBAND NOISE")

subsurface_sensor_list = (
    "N.S.",
)

confidence_level_list = (
    "N.S.",
)

depth_contact_list = (
    "N.S.",
)

surface_platform = (
	"N.S.",
)

surface_activity_type = (
	"N.S.",
)

surface_specific_type = (
    "N.S.",
)

spitype = ("Yes", "No")

strength = (
    "N.S.",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "2 Through 7 (Few) Units",
    "Greater Than 7 (Many) Units",
    "Greater Than 12 Units",
)

track_identity = (
    "Unknown",
    "Pending",
    "Hostile",
    "Friend",
    "Neutral",
    "Assumed Friend",
    "Suspect",
)


track_profile = (
    "TOAD_J-Series_Air",
    "TOAD_J-Series_Land",
    "TOAD_J-Series_Surface",
    "TOAD_J-Series_SubSurface",
    "TOAD_J-Series_Space",
    "TOAD_J-Series_Reference_Point",
    "TOAD_J-Series_EW"
)

mode_1_options = (
    "N.S.",
    1,
    2,
    3,
    10,
    11,
    12,
    13,
    20,
    21,
    22,
    23,
    30,
    31,
    32,
    33,
    40,
    41,
    42,
    43,
    50,
    51,
    52,
    53,
    60,
    61,
    62,
    63,
    70,
    71,
    72,
    73,
)

mode_3_options = ("N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  "N.S.",
                  7500, 
                  7600, 
                  7700,)

mode_4_indicator = (
    "Not Interrogated",
    "No Response",
    "Invalid Response",
    "Valid Response",
)
mode_5_indicator = (
    "N.S.",
    "Interrogated, No Response",
    "Interrogated, Valid Response",
)

mode_5_nationality = (
    "N.S.",
    "Albania",
    "Belgium",
    "Bulgaria",
    "Canada",
    "Croatia",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Netherlands",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Turkey",
    "United Kingdom",
    "United States I",
    "United States II",
    "NATO",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Belarus",
    "Bonsnia and Herzegovina",
    "Finland",
    "Georgia",
    "Ireland",
    "Kazakhstan",
    "Kyrghyz Republic",
    "Malta",
    "Moldova",
    "Montenegro",
    "Russia",
    "Serbia",
    "Sweden",
    "Switzerland",
    "Tajikistan",
    "Macedonia",
    "Turkmenistan",
    "Ukraine",
    "Uzbekistan",
    "TA1",
    "TA2",
    "TA3",
    "TA4",
    "TA5",
    "TA6",
    "TA7",
    "TA8",
    "TA9",
    "TA10",
    "TA11",
    "TA12",
    "TA13",
    "TA14",
    "TA15",
)

# scenario generation starts here
def generate_track_code(n_tracks, delay_secs, pause_intervals=[]):
    global delay_line

    track_lines = []
    # Iterate through each track.
    # Make the name and get the parameters.
    # Add to list.
    line_length = 1000
    lat_offset = 0
    long_offset = 0

    pause_index = 0
    n_tracks_since_last_pause = 0

    for i in range(0, n_tracks):
        # Calc position
        lat = start_lat + lat_offset
        lon = start_long + long_offset

        long_offset += 0.02
        # Check boundary.
        if i % line_length == 0 and i != 0:
            long_offset = 0.1
            lat_offset += 0.1

        #Convert track number to int, then to octal
        track_number = oct(512 + i)[2:]
        name = track_number 
        profile = "TOAD_J-Series_Air"

        track3454ind = ""
        if profile == "TOAD_J-Series_SubSurface":
            track3454ind = "Track 3.4/5.4 Indicator"
        elif profile == "TOAD_J-Series_EW":
            track3454ind = "Track 3.7/14.0 Indicator"
        else:
            track3454ind = ""

        trackind = ""
        if profile == "TOAD_J-Series_SubSurface":
            trackind = random.choice(track_ind_name)
        elif profile == "TOAD_J-Series_EW":
            trackind = random.choice(ew_ind_name)
        else:
            trackind = ""

        identity_name = ""
        if (
            profile == "TOAD_J-Series_Reference_Point"
            or track3454ind == "J14.0 Track(EW Parametrics)"
        ):
            identity_name = ""
        else:
            identity_name = "Identity"

        identity = ""
        if (
            profile == "TOAD_J-Series_Reference_Point"
            or track3454ind == "J14.0 Track(EW Parametrics)"
        ):
            identity = ""
        else:
            identity = random.choice(track_identity)

        callsign_name = ""
        if profile == "TOAD_J-Series_Air":
            callsign_name = "Callsign Published"
        else: 
            callsign_name = ""

        callsign = ""
        if profile == "TOAD_J-Series_Air":
            callsign = random.choice(callsign_list)
        else: 
            callsign = ""

        env_cat_name = ""
        if profile == "TOAD_J-Series_EW":
            env_cat_name = "Environ/Category"
        else:
            env_cat = ""

        env_cat = ""
        if profile == "TOAD_J-Series_EW":
            env_cat = random.choice(ew_environment)
        else:
            env_cat = ""

        ew_track_type_name = ""
        if profile == "TOAD_J-Series_EW":
            ew_track_type_name = "Track Type"
        else:
            ew_track_type_name = ""

        ew_track_type = ""
        if profile == "TOAD_J-Series_EW":
            ew_track_type = "EW"
        else:
            ew_track_type = ""

        platform_name = ""
        if (
            profile == "TOAD_J-Series_Air"
            or profile == "TOAD_J-Series_Surface"
            or profile == "TOAD_J-Series_SubSurface"
            or profile == "TOAD_J-Series_Land"
            or profile == "TOAD_J-Series_Space"
            or profile == "TOAD_J-Series_EW"
        ):
            platform_name = "Platform"
        elif profile == "TOAD_J-Series_Reference_Point":
            platform_name = "Point Type"
        else:
            platform_name = ""

        platform = ""
        if profile == "TOAD_J-Series_Air" or env_cat == "Air":
            platform = random.choice(air_platform)
        elif profile == "TOAD_J-Series_Surface" or env_cat == "Surface":
            platform = random.choice(surface_platform)
        elif profile == "TOAD_J-Series_SubSurface" or env_cat == "Subsurface":
            platform = random.choice(subsurface_platform)
        elif profile == "TOAD_J-Series_Land" or env_cat == "Land":
            platform = random.choice(land_platform)
        elif profile == "TOAD_J-Series_Space" or env_cat == "Space":
            platform = random.choice(space_platform)
        elif profile == "TOAD_J-Series_Reference_Point":
            platform = random.choice(reference_track_point_name)
        else:
            platform = ""

        activity_name = ""
        if (
            profile == "TOAD_J-Series_Reference_Point"
            or track3454ind == "J3.7 Track(EW Product Info)"
        ):
            activity_name = ""
        else:
            activity_name = "Activity"

        activity = ""
        if profile == "TOAD_J-Series_Air" or env_cat == "Air":
            activity = random.choice(air_activity_type)
        elif profile == "TOAD_J-Series_Surface" or env_cat == "Surface":
            activity = random.choice(surface_activity_type)
        elif profile == "TOAD_J-Series_SubSurface" or env_cat == "Subsurface":
            activity = random.choice(subsurface_activity_type)
        elif profile == "TOAD_J-Series_Land" or env_cat == "Land":
            activity = random.choice(land_activity_type)
        elif profile == "TOAD_J-Series_Space" or env_cat == "Space":
            activity = random.choice(space_activity_type)
        else:
            activity = ""

        spec_type_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            spec_type_name = ""
        elif platform_name == "Platform":
            spec_type_name = "Specific Type"
        else:
            spec_type_name = "Amplification"

        spec_type = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            spec_type = ""
        elif profile == "TOAD_J-Series_Air":
            spec_type = random.choice(air_specific_type)
        elif profile == "TOAD_J-Series_Surface":
            spec_type = random.choice(surface_specific_type)
        elif profile == "TOAD_J-Series_SubSurface":
            spec_type = random.choice(subsurface_specific_type)
        elif profile == "TOAD_J-Series_Land":
            spec_type = random.choice(land_specific_type)
        elif profile == "TOAD_J-Series_Space":
            spec_type = random.choice(space_specific_type)
        elif env_cat == "Air":
            spec_type = random.choice(air_specific_type)
        elif env_cat == "Land":
            spec_type = random.choice(land_specific_type)
        elif env_cat == "Surface":
            spec_type = random.choice(surface_specific_type)
        elif env_cat == "Subsurface":
            spec_type = random.choice(subsurface_specific_type)
        elif env_cat == "Space":
            spec_type = random.choice(space_specific_type)
        elif platform == "Emergency":
            spec_type = random.choice(emergency_amp)
        elif platform == "Hazard":
            spec_type = random.choice(hazard_amp)
        elif platform == "Reference Point (General)":
            spec_type = random.choice(reference_amp)
        elif platform == "Station (General)":
            spec_type = random.choice(general_station_amp)
        elif platform == "Station (Air)":
            spec_type = random.choice(air_station_amp)
        elif platform == "Area (General)":
            spec_type = random.choice(general_area_amp)
        elif platform == "Area (Hazard)":
            spec_type = random.choice(hazard_area_amp)
        elif platform == "ASW":
            spec_type = random.choice(asw_amp)
        elif platform == "ASW, 1":
            spec_type = random.choice(asw1_amp)
        else:
            spec_type = ""

        amplification_name = ""
        if profile == "TOAD_J-Series_Space":
            amplification_name = "Space Amplification"
        else:
            amplification_name = ""

        amplification = ""
        if profile == "TOAD_J-Series_Space":
            amplification = random.choice(space_amp)
        else:
            amplification = ""

        time_function_name = ""
        if platform == "ASW":
            time_function_name = "Time Function"
        else:
            time_function_name = ""

        time_function = ""
        if (
            spec_type == "Sinker"
            or spec_type == "Brief Contact"
            or spec_type == "Search Center (ASW)"
            or spec_type == "Estimated Position (EP)"
            or spec_type == "Fix (ASW)"
            or spec_type == "Area of Probability (ASW)"
        ): 
            time_function = "TIME POINT ESTABLISHED"
        elif (
            spec_type == "Limiting Line of Approach"
            or spec_type == "Notack Area"
            or spec_type == "Moving Haven"
            or spec_type == "Notack Area"
            or spec_type == "Sonobuoy Position"

        ):
            time_function = "ACTIVATION TIME"
        else: time_function = ""

        amplification = ""
        if profile == "TOAD_J-Series_Space":
            amplification = random.choice(space_amp)
        else:
            amplification = ""

        amplification_amb_name = ""
        if profile == "TOAD_J-Series_Space":
            amplification_amb_name = "Space Amplification Ambiguity 1"
        else:
            amplification_amb_name = ""

        amplification_amb = ""
        if profile == "TOAD_J-Series_Space":
            amplification_amb = random.choice(space_amp)
        else:
            amplification_amb = ""

        alt_type = ""
        if (
            profile == "TOAD_J-Series_Air"
            or profile == "TOAD_J-Series_Space"
            or profile == "TOAD_J-Series_Reference_Point"
            or env_cat == "Air"
            or env_cat == "Land"
            or env_cat == "Subsurface"
            or env_cat == "Space"
        ):
            alt_type = "Altitude"
        elif (
            profile == "TOAD_J-Series_Surface"
            or trackind == "J5.4 Track(ASW Acoustic Bearing/Range)"
        ):
            alt_type = ""
        elif profile == "TOAD_J-Series_Land":
            alt_type = "Elevation"
        elif trackind == "J3.4 Track(ASW)":
            alt_type = "Depth"
        else:
            alt_type = ""

        alt = ""
        if profile == "TOAD_J-Series_Air" or env_cat == "Air":
            alt = random.randint(0, 204750)
        elif trackind == "J3.4 Track(ASW)" or env_cat == "Subsurface":
            alt = random.randint(0, 6200)
        elif (
            profile == "TOAD_J-Series_Land"
            or env_cat == "Land"
            or profile == "TOAD_J-Series_Reference_Point"
        ):
            alt = random.randint(0, 51150)
        elif profile == "TOAD_J-Series_Space" or env_cat == "Space":
            alt = random.randint(0, 204750)
        elif (
            profile == "TOAD_J-Series_Surface"
            or env_cat == "Surface"
            or trackind == "J5.4 Track(ASW Acoustic Bearing/Range)"
        ):
            alt = ""
        else:
            alt = ""

        land_type_name = ""
        if profile == "TOAD_J-Series_Land":
            land_type_name = "Point/Track Ind"
        else:
            land_type_name = ""

        land_type = ""
        if profile == "TOAD_J-Series_Land":
            land_type = random.choice(tracktype35)
        else:
            land_type = ""

        course_name = ""
        if land_type == "POINT":
            course_name = ""
        elif trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            course_name = "Bearing 1"
        else:
            course_name = "True Course"

        course = ""
        if land_type == "POINT":
            course = ""
        else:
            course = random.randint(0, 359)

        speed_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)" or land_type == "POINT":
            speed_name = ""
        else:
            speed_name = "Speed"

        speed = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)" or land_type == "POINT":
            speed = ""
        else:
            speed = random.randint(0, 300)

        bearing_origin_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            bearing_origin_name = "Bearing Origin"
        else:
            bearing_origin_name = ""

        bearing_origin = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            bearing_origin = "Latitude/Longitude"
        else:
            bearing_origin = ""

        hour_name = (
            "Hour"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            or trackind == "J3.5 Track(ASW Acoustic Bearing/Range)"
            or time_function_name == "Time Function"
            else ""
        )

        hour = (
            random.randint(00, 23)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            or trackind == "J3.5 Track(ASW Acoustic Bearing/Range)"
            or time_function_name == "Time Function"
            else ""
        )

        minute_name = (
            "Minute"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
                "TOAD_J-Series_Space",
            )
            or trackind == "J3.5 Track(ASW Acoustic Bearing/Range)"
            or time_function_name == "Time Function"
            else ""
        )

        minute = (
            random.randint(00, 59)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
                "TOAD_J-Series_Space",
            )
            or trackind == "J3.5 Track(ASW Acoustic Bearing/Range)"
            or time_function_name == "Time Function"
            else ""
        )

        seconds_name = ""
        if profile == "TOAD_J-Series_Space":
            seconds_name = "Seconds"
        else:
            seconds_name = ""

        second = ""
        if profile == "TOAD_J-Series_Space":
            second = random.randint(00, 59)
        else:
            second = ""

        strength_name = (
            "Strength"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        strength_type = (
            random.choice(strength)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        def get_mode_name(code: int) -> str:
            return (
                f"Mode {code} Code"
                if profile
                in (
                    "TOAD_J-Series_Air",
                    "TOAD_J-Series_Surface",
                    "TOAD_J-Series_SubSurface",
                    "TOAD_J-Series_Land",
                )
                else ""
            )

        mode_1_name = get_mode_name(1)
        mode_2_name = get_mode_name(2)
        mode_3_name = get_mode_name(3)

        mode_1 = (
            random.choice(mode_1_options)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_2 = (
            oct(random.randint(0, 4095))[2:]
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_3 = (
            random.choice(mode_3_options)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_4_indicator_type = (
            random.choice(mode_4_indicator)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_4_indicator_name = (
            "Mode 4 Indicator"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_5_indicator_type = (
            random.choice(mode_5_indicator)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_5_indicator_name = (
            "Mode 5 Indicator"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_5_nationality_name = (
            random.choice(mode_5_nationality)
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_5_name = (
            "Mode 5 Nationality"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_5_platform_id = (
            oct(random.randint(0, 16383))[2:]
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_5_platform_name = (
            "Mode 5 Platform ID"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_1_enhanced_name = (
            "Mode 1 Enhanced"
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )
        mode_1_enhanced_id = (
            oct(random.randint(0, 4095))[2:]
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
            )
            else ""
        )

        mode_s_aircraft_name = ""
        if profile == "TOAD_J-Series_Air":
            mode_s_aircraft_name = "Mode S Aircraft Address"

        mode_s_aircraft = ""
        if profile == "TOAD_J-Series_Air":
            mode_s_aircraft = random.randint(0, 16777214)

        spi = random.choice(spitype)

        boost_name = ""
        if profile == "TOAD_J-Series_Space":
            boost_name = "Boost Ind"
        else:
            boost_name = ""

        boost = ""
        if profile == "TOAD_J-Series_Space":
            boost = random.choice(space_boost_indicator)
        else:
            boost = ""

        lost_name = ""
        if profile == "TOAD_J-Series_Space":
            lost_name = "Lost Track Indicator"

        lost = ""
        if profile == "TOAD_J-Series_Space":
            lost = random.choice(space_lost)
        else:
            lost = ""

        doppler_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            doppler_name = "Doppler"
        else:
            doppler_name = ""

        doppler = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            doppler = random.choice(doppler_type_list)
        else:
            doppler = ""

        sound_prop_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            sound_prop_name = "Sound Propagation Path"
        else:
            sound_prop_name = ""

        sound_prop = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            sound_prop = random.choice(sound_prop_list)
        else:
            sound_prop = ""

        depth_contact_name = ""
        if profile == "TOAD_J-Series_SubSurface":
            depth_contact_name = "Depth Contact"
        else:
            depth_contact_name = ""

        depth_contact = ""
        if profile == "TOAD_J-Series_SubSurface":
            depth_contact = random.choice(depth_contact_list)
        else:
            depth_contact = ""

        confidence_level_name = ""
        if profile == "TOAD_J-Series_SubSurface":
            confidence_level_name = "Confidence Level"
        else:
            confidence_level_name = ""

        confidence_level = ""
        if profile == "TOAD_J-Series_SubSurface":
            confidence_level = random.choice(confidence_level_list)
        else:
            confidence_level = ""

        broadband_noise_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            broadband_noise_name = "Broadband Noise"
        else:
            broadband_noise_name = ""

        broadband_noise = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            broadband_noise = random.choice(broadband_noise_list)
        else:
            broadband_noise = ""

        subsurface_sensor_name = ""
        if profile == "TOAD_J-Series_SubSurface":
            subsurface_sensor_name = "Subsurface Sensor"
        else:
            subsurface_sensor_name = ""

        subsurface_sensor = ""
        if profile == "TOAD_J-Series_SubSurface":
            subsurface_sensor = random.choice(subsurface_sensor_list)
        else:
            subsurface_sensor = ""

        audio_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            audio_name = "Audio"
        else:
            audio_name = ""

        audio = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            audio = random.choice(audio_list)
        else:
            audio = ""

        sensor_depth_name = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            sensor_depth_name = "Sensor Depth"
        else:
            sensor_depth_name = ""

        sensor_depth = ""
        if trackind == "J5.4 Track(ASW Acoustic Bearing/Range)":
            sensor_depth = random.choice(sensor_depth_list)
        else:
            sensor_depth = ""

        templ = string.Template(track_field_template)
        track_lines.append(templ.substitute(locals()))
        delay_line = delay_line.replace("1", str(delay_secs))
        track_lines.append(delay_line)

        n_tracks_since_last_pause += 1

        # Need to pause here?
        if (
            pause_index < len(pause_intervals)
            and n_tracks_since_last_pause == pause_intervals[pause_index]
        ):
            pauseLine = (
                '<showmessage text="Pausing after %d tracks; click to continue" />'
                % (n_tracks_since_last_pause)
            )
            track_lines.append(pauseLine)
            print("Added pause line:"), pauseLine
            n_tracks_since_last_pause = 0
            pause_index += 1

    # Combine them all into a big block.
    return "\n".join(track_lines)


# import argparse to allow command line arguments to be passed in
parser = argparse.ArgumentParser(description="TacView Scenario Generator")
parser.add_argument(
    "-n",
    "--number_of_tracks",
    default="100",
    type=int,
    action="store",
    help="Number of tracks to generate.",
)
parser.add_argument(
    "-lat",
    "--latitude",
    default="33.0",
    type=float,
    action="store",
    help="Starting latitude. e.g. 33.0",
)
parser.add_argument(
    "-long",
    "--longitude",
    default="-117.0",
    type=float,
    action="store",
    help="Starting longitude. e.g. -117.2",
)
parser.add_argument(
    "-d",
    "--delay",
    default="0",
    type=int,
    action="store",
    help="Number of seconds between tracks. e.g. 1",
)

args = parser.parse_args()

number_of_tracks = args.number_of_tracks

delay = args.delay

start_lat = args.latitude

start_long = args.longitude

string_of_tracks = str(number_of_tracks)


# this part generates the scenario file
def generate_scenario_file(n_tracks, filename, delay_secs, pauses=[]):
    filename = "%d %s Tracks.xml" % (n_tracks, filename)

    track_block = generate_track_code(n_tracks, delay_secs, pauses)
    main_body = open("scenario_track_template.xml").read()
    main_templ = string.Template(main_body)
    final_text = main_templ.substitute(locals())
    open(filename, "w").write(final_text)


# pause after every x tracks
pauses = [500]

# generate_scenario_file(number of tracks, "File Name", delay in seconds between each track, pauses after x tracks)
# generate_scenario_file(1000, "TacView Air", 0, pauses)
# generate_scenario_file(1000, "TacView Air", random.randint(0, 10), pauses)
generate_scenario_file(number_of_tracks, "TacView Air", delay)


# this removes the lines that are not needed in the scenario file
f = open(string_of_tracks + " TacView Air Tracks.xml", "r")
a = (
    "    <field name='' value=''/>",
    "	<field name='' value=''/>",
    "00000000000",
    "0000000000000",
    "000000000000",
    "999999999",
)
lst = []
for line in f:
    for word in a:
        if word in line:
            line = line.replace(word, "")
    lst.append(line)
f.close()
f = open(string_of_tracks + " TacView Air Tracks.xml", "w")
for line in lst:
    if line.strip():
        f.write(line)
f.close()

print("The scenario with " + string_of_tracks + " tracks has been generated!")


"""
commenting this out for now as it's not needed
        def get_special_code_name(code: int) -> str:
            return (
                f"Special Code {code}"
                if profile
                in (
                    "TOAD_J-Series_Air",
                    "TOAD_J-Series_Surface",
                    "TOAD_J-Series_SubSurface",
                    "TOAD_J-Series_Land",
                    "TOAD_J-Series_Space",
                )
                else ""
            )

        special_code_1_name = get_special_code_name(1)
        special_code_2_name = get_special_code_name(2)
        special_code_3_name = get_special_code_name(3)

        special_code_1 = (
            oct(random.randint(0, 63))[2:]
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
                "TOAD_J-Series_Space",
            )
            else ""
        )

        special_code_2 = (
            oct(random.randint(0, 4095))[2:]
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
                "TOAD_J-Series_Space",
            )
            else ""
        )

        special_code_3 = (
            oct(random.randint(0, 4095))[2:]
            if profile
            in (
                "TOAD_J-Series_Air",
                "TOAD_J-Series_Surface",
                "TOAD_J-Series_SubSurface",
                "TOAD_J-Series_Land",
                "TOAD_J-Series_Space",
            )
            else ""
        )
"""