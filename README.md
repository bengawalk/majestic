# Majestic
### Platform, route / bus, stop web-app for the majestic bus stand
A mobile-friendly single-page PWA that facilitates easy navigation of the Kempegowda Bus Stand (Majestic): https://majestic.bmtc.co.in

#### Setup

- To set up the project, for development or otherwise, first run `yarn install`
- Once the packages have been installed, `yarn dev` will run the applet locally, while `yarn build` will create a build folder.

#### Translations

Translation strings for data elements are provided with the data, while other translations are stored in `messages/`. 
Translation related settings (e.g default locale) are stored in `project.inlang/settings.json`.

#### Data

All input data is stored in `input/`:

- `platforms-majestic.geojson`: Platform coordinates
- `platform-index.csv`: Platform <-> Route mappings
- `bus-stops.csv`: Stops of a route in English
- `bus-stops-kn.csv`: Stop in English <-> Stop in Kannada

Python scripts to process the data are stored in the root project folder.

- `generate-geojson.py`: Takes all available data in `input/` to create `platform-routes-majestic.geojson` (used by applet for all data)
- `update-platform-index.py`: Reads a temporary bus-stops-pf.csv with platform information and modifies existing platform values to the new ones.
- `generate-bus-stops-kn.py`: Takes all available unique stops in bus-stops.csv, and uses varnam's transliteration API to generate bus-stops-kn.csv (not used as we now receive a bus-stops-kn.csv)

The final output file is `static/data/platforms-routes-majestic.geojson`. This is available on the build under `data/platforms-routes-majestic.geojson`.
This output file is used by the applet to read platform, route / bus, and stop information.

##### AI Disclaimer: Certain project components have been created or modified by generative AI.