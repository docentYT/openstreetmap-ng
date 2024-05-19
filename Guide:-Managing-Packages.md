Here's a quick guide on how to update, install, and remove different types of packages used in our project.

## Python

We use the [Poetry](https://python-poetry.org/) dependency manager for Python packages. You can manage them using the following commands:

- **Update:** `poetry update` *([docs](https://python-poetry.org/docs/cli/#update))*
- **Install:** `poetry add <name>` *([docs](https://python-poetry.org/docs/cli/#add))*
- **Uninstall:** `poetry remove <name>` *([docs](https://python-poetry.org/docs/cli/#remove))*

## JavaScript

We use [Bun](https://bun.sh), an all-in-one JavaScript toolkit.

- **Update:** `bun update` *([docs](https://bun.sh/docs/cli/update))*
- **Install:** `bun add <name>` *([docs](https://bun.sh/docs/cli/add))*
- **Uninstall:** `bun remove <name>` *([docs](https://bun.sh/docs/cli/remove))*

## Nix and Other Software

For traditional software like databases or system tools, we use the [Nix](https://nixos.org) package manager. All the related configuration is stored in the `shell.nix` file.

### Updating

Nix packages are tied to specific [commits](https://github.com/NixOS/nixpkgs/commits/nixpkgs-unstable/) for reproducibility. To update to newer versions, you'll need to edit the pkgs hash in the `shell.nix` file *(it's at the very top)*. We provide a `nixpkgs-update` command that fully automates this process — simply run it.

### Installing and Uninstalling

To manage Nix packages, begin by using [Nix Search](https://search.nixos.org/packages) to find the package you need. Make sure to switch to the unstable channel. Next, open the `shell.nix` file. If you want to install a package, add its name to the list of packages in the file. To uninstall a package, do otherwise. Once you've made the changes, save the file and restart your development shell.