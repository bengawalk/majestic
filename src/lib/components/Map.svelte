<script lang="ts">
    import maplibregl from 'maplibre-gl';
    import 'maplibre-gl/dist/maplibre-gl.css';
    import {onMount, tick} from 'svelte';
    import { setPlatforms } from '$lib/stores/platforms';
    import { setRoutes } from '$lib/stores/routes';
    import {results, setResults} from '$lib/stores/results';
    import { get } from 'svelte/store';
    import { Platform } from '$lib/types/Platform';
    import {previousSelectedItem, selectedItem} from '$lib/stores/selectedItem';

    const MAJESTIC_CENTER: maplibregl.LngLatLike = [77.5724549, 12.9772291]; // [lng, lat]

    // // Raster overlay boundaries
    // let overlayBounds = [
    //     [
    //         77.57002448255838,
    //         12.979030212561781
    //     ],
    //     [
    //         77.57465645568396,
    //         12.979030212561781
    //     ],
    //     [
    //         77.57465645568396,
    //         12.977137224193143
    //     ],
    //     [
    //         77.57002448255838,
    //         12.977137224193143
    //     ]
    // ];

    let map: maplibregl.Map | undefined;
    let platformsGeoJson: GeoJSON.FeatureCollection | null = null;

    function updatePlatformColors() {
        if (!map || !platformsGeoJson) return;
        // Use the global search value to determine if a search is active
        const currentResults = get(results);
        const resultRouteIds = new Set(currentResults ? currentResults.map(r => r.number) : []);
        // Clone the geojson
        const updated = JSON.parse(JSON.stringify(platformsGeoJson));
        for (const feature of updated.features) {
            // Store original color
            if (!feature.properties.OriginalColor) {
                feature.properties.OriginalColor = feature.properties.Color;
            }
            const platformRoutes = (feature.properties && Array.isArray(feature.properties.Routes)) ? feature.properties.Routes : [];
            // isGray: true if no route matches
            const isGray = !platformRoutes.some((route) => Object.hasOwn(route, 'Route') && resultRouteIds.has(route.Route));
            feature.properties.isGray = isGray;
            feature.properties.Color = isGray ? '#D2D2D2' : feature.properties.OriginalColor || feature.properties.Color;
        }
        // Update the map source
        if (map.getSource('platforms')) {
            (map.getSource('platforms')! as maplibregl.GeoJSONSource).setData(updated);
        }
    }

    onMount(() => {

        map = new maplibregl.Map({
            container: 'map',
            style: {
                version: 8,
                glyphs: 'glyphs/{fontstack}/{range}.pbf',
                sources: {
                    carto: {
                        type: 'raster',
                        tiles: [
                            'https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
                        ],
                        tileSize: 256,
                        attribution: '© OpenStreetMap contributors, © CartoDB'
                    }
                },
                layers: [
                    {
                        id: 'carto',
                        type: 'raster',
                        source: 'carto'
                    }
                ]
            },
            center: MAJESTIC_CENTER,
            zoom: 16.8,
            dragRotate: false,
            bearing: 0,
            pitch: 0,
            maxPitch: 0,
            minPitch: 0
        });
        // Subscribe to results and update platform colors on change
        const unsub = results.subscribe(() => {
            if (map && platformsGeoJson) {
                updatePlatformColors();
            }
        });
        // Prevent rotation and pitch changes
        map.on('rotate', () => {
            map.setBearing(0);
        });
        
        map.on('pitch', () => {
            map.setPitch(0);
        });
        
        map.on('load', () => {
            // map.addSource('majestic-overlay', {
            //     type: 'image',
            //     url: '/data/majestic-alpha-overlay.png',
            //     coordinates: overlayBounds
            // });
            //
            // map.addLayer({
            //     id: 'majestic-overlay-layer',
            //     type: 'raster',
            //     source: 'majestic-overlay',
            //     paint: {
            //         'raster-opacity': 1
            //     }
            // });

            // Add platforms geojson
            fetch('/data/platforms-routes-majestic.geojson')
                .then(r => r.json())
                .then(data => {
                    if(!map) return;
                    // Set isGray property for all features initially
                    const currentResults = get(results);
                    const resultRouteIds = new Set(currentResults ? currentResults.map(r => r.number) : []);
                    for (const feature of data.features) {
                        const platformRoutes = (feature.properties && Array.isArray(feature.properties.Routes)) ? feature.properties.Routes : [];
                        const isGray = !platformRoutes.some((route) => Object.hasOwn(route, 'Route') && resultRouteIds.has(route.Route));
                        feature.properties.isGray = isGray;
                    }
                    platformsGeoJson = data;
                    // Store platforms as Platform class instances
                    const platformsArr = (data.features || []).map(feature => {
                        const platformNumber = feature.properties?.Platform?.toString().toUpperCase() || '';
                        const color = feature.properties?.Color || '#FFFFFF';
                        const routes = (feature.properties?.Routes || []).map(route => {
                            // Convert stops
                            const stops = (route.Stops || []).map((s) => ({ name: s.name, nameKannada: s.name_kn}));
                            // Convert via
                            const via = { name: route.Via, nameKannada: route.KannadaVia };
                            // Convert area
                            const area = { name: route.Area, nameKannada: route.KannadaArea };
                            return {
                                number: route.Route,
                                area,
                                stops,
                                via,
                                destination: route.Destination,
                                kannadaDestination: route.KannadaDestination,
                                platformNumber: route.PlatformNumber.toUpperCase()
                            };
                        });
                        return new Platform({ platformNumber, color, routes });
                    });
                    setPlatforms(platformsArr);

                    // Flatten all routes from all platforms, convert to Route types
                    const allRoutes = [];
                    for (const platform of platformsArr) {
                        for (const route of platform.routes) {
                            allRoutes.push(route);
                        }
                    }
                    setRoutes(allRoutes);

                    map.addSource('platforms', {
                        type: 'geojson',
                        data
                    });
                    // Add gray platforms layer (bottom)
                    map.addLayer({
                        id: 'platform-circles-gray',
                        type: 'circle',
                        source: 'platforms',
                        filter: ['==', ['get', 'isGray'], true],
                        paint: {
                            'circle-radius': 16,
                            'circle-color': '#D2D2D2'
                        }
                    });
                    // Add gray platform labels (just above gray circles)
                    map.addLayer({
                        id: 'platform-labels-gray',
                        type: 'symbol',
                        source: 'platforms',
                        filter: ['==', ['get', 'isGray'], true],
                        layout: {
                            'text-field': ['get', 'Platform'],
                            'text-size': 16,
                            'text-font': ['Manrope SemiBold'],
                            'text-offset': [0, 0],
                            'text-anchor': 'center',
                            'text-allow-overlap': true
                        },
                        paint: {
                            'text-color': '#fff',
                            'text-halo-width': 0
                        }
                    });
                    // Add colored platforms layer (top)
                    map.addLayer({
                        id: 'platform-circles-colored',
                        type: 'circle',
                        source: 'platforms',
                        filter: ['==', ['get', 'isGray'], false],
                        paint: {
                            'circle-radius': 16,
                            'circle-color': [
                                'coalesce',
                                ['get', 'Color'],
                                '#FFFFFF'
                            ]
                        }
                    });
                    // Add colored platform labels (just above colored circles)
                    map.addLayer({
                        id: 'platform-labels-colored',
                        type: 'symbol',
                        source: 'platforms',
                        filter: ['==', ['get', 'isGray'], false],
                        layout: {
                            'text-field': ['get', 'Platform'],
                            'text-size': 16,
                            'text-font': ['Manrope SemiBold'],
                            'text-offset': [0, 0],
                            'text-anchor': 'center',
                            'text-allow-overlap': true
                        },
                        paint: {
                            'text-color': '#fff',
                            'text-halo-width': 0
                        }
                    });
                    // Remove the original single platform-circles and platform-labels layers if present
                    if (map.getLayer('platform-circles')) {
                        map.removeLayer('platform-circles');
                    }
                    if (map.getLayer('platform-labels')) {
                        map.removeLayer('platform-labels');
                    }

                    // Add click listener for platform features
                    map.on('click', (e) => {
                        const features = map.queryRenderedFeatures(e.point, { layers: ['platform-circles-gray', 'platform-circles-colored'] });
                        if (features && features.length > 0) {
                            const feature = features[0];
                            if (feature && feature.properties && feature.properties.Platform) {
                                selectedItem.set(undefined);
                                previousSelectedItem.set(undefined);
                                tick().then( () => selectedItem.set({ type: 'Platform', display: feature.properties.Platform }) );
                            }
                        }
                    });

                    // Add GeolocateControl to show user location if permission is granted
                    const geolocate = new maplibregl.GeolocateControl({
                        positionOptions: { enableHighAccuracy: true },
                        trackUserLocation: true,
                        showUserHeading: true,
                        showUserLocation: true,
                        showAccuracyCircle: true,
                        fitBoundsOptions: { maxZoom: map.getZoom() }, // Prevent zooming in
                        flyTo: false // Prevent flying to user location
                    });
                    map.addControl(geolocate);
                    setResults(allRoutes);
                    updatePlatformColors();
                    // Hide the geolocate control button via CSS
                    map.once('render', () => {
                        const controls = document.getElementsByClassName('maplibregl-ctrl-geolocate');
                        for (const ctrl of controls) {
                            ctrl.style.display = 'none';
                        }
                    });

                    // Request user location on map load, but do not fly to it
                    if (navigator.geolocation) {
                        navigator.geolocation.getCurrentPosition(
                            (pos) => {
                                // Permission granted, update the geolocate control's marker without flying
                                // This is a workaround: set the control's _lastKnownPosition and emit the event
                                if (geolocate._updateMarker) {
                                    geolocate._updateMarker({ coords: pos.coords });
                                }
                            },
                            () => {
                                // Permission denied or failed, do nothing
                            }
                        );
                    }
                });
        });

        return () => {
            if(map)
                map.remove();
            unsub();
        };
    });

</script>

<div id="map" class="fixed inset-0 w-screen h-screen z-0"></div>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
/* Hide the geolocate control button */
.maplibregl-ctrl-geolocate { display: none !important; }
</style>