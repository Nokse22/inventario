<img height="128" src="data/icons/hicolor/scalable/apps/io.github.nokse22.inventario.svg" align="left"/>

# Inventario 
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-ff7b3f.svg)](https://www.python.org/)
  [![Generic badge](https://img.shields.io/badge/Version-v0.1.0-green.svg)](https://shields.io/)
  [![Downloads](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=Flathub%20Downloads&query=%24.installs_total&url=https%3A%2F%2Fflathub.org%2Fapi%2Fv2%2Fstats%2Fio.github.nokse22.inventario)](https://flathub.org/apps/details/io.github.nokse22.inventario)
  
  <p>
  A Gtk4/Libadwaita application to keep track of your inventory.
  It's still under development, it's not ready for use.
  </p>
  
  <div align="center">
  <img src="data/resources/Screenshot 1.png" height="400"/>
  </div>

## Feature ideas:
Not all features will be implemented, it's just a list of ideas
- [x] saving inventory in a file
- [x] automatically loading last file on startup
- [x] view items list
- [x] delete item
- [x] edit item
- [x] view item info
- [ ] sorting
  - [x] alphabetical sorting
  - [ ] numerical sorting
- [x] search/filter items
    - [x] search bar
    - [x] search item by detail
    - [x] disable other rows (filter)
    - [x] conditional filter (<,>)
    - [ ] fix bugs
- [x] custom info for every item with saving/loading from file
- [ ] export to csv or other formats
- [ ] import from csv or json
- [ ] dashboard with customizable widgets
- [ ] low stock
- [ ] datasheet file/url linking
- [ ] barcode scanning
- [ ] filtered view
- [ ] bill/invoice generation
- [ ] remove items from BOM
- [ ] products list with items linked
- [ ] threading for loading files

## Installation

### From source

You just need to clone the repository

```sh
git clone https://github.com/Nokse22/inventario.git
```

I'm using the latest version of Adwaita ( > 1.4.11) to be able to use Adw.NavigationSplitView that at the time is included only in Gnome Builder Nightly.

Open the project in GNOME Builder and click "Run Project".
