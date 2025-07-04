<script lang="ts">
    import maplibregl from 'maplibre-gl';
    import 'maplibre-gl/dist/maplibre-gl.css';
    import { onMount } from 'svelte';
    import { setPlatforms } from '$lib/stores/platforms';
    import { setRoutes } from '$lib/stores/routes';
    import { results } from '$lib/stores/results';
    import { get } from 'svelte/store';
    import type { Route } from '$lib/types/Route';
    import type { Area } from '$lib/types/Area';
    import type { Stop } from '$lib/types/Stop';
    import type { Via } from '$lib/types/Via';

    const MAJESTIC_CENTER: maplibregl.LngLatLike = [77.5707, 12.9784]; // [lng, lat]

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
        console.log(resultRouteIds);
        console.log(currentResults);
        // Clone the geojson
        const updated = JSON.parse(JSON.stringify(platformsGeoJson));
        for (const feature of updated.features) {
            // Store original color
            if (!feature.properties.OriginalColor) {
                feature.properties.OriginalColor = feature.properties.Color;
            }
            const platformRoutes = (feature.properties && Array.isArray(feature.properties.Routes)) ? feature.properties.Routes : [];
            let hasMatch = true;
            hasMatch = !platformRoutes.some((route) => Object.hasOwn(route, 'Route') && resultRouteIds.has(route.Route));
            feature.properties.Color = hasMatch ? '#D2D2D2' : feature.properties.OriginalColor || feature.properties.Color;
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
            zoom: 17
        });
        // Subscribe to results and update platform colors on change
        const unsub = results.subscribe(() => {
            if (map && platformsGeoJson) {
                updatePlatformColors();
            } else {
                console.log("SFDSAF");
            }
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
                    platformsGeoJson = data;
                    // Store platforms
                    const platformsArr = data.features || [];
                    setPlatforms(platformsArr);

                    // Flatten all routes from all platforms, convert to Route types
                    const allRoutes: Route[] = [];
                    for (const platform of platformsArr) {
                        if (platform.properties && Array.isArray(platform.properties.Routes)) {
                            for (const route of platform.properties.Routes) {
                                // Convert stops
                                const stops: Stop[] = (route.Stops || []).map((s: any) => ({
                                    name: s,
                                    nameKannada: ""
                                }));
                                // Convert via
                                const via: Via = {
                                    name: route.Via,
                                    nameKannada: route.KannadaVia
                                };
                                // Convert area
                                const area: Area = {
                                    name: route.Area,
                                    nameKannada: route.KannadaArea
                                }
                                allRoutes.push({
                                    number: route.Route,
                                    area,
                                    stops,
                                    via,
                                    destination: route.Destination,
                                    kannadaDestination: route.KannadaDestination,
                                    platformNumber: route.PlatformNumber
                                });
                            }
                        }
                    }
                    setRoutes(allRoutes);

                    map.addSource('platforms', {
                        type: 'geojson',
                        data
                    });
                    map.addLayer({
                        id: 'platform-circles',
                        type: 'circle',
                        source: 'platforms',
                        paint: {
                            'circle-radius': 16,
                            'circle-color': [
                                'coalesce',
                                ['get', 'Color'],
                                '#FFFFFF'
                            ]
                        }
                    });
                    map.addLayer({
                        id: 'platform-labels',
                        type: 'symbol',
                        source: 'platforms',
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
</style>