**📚 This is the continuation of the [Getting Started](https://github.com/Zaczero/openstreetmap-ng/wiki/Contributing:-Getting-Started) guide.**

## Templates

Templates define the HTML structure of the web pages, they are usually served by the application's controllers. Templates are also used to render some RSS feeds content and email notifications. Templates support live-reloading, which means that you can edit them and see the changes in real-time without restarting the web server.

## Translations

To add or change text in the application, simply edit the config/locale/extra_en.yaml file. This file contains all the NextGen translations and is overlaid on top of the [translatewiki translations](https://translatewiki.net/wiki/Translating:OpenStreetMap). You can't edit the translatewiki texts directly, you should create new translations instead. Any changes you make to the extra_en.yaml file will be automatically recompiled by the watch-locale service. The JavaScript [i18next](https://www.i18next.com/) library supports live-reloading of translations, but Python's [gettext](https://docs.python.org/3/library/gettext.html) does not.

## Stylesheets

We use [SCSS](https://sass-lang.com/) to write stylesheets. SCSS is a superset of CSS that allows you to use variables, mixins, and nesting. If you are only familiar with CSS, you will easily understand how SCSS works. To make changes, edit files in the app/static/scss and if you have dev services running, they will be automatically recompiled to CSS in the app/static/css directory. [Autoprefixer](https://github.com/postcss/autoprefixer) is used to add vendor-specific prefixes to generated CSS. You may require to force reload the page in your browser to see the changes (<kbd>CTRL+F5</kbd> or <kbd>CTRL+SHIFT+R</kbd>).

## JavaScript

The JavaScript code is located in the app/static/js directory. This project does not use any JavaScript frameworks, just plain modern JavaScript. You don't have to worry about the compatibility of your code with older browsers. We use [Babel](https://babeljs.io/) to automatically transpile and polyfill the bundled JavaScript code. Whenever you make changes to the JavaScript files, the watch-js service will automatically recompile and bundle them. You may require to force reload the page in your browser to see the changes (<kbd>CTRL+F5</kbd> or <kbd>CTRL+SHIFT+R</kbd>).