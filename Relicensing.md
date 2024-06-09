The OpenStreetMap-NG project is undergoing a significant change in its licensing, moving from the GPL-2.0 license to the AGPL-3.0 license. This change aims to strengthen the freedom and accessibility of the website's source code for all users.

## Limitations of GPL-2.0

While the GPL-2.0 license promotes software freedom, its design primarily focuses on traditional software distribution, not network-based applications. Quoting from the GPL-2.0 license:

> (...) the GNU General Public License is intended to guarantee your freedom to share and change free software--to make sure the software is free for all its users.

Unfortunately, the well-known Software as a Service (SaaS) loophole allow the website's code to become proprietary and closed-source, undermining the principles of free software without violating the license.

## AGPL-3.0

The AGPL-3.0 license directly addresses this loophole by extending the protections of the GPL-2.0 to networked environments. It includes a key clause that states:

> (...) if you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network (if your version supports such interaction) an opportunity to receive the Corresponding Source of your version by providing access to the Corresponding Source from a network server at no charge (...)

This provision ensures that if the website's code is modified, anyone interacting with it through a network (like a web browser) must be offered access to the modified source code.

## Tips for Contributors

Due to licensing incompatibilities, code previously licensed under GPL-2.0 cannot be directly copied into the AGPL-3.0 codebase. However, contributors have several options to preserve the existing functionalities:

1. Several contributors have generously agreed to dual-license their work under both GPL-2.0 and AGPL-3.0. This means their code can be incorporated directly into the new codebase.

2. Contributors can also observe the behavior of public OpenStreetMap websites. By studying the features and functionality of these sites, contributors can reimplement similar or the same features within the AGPL-3.0 framework, thus avoiding any licensing conflicts.

### Dual-Licensing Agreements

Some contributors have agreed to dual-license their work under both GPL-2.0 and AGPL-3.0:

- <https://github.com/samanpwbb>
- <https://github.com/simonpoole>
- <https://github.com/TheMarex>