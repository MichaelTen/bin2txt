# bin2txt
Human-Readable Dumps for .mul 

# bin2txt – Human-Readable Dumps for Ultima Online `.mul` Files

`bin2txt.py` is a simple Python tool for converting Ultima Online `.mul` binary files into human-readable text.  
It was created as a learning aid to better understand the inner workings of `.mul` file structures, starting with the static object index files (`staidxX.mul`).

The script **does not contain or distribute any Ultima Online assets**.  
It only reads `.mul` files you already have and outputs their data in a friendly format.

---

## Features

- **Hex Dump Mode**  
  View any binary file’s contents in hex + ASCII side-by-side.  
  Useful for inspecting unknown formats, verifying byte layouts, or exploring raw data.  
  Note: large image files will produce very large text outputs.

- **staidx Mode**  
  Decode Ultima Online `staidxX.mul` files into columns:  
  ```
  index, offset, length, extra
  ```  
  This shows one entry per 8×8 map block.  
  Useful for inspecting static object indexes without loading graphics.

- **artidx Mode**  
  Decode `artidx.mul` into:  
  ```
  index, offset, length
  ```  
  Shows where each art ID’s data is located in `art.mul` (or `-1,0` if missing).  
  Helpful for seeing which art IDs are populated without dumping the full art files.

- **Interactive Mode Prompt**  
  If no mode is specified, the script will ask which mode you want, with descriptions for each.

---

## Current Testing Status

So far, the script has been tested only with:
- `staidx0.mul`
- `staidx#.mul` (where `#` is a map index number, e.g., 1, 2, etc.)

It should also work for `artidx.mul`, but additional testing on other `.mul` files is encouraged.

---

## Why I Made This

I built this tool to **understand Ultima Online’s file formats more deeply**.  
While `.mul` editors like UOFiddler exist, I wanted a lightweight way to *look under the hood* at the raw binary data and index structures.

Learning to parse these files helps demystify:
- How UO maps store terrain and static objects.
- How artwork is stored and indexed.
- How the client and server interpret file offsets and lengths.

---

## Potential Learning Applications

You could use this tool to:
- Learn basic binary file parsing with Python’s `struct` module.
- Explore how fixed-record binary index files are structured.
- Understand the mapping between `.mul` index files and the corresponding data files.
- Build more advanced `.mul` inspection tools or editors.
- Automate validation of custom map/statics/artwork projects before loading them into UO tools.

---

## Potential Project Ideas

1. **Custom Map Validator**  
   Check if all `staidx` offsets in a custom map are valid and point to real static data.

2. **Art Asset Inventory**  
   Scan `artidx.mul` to see which art IDs are unused, then plan new asset allocations.

3. **Automated Blank File Generator**  
   Extend the script to create fully blank `.mul` index/data pairs for scratch projects.

4. **Diff Tool for MUL Indexes**  
   Compare two `.mul` index files to see where offsets/lengths differ.

5. **Visualization Layer**  
   Build a web-based viewer that loads the CSV output and visualizes populated/unpopulated blocks.

---

## Usage

```bash
python bin2txt.py <mode> <input_file> [optional_output_file]

Modes:
  hex     Hex/ASCII dump of any binary file.
  staidx  Decode Ultima Online staidxX.mul index files.
  artidx  Decode Ultima Online artidx.mul index files.

If you omit the mode, you’ll be prompted to choose.
```

Examples:
```bash
# Decode staidx0.mul into staidx0_bin_output.txt
python bin2txt.py staidx staidx0.mul

# Let the script ask which mode to use
python bin2txt.py staidx0.mul

# Decode artidx.mul into artidx_artidx_output.txt
python bin2txt.py artidx artidx.mul
```

---

## License

You are free to use, modify, and share this script.  
Please avoid distributing any `.mul` files or Ultima Online assets, as they are owned by Electronic Arts.

---

## Disclaimer

This project is **not affiliated with or endorsed by Electronic Arts**.  
"Ultima Online" and all related assets are trademarks of Electronic Arts Inc.  
This tool is provided solely for educational purposes and for working with files you have the legal right to use.
