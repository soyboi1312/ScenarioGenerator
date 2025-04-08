import sys
import string
import random
import argparse

"""  
python 3.x must be installed to run this script.

scenarios generated from this script need to be used with TacView version '10583-TacViewC2_16_X-16.1.0', dated July 2023 or later, otherwise you will more than likely get an error saying the value is not supported. 
 
by default 50 units will be created with the lat long starting at 33.1,-117.1. The first JU will be 50.

to change the number of units, lat/long run the script from the command line with the following arguments: 
-n xxx -lat xx.x -long -xxx.x 
-h will show examples

(e.g.: py c2_unit_generator.py -n 100 -lat 33.3 -long -118.1) """

track_field_template = """
<createtrack name='${name}' profile='TOAD_J-Series_Unit'>
    <field name='Track Number' value='${track_number}'/>
    <field name='Latitude' value='${lat}'/>
    <field name='Longitude' value='${lon}'/>
    <field name='${course_name}' value='${course}'/>
    <field name='Track Type' value='Unit'/>
    <field name='Unit Environ/Category' value='${unit_env}'/>
    <field name='${alt_name}' value='${alt}'/>
    <field name='Platform' value='${platform}'/>
    <field name='Activity' value='${activity}'/>
    <field name='${speed_name}' value='${speed}'/>
    <field name='C2 Ind' value='Yes'/>
    <field name='Indirect Indicator' value='Direct'/>
    <field name='Voice Call Sign' value='${voice_call_sign}'/>
    <field name='Reporting Unit' value='${track_number}'/>
    <field name='Track Label' value='${track_number}'/>
</createtrack>
"""
delay_line = """<wait seconds="1"/>"""

unit_platform = ("Air", "Land Point", "Land Track", "Surface", "Subsurface")

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
    "Nuclear Operations",
    "Biological Operations",
    "Chemical Operations",
    "Aborting Mission",
    "Standoff Operations",
    "Combat Search and Rescue (CSAR)",
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

land_platform = (
    "N.S.",
    "Troop Concentration/Unit",
    "Headquarter Complex",
    "Command/Control/Command and Control Center",
    "Assembly Area",
    "Installation/Facility, Military",
    "Installation/Facility, Civilian",
    "Airfield/Airbase",
    "Port/Harbor Facility",
    "Storage Site",
    "Tactical Position",
    "Fortification",
    "Intersection",
    "Convoy",
    "Combat Vehicle",
    "Combat Support Vehicle",
    "Vehicle, Other",
    "Tank",
    "Train",
    "Remotely Piloted Vehicle/Unmanned Ground Vehicle (UGV)",
    "Mortar",
    "Field Artillery",
    "Air Defense Artillery",
    "Rocket Launcher",
    "Missile Launcher",
    "Special Weapon",
    "Bridge",
    "Building/Structure",
    "Power Facility",
    "Rail Facility",
    "(ICBS) EOC Gateway",
    "Navaid Site",
    "Communication Site",
    "Radar Site",
    "Antenna/Emitter",
    "Electronic Warfare Site",
    "Surveillance Site",
    "Bridging Equipment",
    "Mine Warfare Equipment",
    "Surface-to-Air Missile (SAM) Site",
    "Maritime Headquarters",
    "Air Support Radar Team (ASRT)",
    "Direct Air Support Center (DASC)",
    "Forward Air Control Party (FACP)/Tactical Air Control Party (TACP)",
    "Tactical Operations Center (TOC)",
    "Tactical Data System (TDS)",
    "Decoy",
    "Tracked Vehicle",
    "Terminal High Altitude Area Defense (THAAD)",
    "Joint Tactical Ground Station (JTAGS)",
    "Armor Unit",
    "Cavalry Unit",
    "Engineer Unit",
    "Airborne Unit",
    "Aviation Unit",
    "Air Defense Site",
    "Ballistic Missile Defense Site",
    "Special Operations Unit",
    "Air Support Operations Center (ASOC)",
    "Infrared Decoy",
    "Active Electronic Decoy",
)

land_activity_type = (
    "N.S.",
    "Holding",
    "Delaying",
    "Moving",
    "Detecting",
    "Acquiring",
    "Engaging",
    "Advancing",
    "Antiair Attack",
    "Amphibious Assault",
    "Firing",
    "Conventional Attack/Assault",
    "Special Weapons Attack",
    "Demolition",
    "Over The Horizon Targeting",
    "Transiting",
    "Return To Base",
    "Deploying",
    "Emission Control (EMCON)",
    "River Crossing",
    "Loading",
    "Towing",
    "Building Fortification/Barrier",
    "Clearing Barrier",
    "Recovering Equipment",
    "Mine Sweeping",
    "Mine Laying",
    "Jamming",
    "Reconnaissance/Patrolling",
    "Search And Rescue (SAR)",
    "Training",
    "Medical Evacuation (MEDEVAC)",
    "Escorting",
    "Transporting",
    "Screening",
    "Supporting",
    "Repairing",
    "Refueling",
    "Neutralizing",
    "Targeting",
    "Bypassing",
    "Closing",
    "Concentrating",
    "Defending",
    "Disengaging",
    "Infiltrating",
    "Interdicting",
    "Landing",
    "Occupying",
    "Dispersing",
    "Supply/Resupply",
    "Retrograde/Withdrawing",
    "Transmitting",
    "Electronic Warfare Support (ES)",
    "Electronic Attack (EA)",
    "Moving Equipment",
    "Powering Up And Manned, Not Emitting",
    "Preparing For Launch",
    "Site Shutting Down To Unpowered Status",
    "Launching",
    "Fire Support",
    "Special Operations",
    "Nuclear, Biological, Chemical (NBC) Operations",
    "Nuclear Operations",
    "Biological Operations",
    "Chemical Operations",
    "Combat Search and Rescue (CSAR)",
    "Air Breathing Threat Mode",
    "Tactical Ballistic Missile/Air Breathing Threat Mode",
    "Cruise Missile/Air Breathing Threat/Tactical Ballistic Missile Mode",
    "Cruise Missile/Air Breathing Threat Mode",
    "Tactical Ballistic Missile Mode",
    "Air Picture Provision",
    "UAV Operations",
    "Land Activity 1",
    "Land Activity 2",
    "Land Activity 3",
    "Land Activity 4",
    "Land Activity 5",
    "Land Activity 6",
    "Land Activity 7",
    "Land Activity 8",
    "Land Activity 9",
    "Land Activity 10",
    "Land Activity 11",
    "Land Activity 12",
)

surface_platform = (
    "N.S.",
    "Aircraft Carrier",
    "Battleship",
    "Cruiser",
    "Destroyer",
    "Frigate",
    "Fast Patrol Boat",
    "Amphibious",
    "LHA/LHD",
    "Amphibious Assault Command Ship (LCC)",
    "Landing Craft (LC)",
    "Troop Ship",
    "Tanker/Oiler",
    "Auxiliary Ship",
    "Mine Warfare Ship",
    "Mine Countermeasures Maritime Vessel (MCMV)",
    "Hospital Ship",
    "Surfaced Submarine",
    "Hydrofoil",
    "Air Cushion Vehicle",
    "Intelligence Collector",
    "Survey Vessel",
    "Non-Military",
    "Landing Platform",
    "Landing Ship",
    "Command",
    "Ocean Research",
    "Patrol",
    "Support",
    "Fishing Vessel",
    "Merchant Vessel",
    "Patrol Craft Escort",
    "Amphibious General Assault",
    "Missile Control Unit",
    "Decoy",
    "Infrared Decoy",
    "Chaff Decoy",
    "Active Electronic Decoy",
    "Corvette",
    "Littoral Combat Ship",
    "RESET TO NO STATEMENT",
)

surface_activity_type = (
    "N.S.",
    "Air Warfare Support",
    "Over the Horizon Targeting (OTHT)",
    "Training",
    "Logistics Support",
    "Antisurface Warfare",
    "Electronic Warfare (EW)",
    "Fishery Protection",
    "Search and Rescue (SAR)",
    "Escorting",
    "Minelaying",
    "Transiting",
    "Naval Surface Fire Support",
    "Intruding",
    "Amphibious Warfare",
    "Intelligence Collecting",
    "Patrol",
    "Transport",
    "Antisubmarine Warfare (ASW)",
    "Towing",
    "Special Warfare",
    "Strike Warfare",
    "Antiair Warfare",
    "Fishing",
    "Picketing",
    "Mine Countermeasures",
    "Mine Warfare",
    "Marking",
    "Noncombatant Operations",
    "Underway Replenishment",
    "Surveying",
    "Electronic Warfare Support (ES)",
    "Electronic Attack (EA)",
    "Flight Operations",
    "Video Data Linking (Targeting)",
    "Plane Guard",
    "Rescue Ship/Lifeguard",
    "Special Operations",
    "Shadowing",
    "Intervening",
    "Nuclear, Biological, Chemical (NBC) Operations",
    "Nuclear Operations",
    "Biological Operations",
    "Chemical Operations",
    "Electronic Protection (EP)",
    "Combat Search and Rescue (CSAR)",
    "BMD Mission",
    "Return To Base (RTB)",
    "Surface Activity 1",
    "Surface Activity 2",
    "Surface Activity 3",
    "Surface Activity 4",
    "Surface Activity 5",
    "Surface Activity 6",
    "Surface Activity 7",
    "Surface Activity 8",
    "Surface Activity 9",
    "Surface Activity 10",
    "Surface Activity 11",
    "Surface Activity 12",
    "RESET TO NO STATEMENT",
)

subsurface_platform = (
    "N.S.",
    "Submarine Propulsion Unknown",
    "Diesel Electric Submarine General",
    "Diesel Electric Attack Submarine",
    "Diesel Electric Missile Submarine",
    "Diesel Electric Ballistic Missile Submarine",
    "Type 1 Diesel",
    "Type 3 Diesel",
    "Nuclear Submarine General",
    "Nuclear Attack Submarine",
    "Nuclear Missile Submarine",
    "Nuclear Ballistic Missile Submarine",
    "Type II Nuclear",
    "Type III Nuclear",
    "Non-Submarine",
    "Surface Vessel",
    "Torpedo",
    "Mine",
    "Decoy",
    "Wreck",
    "Seabed Pipeline",
    "Fish/Marine Life",
    "Swimmer/Frogman",
    "Knuckle/Wake",
    "Attack Submarine",
    "Cruise Missile Launcher",
    "Pinnacle/Seamountain",
    "Non-Military Submersible",
    "Type VI Nuclear",
    "Type VII Nuclear",
    "Conventional (Command and Control)",
    "Conventional (Auxiliary)",
    "Nuclear (Command and Control)",
    "Infrared Decoy",
    "Chaff Decoy",
    "Active Electronic Decoy",
    "Type 4 Diesel",
    "Missile Control Unit",
    "RESET TO NO STATEMENT",
)

subsurface_activity_type = (
    "N.S.",
    "Reconnaissance",
    "Over The Horizon Targeting (OTHT)",
    "Training",
    "Diving",
    "Antisurface Warfare",
    "Electronic Warfare (EW)",
    "Surveillance",
    "Search And Rescue (SAR)",
    "Escorting",
    "Minelaying",
    "Transiting",
    "Special Weapons Attack",
    "Surfacing",
    "Amphibious Warfare",
    "Intelligence Collecting",
    "Patrol",
    "Transport",
    "Antisubmarine Warfare (ASW)",
    "Bottoming",
    "Special Warfare",
    "Strike Warfare",
    "Clandestine Operations",
    "Snorkeling",
    "Conventional Attack",
    "Mine Countermeasures",
    "Mine Warfare",
    "Marking",
    "Noncombatant Operations",
    "Direct Support",
    "Video Data Linking (Targeting)",
    "Special Operations",
    "Shadowing",
    "Intervening",
    "Nuclear, Biological, Chemical (NBC) Operations",
    "Nuclear Operations",
    "Biological Operations",
    "Chemical Operations",
    "Electronic Warfare Support (ES)",
    "Combat Search and Rescue (CSAR)",
    "Return to Base (RTB)",
    "Subsurface Activity 1",
    "Subsurface Activity 2",
    "Subsurface Activity 3",
    "Subsurface Activity 4",
    "Subsurface Activity 5",
    "Subsurface Activity 6",
    "Subsurface Activity 7",
    "Subsurface Activity 8",
    "Subsurface Activity 9",
    "Subsurface Activity 10",
    "Subsurface Activity 11",
    "Subsurface Activity 12",
    "RESET TO NO STATEMENT",
)

call_sign_list = (
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


def generate_track_code(n_tracks, delay_secs, pause_intervals=[]):
    global delay_line

    track_lines = []
    # Iterate through each track.
    # Make the name and get the parameters.
    # Add to list.

    line_length = 100
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
            long_offset += 0.1
            lat_offset += 0.5

        track_number = oct(40 + i)[2:]
        name = track_number
        profile = "TOAD_J-Series_Unit"
        unit_env = random.choice(unit_platform)

        course_name = ""
        if unit_env == "Land Point":
            course_name = ""
        else:
            course_name = "True Course"

        course = ""
        if unit_env == "Land Point":
            course = ""
        else:
            course = random.randint(0, 359)

        speed_name = ""
        if unit_env == "Land Point":
            speed_name = ""
        else:
            speed_name = "Speed"

        speed = ""
        if unit_env == "Land Point":
            speed = ""
        else:
            speed = random.randint(0, 4092)

        alt_name = ""
        if unit_env == "Surface":
            alt_name = ""
        else:
            alt_name = "Altitude"

        alt = ""
        if unit_env == "Air":
            alt = random.randint(0, 204750)
        elif unit_env == "Land Point" or unit_env == "Land Track":
            alt = random.randint(0, 51150)
        elif unit_env == "Surface":
            alt = ""
        elif unit_env == "Subsurface":
            alt = random.randint(0, 6200)
        else:
            alt = ""

        platform = ""
        if unit_env == "Air":
            platform = random.choice(air_platform)
        elif unit_env == "Land Point" or unit_env == "Land Track":
            platform = random.choice(land_platform)
        elif unit_env == "Surface":
            platform = random.choice(surface_platform)
        elif unit_env == "Subsurface":
            platform = random.choice(subsurface_platform)
        else:
            platform = ""

        activity = ""
        if unit_env == "Air":
            activity = random.choice(air_activity_type)
        elif unit_env == "Land Point" or unit_env == "Land Track":
            activity = random.choice(land_activity_type)
        elif unit_env == "Surface":
            activity = random.choice(surface_activity_type)
        elif unit_env == "Subsurface":
            activity = random.choice(subsurface_activity_type)
        else:
            activity_ = ""

        voice_call_sign = random.choice(call_sign_list)

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
    default="50",
    type=int,
    action="store",
    help="Number of tracks to generate.",
)
parser.add_argument(
    "-lat",
    "--latitude",
    default="33.1",
    type=float,
    action="store",
    help="Starting latitude. e.g. 32.1",
)
parser.add_argument(
    "-long",
    "--longitude",
    default="-117.1",
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


def generate_scenario_file(n_tracks, filename, delay_secs, pauses=[]):
    filename = "%d %s Units.xml" % (n_tracks, filename)

    track_block = generate_track_code(n_tracks, delay_secs, pauses)
    main_body = open("scenario_track_template.xml").read()
    main_templ = string.Template(main_body)
    final_text = main_templ.substitute(locals())
    open(filename, "w").write(final_text)


# pause after every x tracks
pauses = [500]

# generate_scenario_file(number of tracks, "File Name", delay in seconds between each track, pauses after x tracks)
# generate_scenario_file(100, "TacView ", 0, pauses)
# generate_scenario_file(100, "TacView ", random.randint(0, 10), pauses)
generate_scenario_file(number_of_tracks, "TacView", delay)

f = open(string_of_tracks + " TacView Units.xml", "r")
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
f = open(string_of_tracks + " TacView Units.xml", "w")
for line in lst:
    f.write(line)
f.close()

print("The scenario with " + string_of_tracks + " C2 units has been generated!")
