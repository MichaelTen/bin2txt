#!/usr/bin/env python3
import argparse
import struct
from pathlib import Path

def hex_dump_to_text(in_path: Path, out_path: Path, width: int = 16):
    def to_ascii(byte: int) -> str:
        return chr(byte) if 32 <= byte <= 126 else '.'

    with in_path.open('rb') as f, out_path.open('w', encoding='utf-8', newline='\n') as out:
        offset = 0
        while True:
            chunk = f.read(width)
            if not chunk:
                break
            hex_bytes = ' '.join(f'{b:02x}' for b in chunk)
            hex_bytes = hex_bytes.ljust(width * 3 - 1)
            ascii_repr = ''.join(to_ascii(b) for b in chunk)
            out.write(f'{offset:08x}  {hex_bytes}  |{ascii_repr}|\n')
            offset += len(chunk)

def dump_staidx_to_text(in_path: Path, out_path: Path, limit=None):
    entry_struct = struct.Struct('<iii')  # offset, length, extra
    entry_size = entry_struct.size
    file_size = in_path.stat().st_size
    if file_size % entry_size != 0:
        print(f'Warning: file size {file_size} not a multiple of {entry_size}; trailing bytes ignored.')
    total_entries = file_size // entry_size
    max_entries = min(total_entries, limit) if limit else total_entries

    with in_path.open('rb') as f, out_path.open('w', encoding='utf-8', newline='\n') as out:
        out.write('# index, offset, length, extra\n')
        for idx in range(max_entries):
            data = f.read(entry_size)
            if len(data) < entry_size:
                break
            off, length, extra = entry_struct.unpack(data)
            out.write(f'{idx},{off},{length},{extra}\n')

def dump_artidx_to_text(in_path: Path, out_path: Path, limit=None):
    entry_struct = struct.Struct('<ii')  # offset, length
    entry_size = entry_struct.size
    file_size = in_path.stat().st_size
    if file_size % entry_size != 0:
        print(f'Warning: file size {file_size} not a multiple of {entry_size}; trailing bytes ignored.')
    total_entries = file_size // entry_size
    max_entries = min(total_entries, limit) if limit else total_entries

    with in_path.open('rb') as f, out_path.open('w', encoding='utf-8', newline='\n') as out:
        out.write('# index, offset, length\n')
        for idx in range(max_entries):
            data = f.read(entry_size)
            if len(data) < entry_size:
                break            # partial trailing data
            off, length = entry_struct.unpack(data)
            out.write(f'{idx},{off},{length}\n')

def choose_mode():
    print("No mode specified. Which mode do you want?")
    print("1 = hex (hex/ASCII dump)")
    print("    View raw bytes of any file in hexadecimal with an ASCII side column.")
    print("    Use this when exploring unknown formats or verifying exact byte layouts.")
    print("    Note: image-heavy files will produce very large text outputs.")
    print()
    print("2 = staidx (decode staidxX.mul index entries)")
    print("    Parse the static object index for .mul maps (one entry per 8×8 block).")
    print("    Output columns: index, offset, length, extra.")
    print("    Use this to inspect or verify static placement data without loading graphics.")
    print()
    print("3 = artidx (decode artidx.mul index entries)")
    print("    Parse the artwork index table that points into art.mul (one entry per art ID).")
    print("    Output columns: index, offset, length.")
    print("    Use this to see which art IDs are populated and where, without dumping images.")
    choice = input("Enter choice [1/2/3]: ").strip()
    if choice == '1':
        return 'hex'
    elif choice == '2':
        return 'staidx'
    elif choice == '3':
        return 'artidx'
    else:
        raise SystemExit("Invalid choice.")

def main():
    ap = argparse.ArgumentParser(description='Convert binary files (.mul or any) to readable text.')
    ap.add_argument('mode', nargs='?', choices=['hex', 'staidx', 'artidx'],
                    help="hex = hex/ASCII dump; staidx = decode staidxX.mul; artidx = decode artidx.mul")
    ap.add_argument('input', type=Path, help='Input binary file')
    ap.add_argument('output', type=Path, nargs='?', help='Optional output text file')
    ap.add_argument('--width', type=int, default=16, help='Bytes per line for hex mode')
    ap.add_argument('--limit', type=int, default=None, help='Max entries for staidx/artidx mode')
    args = ap.parse_args()

    # If no mode given, ask interactively
    if not args.mode:
        args.mode = choose_mode()

    # Default output file if none provided
    if not args.output:
        suffix_map = {'hex': '_hex_output.txt', 'staidx': '_bin_output.txt', 'artidx': '_artidx_output.txt'}
        args.output = args.input.with_name(args.input.stem + suffix_map[args.mode])

    # Run chosen mode
    if args.mode == 'hex':
        hex_dump_to_text(args.input, args.output, width=args.width)
    elif args.mode == 'staidx':
        dump_staidx_to_text(args.input, args.output, limit=args.limit)
    elif args.mode == 'artidx':
        dump_artidx_to_text(args.input, args.output, limit=args.limit)

    print(f'Wrote {args.output}')

if __name__ == '__main__':
    main()
