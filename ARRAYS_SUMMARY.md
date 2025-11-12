# Extracted Arrays Summary

Successfully extracted all 49 data arrays from `all_track_generator.py`

## Files Created

1. **all_extracted_arrays.json** - Complete JSON file with all arrays
2. **extracted_arrays.js** - JavaScript/ES6 module with exported arrays
3. **ARRAYS_SUMMARY.md** - This summary document

## Array Statistics

| Array Name | Number of Items |
|------------|----------------|
| air_platform | 54 |
| air_activity_type | 95 |
| air_specific_type | 1,067 |
| callsign_list | 112 |
| ew_environment | 5 |
| ew_ind_name | 3 |
| land_platform | 61 |
| land_activity_type | 86 |
| land_specific_type | 388 |
| reference_track_point_name | 9 |
| emergency_amp | 9 |
| reference_amp | 10 |
| general_station_amp | 6 |
| air_station_amp | 13 |
| general_area_amp | 8 |
| hazard_area_amp | 10 |
| asw_amp | 11 |
| asw1_amp | 4 |
| hazard_amp | 7 |
| track_ind_name | 2 |
| tracktype35 | 2 |
| space_platform | 16 |
| space_specific_type | 555 |
| space_activity_type | 41 |
| space_amp | 24 |
| space_boost_indicator | 2 |
| space_lost | 2 |
| subsurface_platform | 38 |
| subsurface_activity_type | 53 |
| subsurface_specific_type | 137 |
| doppler_type_list | 4 |
| sound_prop_list | 9 |
| sensor_depth_list | 3 |
| audio_list | 2 |
| broadband_noise_list | 2 |
| subsurface_sensor_list | 28 |
| confidence_level_list | 10 |
| depth_contact_list | 8 |
| surface_platform | 40 |
| surface_activity_type | 60 |
| surface_specific_type | 1,220 |
| spitype | 2 |
| strength | 16 |
| track_identity | 7 |
| mode_1_options | 32 |
| mode_3_options | 61 |
| mode_4_indicator | 4 |
| mode_5_indicator | 3 |
| mode_5_nationality | 69 |

**Total: 4,357 data items across 49 arrays**

## Usage Examples

### JavaScript/Node.js
```javascript
import { air_platform, callsign_list, track_identity } from './extracted_arrays.js';

console.log(air_platform[0]); // "N.S."
console.log(callsign_list.length); // 112
```

### JSON
```javascript
const data = require('./all_extracted_arrays.json');
console.log(data.air_platform);
console.log(data.surface_specific_type);
```

## Notes

- All arrays maintain their original order from the Python file
- "N.S." typically stands for "No Statement" or "Not Specified"
- Some arrays contain mixed types (strings and numbers, particularly mode_1_options and mode_3_options)
- The data is suitable for dropdown menus, validation, or data generation in web applications

## Source

Original file: `/home/user/ScenarioGenerator/all_track_generator.py`
Extraction date: 2025-11-12
