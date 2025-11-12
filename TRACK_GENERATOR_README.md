# Track Generator - Web Interface

A single HTML file that converts track profiles to XML scenario files. This replaces the Python script `all_track_generator.py` with a modern web-based interface.

## Files

- **track_generator.html** - Main web application (open in browser)
- **extracted_arrays.js** - Data arrays extracted from the Python script
- **all_extracted_arrays.json** - Complete data in JSON format

## How to Use

### 1. Open the Application

Simply open `track_generator.html` in a modern web browser (Chrome, Firefox, Edge, or Safari).

**Important:** Due to JavaScript module security restrictions, you need to serve the files through a web server. You have several options:

#### Option A: Python HTTP Server (Recommended)
```bash
cd /home/user/ScenarioGenerator
python3 -m http.server 8000
```
Then open: http://localhost:8000/track_generator.html

#### Option B: Node.js HTTP Server
```bash
cd /home/user/ScenarioGenerator
npx http-server -p 8000
```
Then open: http://localhost:8000/track_generator.html

### 2. Select Track Profiles

Choose one or more track profiles:

- **Reference Point** - `TOAD_J-Series_Reference_Point`
- **Air** - `TOAD_J-Series_Air`
- **Land** - `TOAD_J-Series_Land`
- **Surface** - `TOAD_J-Series_Surface`
- **Subsurface** - `TOAD_J-Series_SubSurface`
- **Space** - `TOAD_J-Series_Space`
- **EW** - `TOAD_J-Series_EW`
- **All** - Includes all of the above

### 3. Configure Settings

Adjust the following parameters:

- **Number of Tracks**: How many tracks to generate (default: 100)
- **Starting Latitude**: Initial latitude position (default: 33.0)
- **Starting Longitude**: Initial longitude position (default: -117.0)
- **Delay Between Tracks**: Seconds between each track creation (default: 1)

### 4. Field Selection (Optional)

By default, all relevant fields for the selected profile(s) are included. You can uncheck "Include All Fields" to manually select which fields to include.

### 5. Generate XML

Click the "Generate XML" button to create your scenario file. The XML will be displayed in a text area below.

### 6. Download

Click the "Download XML File" button to save the generated XML to your computer.

## Features

✅ **Profile-Specific Fields**: Each track profile automatically includes its relevant fields
✅ **Random Data Generation**: Realistic random values for all fields
✅ **Field Selection**: Choose exactly which fields to include
✅ **Live Preview**: See the generated XML before downloading
✅ **Multiple Profiles**: Mix different track types in a single scenario
✅ **Clean UI**: Modern, responsive interface with visual feedback

## Profile Field Mappings

### Reference Point
- Basic position and altitude
- Point type and amplification

### Air
- Callsign, position, altitude
- Course, speed, platform, activity
- Mode codes (1-5), IFF data
- Identity and strength

### Land
- Position, elevation
- Land type (Track/Point)
- Course, speed (for tracks)
- Platform, activity, specific type
- Mode codes and identity

### Surface
- Position, course, speed
- Platform, activity, specific type
- Mode codes and identity

### Subsurface
- Position, depth, course, speed
- Track indicators (ASW types)
- Subsurface sensors
- Confidence level, depth contact
- Acoustic bearing data (for J5.4 tracks)

### Space
- Position, altitude, course, speed
- Space amplification
- Boost and lost track indicators
- Time fields (minute, seconds)

### EW (Electronic Warfare)
- Environment category (Air/Land/Surface/Subsurface/Space)
- Track indicators
- Platform and activity based on environment
- Dynamic field population

## Technical Details

### Data Arrays
All data arrays from the original Python script have been extracted and converted to JavaScript:
- 49 arrays total
- 4,357 individual data items
- Includes platforms, activities, specific types, mode codes, etc.

### XML Structure
The generated XML follows the TacView scenario format:
- Profile definitions with update intervals
- Track creation blocks with field data
- Wait intervals between tracks
- Compatible with TacView version 10583-TacViewC2_16_X-16.1.0 or later

### Browser Compatibility
- **Required**: Modern browser with ES6 module support
- **Tested**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Not Supported**: Internet Explorer

## Differences from Python Script

The web interface provides the same core functionality as `all_track_generator.py` with these improvements:

✅ No Python installation required
✅ Interactive UI with real-time feedback
✅ Visual profile and field selection
✅ Instant preview of generated XML
✅ Works on any device with a modern browser
✅ No command-line knowledge needed

## Troubleshooting

### "Failed to load module" Error
Make sure you're accessing the HTML file through a web server (see "How to Use" section above). You cannot open the file directly with `file://` protocol due to browser security restrictions.

### Empty or Missing Data
Ensure that `extracted_arrays.js` is in the same directory as `track_generator.html`.

### Browser Console Errors
Check that you're using a modern browser with JavaScript enabled. Open the browser console (F12) to see specific error messages.

## License

This tool is based on the original `all_track_generator.py` script and maintains compatibility with TacView scenario formats.
