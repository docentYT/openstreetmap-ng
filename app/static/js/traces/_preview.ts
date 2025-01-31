import type { LineString } from "geojson"
import { type GeoJSONSource, LngLatBounds, Map as MaplibreMap, ScaleControl } from "maplibre-gl"
import { isMetricUnit } from "../_intl.ts"
import { decodeLonLat } from "../_polyline.ts"
import { requestAnimationFramePolyfill } from "../_utils"
import { CustomGeolocateControl } from "../leaflet/_geolocate"
import {
    type LayerId,
    addMapLayer,
    addMapLayerSources,
    defaultLayerId,
    emptyFeatureCollection,
    layersConfig,
} from "../leaflet/_layers"
import { addControlGroup } from "../leaflet/_map-utils"
import { configureDefaultMapBehavior, padLngLatBounds } from "../leaflet/_utils"
import { CustomZoomControl } from "../leaflet/_zoom"
import { CustomGlobeControl } from "../leaflet/_globe.ts"

const tracePreviewContainer = document.querySelector("div.trace-preview")
if (tracePreviewContainer) {
    console.debug("Initializing trace preview map")

    const baseLayerId = "trace-preview" as LayerId
    layersConfig.set(baseLayerId as LayerId, {
        specification: {
            type: "geojson",
            data: emptyFeatureCollection,
        },
        layerTypes: ["line"],
        layerOptions: {
            layout: {
                "line-join": "round",
                "line-cap": "round",
            },
            paint: {
                "line-color": "#f60",
                "line-width": 4.5,
            },
        },
    })
    const antLayerId = "trace-preview-ant" as LayerId
    layersConfig.set(antLayerId as LayerId, {
        specification: {
            type: "geojson",
            data: emptyFeatureCollection,
        },
        layerTypes: ["line"],
        layerOptions: {
            layout: {
                "line-join": "round",
                // buggy with line-dasharray: "line-cap": "round",
            },
            paint: {
                "line-color": "#220",
                "line-width": 4.5,
            },
        },
    })

    const map = new MaplibreMap({
        container: tracePreviewContainer,
        minZoom: 0,
        maxZoom: 19,
        attributionControl: { compact: true, customAttribution: "" },
        refreshExpiredTiles: false,
    })
    configureDefaultMapBehavior(map)
    addMapLayerSources(map, "all")

    const isSmall = tracePreviewContainer.classList.contains("trace-preview-sm")
    if (!isSmall) {
        map.addControl(
            new ScaleControl({
                unit: isMetricUnit() ? "metric" : "imperial",
            }),
        )
        addControlGroup(map, [new CustomZoomControl(), new CustomGeolocateControl(), new CustomGlobeControl()])
    } else {
        addControlGroup(map, [new CustomZoomControl()])
    }

    addMapLayer(map, defaultLayerId)
    addMapLayer(map, baseLayerId)
    addMapLayer(map, antLayerId)

    // Add trace path
    const coordinates = decodeLonLat(tracePreviewContainer.dataset.line, 6)
    const bounds = coordinates.reduce((bounds, coord) => bounds.extend(coord), new LngLatBounds())
    map.fitBounds(padLngLatBounds(bounds, 0.3), { animate: false })

    const geometry: LineString = {
        type: "LineString",
        coordinates,
    }
    ;(map.getSource(baseLayerId) as GeoJSONSource).setData(geometry)
    ;(map.getSource(antLayerId) as GeoJSONSource).setData(geometry)

    const duration = 2000
    const dashA = 4
    const dashB = 3
    const totalLength = dashA + dashB
    let lastOffset = -1

    const antPath = (timestamp?: DOMHighResTimeStamp) => {
        const progress = ((timestamp ?? performance.now()) % duration) / duration
        const offset = Math.round(progress * totalLength * 10) / 10
        if (offset !== lastOffset) {
            lastOffset = offset
            // https://docs.mapbox.com/mapbox-gl-js/example/animate-ant-path/
            const dashPattern: number[] =
                offset <= dashB //
                    ? [offset, dashA, dashB - offset]
                    : [0, offset - dashB, dashB, totalLength - offset]
            map.setPaintProperty(antLayerId, "line-dasharray", dashPattern)
        }
        requestAnimationFramePolyfill(antPath)
    }
    requestAnimationFramePolyfill(antPath)
}
