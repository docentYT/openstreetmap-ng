In this guide, we present the recommended VSCode configuration when working on the OpenStreetMap-NG project.

**TL;DR** We recommend installing all workspace-recommended extensions. These are defined in the [.vscode/extensions.json](https://github.com/Zaczero/openstreetmap-ng/blob/main/.vscode/extensions.json) file and will appear in the recommended extensions tab. Below is a summary of their functionalities.

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/cf5f379f-6d91-4538-a726-27849ca869e8)

## Biome

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/c2b5502b-0bd5-4691-83fe-cbbd474bf960)

We use [Biome](https://biomejs.dev) for formatting, linting, bundling, and testing our JavaScript code. Installing their official Biome extension enables proper integration with VSCode.

## Coverage Gutters

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/d8879c22-bafc-4d79-8935-5456f5ea8774)

This extension is extremely useful for writing tests. When tests are run, either directly in VSCode or via the `run-tests` command, the coverage report will be displayed in the editor:

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/096d066c-7073-4287-b8fd-0ae2d275eee4)

You can easily toggle this feature on and off using the control at the bottom of the VSCode window:

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/2321c686-be82-40c3-960d-bcf5447aa641)

## Nix IDE

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/47d25b5d-6f95-4cc4-826b-392af3a0aed4)

The Nix IDE extension adds support for the Nix language in VSCode. Installing it enables proper syntax highlighting and code completion for Nix files, along with linting and formatting support.

## Prettier

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/1cfe881e-fe51-4548-9f81-77870e8dd7af)

We use [Prettier](https://prettier.io) for formatting SCSS files. With this extension, you can format documents directly in VSCode using the same tooling.

## Ruff

![image](https://github.com/Zaczero/openstreetmap-ng/assets/10835147/4b595aba-e82b-47f1-ba4f-eee563e65b0d)

[Ruff](https://docs.astral.sh/ruff/) is a fast Python linter and code formatter. This extension integrates Ruff directly with VSCode, helping you maintain clean and consistent Python code.