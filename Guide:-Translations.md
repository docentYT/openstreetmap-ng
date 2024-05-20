Currently, most of the project's translations are sourced from the existing website's translations, which are managed through [translatewiki](https://translatewiki.net/wiki/Translating:OpenStreetMap).
These translations are then transpiled into [i18next JSON v4](https://www.i18next.com/misc/json-format#i18next-json-v4) format for use within the project.

To add or modify translations that are specific to OpenStreetMap-NG, simply edit the [extra_en.yaml](https://github.com/Zaczero/openstreetmap-ng/blob/main/config/locale/extra_en.yaml) file (english-only).
When in code, prefer using hard-coded translation strings (no f-strings, no formatting) so it's possible to easily discover all translations using static analysis.

## Live Updates

When the project's helper services are running (using `dev-start`), any changes you make to `extra_en.yaml` will be automatically recompiled.

### Python and Jinja Templates

For translations used in Python code, you'll need to reload the web server because the [gettext](https://docs.python.org/3/library/gettext.html) module caches translation files internally.

### JavaScript

For translations used in JavaScript code, you'll need to reload the page to see the changes.

## Examples

Here are some short examples on how to integrate the translations.

```py
from app.lib.translation import t
fg.title(t('api.notes.rss.title'))
```

```jinja2
<span>{{ t('layouts.sign_up') }}</span>
```

```js
import i18next from "i18next"
closeButton.ariaLabel = i18next.t("javascripts.close")
```

## non-English Translation Support

Please note that there isn't currently a direct way to add new non-english translations.
This functionality will be available in the future.