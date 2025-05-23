/**
 * Parse a query string into an object
 * @example
 * qsParse("?foo=bar&baz=qux")
 * // => { foo: "bar", baz: "qux" }
 */
export const qsParse = (qs: string): { [key: string]: string } => {
    const result: { [key: string]: string } = {}
    if (!qs) return result
    if (qs.startsWith("#")) qs = qs.substring(1)
    const params = new URLSearchParams(qs)
    for (const key of params.keys()) {
        if (result[key] === undefined) {
            result[key] = params.getAll(key).join(";")
        }
    }
    return result
}

/**
 * Encode an object into a URLSearchParams object
 * @example
 * qsEncode({ foo: "bar", baz: "qux", quux: undefined })
 * // => URLSearchParams { "foo" => "bar", "baz" => "qux" }
 */
export const qsEncode = (obj: {
    [key: string]: string | string[] | undefined
}): URLSearchParams => {
    const params = new URLSearchParams()
    for (const [key, value] of Object.entries(obj)) {
        // Skip undefined values
        if (value === undefined) continue

        if (Array.isArray(value)) {
            for (const item of value) params.append(key, item)
        } else {
            params.set(key, value)
        }
    }
    return params
}
