# Majestic
### Platform, route / bus, stop web-app for the majestic bus stand
A mobile-friendly single-page PWA that facilitates easy navigation of the Kempegowda Bus Stand (Majestic): https://majestic.bengawalk.com

#### Setup

- To set up the project, for development or otherwise, first run `yarn install`
- Once the packages have been installed, `yarn dev` will run the applet locally, while `yarn build` will create a build folder.

#### Data

All input data is stored in `input/`.

- `platforms-majestic.geojson`: Platform coordinates
- `platform-index.csv`: Platform <-> Route mappings
- `bus-stops.csv`: Stops of a route
- `bus-stops-kn.csv`: Stop <-> Stop name in Kannada

Python scripts to process the data are stored in the root project folder.

- `generate-geojson.py`: Takes all available data in `input/` to create `platform-routes-majestic.geojson` (used by applet for all data)
- `generate-bus-stops-kn.py`: Takes all available unique stops in bus-stops.csv, and uses varnam's transliteration API to generate bus-stops-kn.csv

The final output file is `static/data/platforms-routes-majestic.geojson`. This is available on the build under `data/platforms-routes-majestic.geojson`.
This output file is used by the applet to read platform, route / bus, and stop information.

##### AI Disclaimer: Certain project components have been created or modified by generative AI.