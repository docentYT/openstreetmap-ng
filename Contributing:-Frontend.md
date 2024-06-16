**📚 This is the continuation of the [Getting Started](https://github.com/Zaczero/openstreetmap-ng/wiki/Contributing:-Getting-Started) guide.**

## Templates

Template files are stored in app/templates. Templates define the HTML structure of the web pages and are usually served by the application's controllers. They are also used to render some RSS feeds' content and email notifications. Templates support live-reloading, meaning you can edit them and see the changes in real-time without restarting the web server.

## Translations

To add or change text in the application, edit the `config/locale/extra_en.yaml` file. This file contains all the NextGen translations and overlays the [translatewiki translations](https://translatewiki.net/wiki/Translating:OpenStreetMap). You cannot edit the translatewiki texts directly; instead, create new translations. Any changes to extra_en.yaml will be automatically recompiled by the watch-locale service. The JavaScript [i18next](https://www.i18next.com/) library supports live-reloading of translations, but Python's [gettext](https://docs.python.org/3/library/gettext.html) does not.

## Icons

It is very easy to add icons to the application. Simply search for one on the [Bootstrap Icons](https://icons.getbootstrap.com) website, copy the HTML snippet provided, and paste it into the template file. All necessary resources are already installed.

## Stylesheets

We use [SCSS](https://sass-lang.com/) to write stylesheets. SCSS is a superset of CSS that allows the use of variables, mixins, and nesting. If you are familiar with CSS, you will easily understand SCSS. To make changes, edit files in the app/static/scss directory. If you have dev services running, they will be automatically recompiled to CSS in the app/static/css directory. [Autoprefixer](https://github.com/postcss/autoprefixer) adds vendor-specific prefixes to generated CSS. You may need to force-reload the page in your browser to see the changes (<kbd>CTRL+F5</kbd> or <kbd>CTRL+SHIFT+R</kbd>).

## JavaScript

The JavaScript code is located in the app/static/js directory. This project uses plain modern JavaScript without any JavaScript frameworks. You don't need to worry about compatibility with older browsers. We use [Babel](https://babeljs.io/) to automatically transpile and polyfill the bundled JavaScript code. Whenever you make changes to the JavaScript files, the watch-js service will automatically recompile and bundle them. You may need to force reload the page in your browser to see the changes (<kbd>CTRL+F5</kbd> or <kbd>CTRL+SHIFT+R</kbd>).