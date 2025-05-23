import i18next from "i18next"
import { activityTracking } from "../lib/config"
import { type APIDetail, configureStandardForm } from "../lib/standard-form"

const body = document.querySelector("body.signup-body")
if (body) {
    const signupForm = body.querySelector("form.signup-form")
    const displayNameInput = signupForm.elements.namedItem(
        "display_name",
    ) as HTMLInputElement
    const displayNameBlacklist = displayNameInput.dataset.blacklist
    const passwordInput = signupForm.querySelector(
        "input[type=password][data-name=password]",
    )
    const passwordConfirmInput = signupForm.querySelector(
        "input[type=password][data-name=password_confirm]",
    )

    const trackingInput = signupForm.elements.namedItem("tracking") as HTMLInputElement
    trackingInput.value = activityTracking.toString()

    configureStandardForm(
        signupForm,
        ({ redirect_url }) => {
            console.debug("onSignupFormSuccess", redirect_url)
            window.location.href = redirect_url
        },
        () => {
            const result: APIDetail[] = []

            // Validate name for blacklisted characters
            const displayNameValue = displayNameInput.value
            if (
                displayNameBlacklist.split("").some((c) => displayNameValue.includes(c))
            ) {
                const msg = i18next.t("validations.url_characters", {
                    characters: displayNameBlacklist,
                    interpolation: { escapeValue: false },
                })
                result.push({ type: "error", loc: ["", "display_name"], msg })
            }

            // Validate passwords equality
            if (passwordInput.value !== passwordConfirmInput.value) {
                const msg = i18next.t("validation.passwords_missmatch")
                result.push({ type: "error", loc: ["", "password"], msg })
                result.push({ type: "error", loc: ["", "password_confirm"], msg })
            }

            return result
        },
    )
}
