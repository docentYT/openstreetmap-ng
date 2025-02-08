import type { AppTheme } from "./_navbar-theme"
import { getDeviceThemePreference, getUnixTimestamp, isLatitude, isLongitude, isZoom } from "./_utils"
import type { MapState } from "./leaflet/_map-utils"

const mapStateVersion = 1

/**
 * Get app theme from local storage
 * @example
 * getAppTheme()
 * // => "auto"
 */
export const getAppTheme = (): AppTheme => (localStorage.getItem("theme") || "auto") as AppTheme

/** Get the active app theme, resolving "auto" if necessary */
export const getActiveTheme = (): "light" | "dark" => {
    const appTheme = getAppTheme()
    return appTheme === "auto" ? getDeviceThemePreference() : appTheme
}

/** Set app theme to local storage */
export const setAppTheme = (theme: AppTheme): void => {
    console.debug("setAppTheme", theme)
    localStorage.setItem("theme", theme)
}

/**
 * Get last map state from local storage
 * @example
 * getLastMapState()
 * // => { lon: 16.3725, lat: 48.208889, zoom: 12, layersCode: "K" }
 */
export const getLastMapState = (): MapState | null => {
    const lastMapState = localStorage.getItem("lastMapState")
    if (!lastMapState) return null
    const { version, lon, lat, zoom, layersCode } = JSON.parse(lastMapState)
    if (version === mapStateVersion && isLongitude(lon) && isLatitude(lat) && isZoom(zoom)) {
        return { lon, lat, zoom, layersCode }
    }
    return null
}

/**
 * Set last map state to local storage
 * @example
 * setLastMapState({ lon: 16.3725, lat: 48.208889, zoom: 12, layersCode: "K" })
 */
export const setLastMapState = (state: MapState): void => {
    const { lon, lat, zoom, layersCode } = state
    localStorage.setItem(
        "lastMapState",
        JSON.stringify({
            version: mapStateVersion,
            lon,
            lat,
            zoom,
            layersCode,
        }),
    )
}

/**
 * Check whether user has hidden a banner
 * @example
 * isBannerHidden("welcome")
 */
export const isBannerHidden = (name: string): boolean => localStorage.getItem(`bannerHidden-${name}`) !== null

/** Mark a banner as hidden in local storage */
export const markBannerHidden = (name: string): void => {
    console.debug("markBannerHidden", name)
    localStorage.setItem(`bannerHidden-${name}`, getUnixTimestamp().toString())
}

/** Get access token for system app from local storage */
export const getSystemAppAccessToken = (clientId: string): string | null =>
    localStorage.getItem(`systemAppAccessToken-${clientId}`)

/** Set access token for system app to local storage */
export const setSystemAppAccessToken = (clientId: string, accessToken: string): void =>
    localStorage.setItem(`systemAppAccessToken-${clientId}`, accessToken)

/**
 * Get last routing engine from local storage
 * @example
 * getLastRoutingEngine()
 * // => "graphhopper_car"
 */
export const getLastRoutingEngine = (): string | null => localStorage.getItem("routingEngine")

/**
 * Set last routing engine to local storage
 * @example
 * setLastRoutingEngine("graphhopper_car")
 */
export const setLastRoutingEngine = (engine: string): void => {
    console.debug("setLastRoutingEngine", engine)
    localStorage.setItem("routingEngine", engine)
}

/** Get overlay opacity from local storage, in the range [0, 1] */
export const getMapOverlayOpacity = (name: string): number => {
    const opacity = localStorage.getItem(`overlayOpacity-${name}`)
    const defaultOpacity = 0.55
    return opacity ? Number.parseFloat(opacity) : defaultOpacity
}

/** Set overlay opacity to local storage, in the range [0, 1] */
export const setMapOverlayOpacity = (name: string, opacity: number): void => {
    localStorage.setItem(`overlayOpacity-${name}`, opacity.toString())
}

/** Get last selected export format from local storage */
export const getLastShareExportFormat = (): string => localStorage.getItem("shareExportFormat") ?? "image/jpeg"

/** Set last selected export format to local storage */
export const setLastShareExportFormat = (format: string): void => {
    console.debug("setLastShareExportFormat", format)
    localStorage.setItem("shareExportFormat", format)
}

/** Get tags diff mode state from local storage */
export const getTagsDiffMode = (): boolean => (localStorage.getItem("tagsDiffMode") || "true") === "true"

/** Set tags diff mode to local storage */
export const setTagsDiffMode = (state: boolean): void => {
    console.debug("setTagsDiffMode", state)
    localStorage.setItem("tagsDiffMode", state.toString())
}

/** Get last timezone update timestamp */
export const getLastTimezoneUpdateTime = (): number | null => {
    const time = localStorage.getItem("timezoneUpdateTime")
    return time ? Number.parseInt(time) : null
}

/** Set last timezone update timestamp to current time */
export const setLastTimezoneUpdateTime = (time: number): void => {
    console.debug("setLastTimezoneUpdateTime", time)
    localStorage.setItem("timezoneUpdateTime", time.toString())
}
