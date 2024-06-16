**📚 This is the continuation of the [Getting Started](https://github.com/Zaczero/openstreetmap-ng/wiki/Contributing:-Getting-Started) guide.**

## Templates

Template files are stored in the app/templates directory. These templates outline the HTML structure for web pages and are typically served by the application's controllers. Additionally, they render content for RSS feeds and email notifications. Templates support live-reloading, allowing you to see changes in real-time without restarting the web server.

## Translations

To update or add text in the application, modify the `config/locale/extra_en.yaml` file. This file contains all the NextGen translations which overlay the existing translations from [translatewiki](https://translatewiki.net/wiki/Translating:OpenStreetMap). Since we cannot directly edit translatewiki texts, new translations should be created here. Any changes to extra_en.yaml will be automatically recompiled by the watch-locale service. While the JavaScript library [i18next](https://www.i18next.com/) supports live-reloading of translations, Python's [gettext](https://docs.python.org/3/library/gettext.html) does not.

## Icons

Adding icons to the application is simple. Visit the [Bootstrap Icons](https://icons.getbootstrap.com/) website, find an icon, copy the provided HTML snippet, and paste it into the template file. All the necessary resources are already included.

## Stylesheets

We use [SCSS](https://sass-lang.com/) for writing stylesheets. SCSS extends CSS by allowing the use of variables, mixins, and nesting, making it more powerful and flexible. If you're familiar with CSS, you will easily understand SCSS. To make changes, edit the files in the app/static/scss directory. If the development services are running, these changes will be automatically recompiled into CSS in the app/static/css directory. [Autoprefixer](https://github.com/postcss/autoprefixer) handles adding vendor-specific prefixes to the generated CSS. Remember, you might need to force-reload the page in your browser to see the changes (<kbd>CTRL+F5</kbd> or <kbd>CTRL+SHIFT+R</kbd>).

## JavaScript

The JavaScript code is located in the app/static/js directory. This project uses plain modern JavaScript without any frameworks. You don't need to be concerned about compatibility with older browsers, as we use [Babel](https://babeljs.io/) to transpile and polyfill the bundled JavaScript code automatically. Whenever you modify the JavaScript files, the watch-js service will recompile and bundle them automatically. You may need to force-reload the page in your browser to see the updates (<kbd>CTRL+F5</kbd> or <kbd>CTRL+SHIFT+R</kbd>).