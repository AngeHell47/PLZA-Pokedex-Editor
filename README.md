# PLZA Pokedex Editor
<sub>This project is not associated with TPC (The Pokémon Company), GameFreak, Nintendo nor any other entity.</sub>

---

## What's this?
While waiting for the PKHex update, this is a simple tool that lets you edit your Pokedex data directly from your Pokémon Legends: ZA save file.
You can mark Pokémon as captured, battled, or shiny, then save your changes back into the game.

## Dependencies
- Python 3.13 (other versions of Python 3 should work too)

## How to use

1. Dump your save file using JKSV or similar
2. Copy your save file to your PC
3. Download latest release ZIP from the [Releases](https://github.com/AngeHell47/PLZA-Pokedex-Editor/releases) Section (or Download latest release EXE and execute it directly)
4. Open your shell (powershell or cmd for windows)
5. Run the Script like `python <path/to/main.py> <path/to/save/main>`!

It will output a new file with `_old` appended to the filename, just restore that save using JKSV or similar and you should be good to go! 

## Thanks to:
- Azalea-w for the lib [plza-save-utils](https://github.com/azalea-w/plza-save-utils)

- The maintainers of [PKHeX](https://github.com/kwsch/PKHeX/) for implementing SwishCrypto

- GameFreak for creating the game
