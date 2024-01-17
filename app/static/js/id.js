import { coreContext } from "iD"
import { apiUrl, primaryLanguage } from "./_params.js"
import { throttle } from "./_utils.js"

const idContainer = document.querySelector(".id-container")
if (idContainer) {
    const params = idContainer.dataset

    // Create and configure app context
    const ctx = coreContext()
    ctx.connection().apiConnections([])
    ctx.preauth({
        url: parent.location.origin,
        apiUrl: apiUrl,
        // biome-ignore lint/style/useNamingConvention: Not controlled by this project
        client_id: params.clientId,
        // biome-ignore lint/style/useNamingConvention: Not controlled by this project
        client_secret: params.clientSecret,
        // biome-ignore lint/style/useNamingConvention: Not controlled by this project
        access_token: params.accessToken,
    })

    const id = ctx
        .embed(true)
        .assetPath(`static-id/${params.version}/`)
        .locale(primaryLanguage)
        .containerNode(idContainer)
        .init()

    const map = id.map()

    // On map move, send the new state to the parent
    // TODO: isn't there moveend event?
    map.addEventListener(
        "move.embed",
        throttle(() => {
            // Skip if in intro
            if (id.inIntro()) return

            const [lon, lat] = map.center()
            const zoom = map.zoom()
            parent.postMessage({ type: "mapState", source: "id", state: { lon, lat, zoom } }, "*")
        }, 250),
    )
}