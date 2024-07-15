#!/usr/bin/env python3

# 3dsconv.py by ihaveamac
# license: MIT License
# https://github.com/ihaveamac/3dsconv

import argparse
import base64
import binascii
import glob
import hashlib
import itertools
import math
import os
import struct
import sys
import zlib

VERSION = '4.21'

# don't know of a better way to store binary data in a script
# compressed using zlib then encoded with base64
# retail CIA certificate chain
CERTCHAIN_RETAIL = b'''
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
JWFnDuv/P7kyh1k='''

# ticket (blank titlekey and title ID), tmd signature with blank header
#   (blank title ID) and blank content info records
TICKET_TMD = b'''
eJxjYGRgYRgFZIOg/PwSXWdHAwgw1o0IhjKTaW83I+2toJMlBAAjgwiQXAPEIlA2CGgwQFzXAsbM
EMH/BMBAOB8vGM1/FAH0/OccAGUmEacfR/J2AAAmBS75'''

MU = 0x200  # media unit
READ_SIZE = 0x800000  # used from padxorer
ZEROKEY = bytes(0x10)


# used from http://www.falatic.com/index.php/108/python-and-bitwise-rotation
# converted to def because pycodestyle complained to me
def rol(val, r_bits, max_bits):
    return (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
        ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))


def print_v(*msg, end='\n') -> None:
    '''Does nothing unless verbose mode is enabled

    If verbose mode is enabled, see: _print_v()
    '''

    return


def _print_v(*msg, end='\n') -> None:
    '''See: print()'''
    print(*msg, end=end)


def v(msg):
    '''Does nothing unless verbose mode is enabled

    If verbose mode is enabled, see: _v()
    '''

    return ''


def _v(msg):
    '''Returns the argument'''
    return msg


def _enable_verbose():
    '''Enables verbose mode functions'''

    global print_v
    print_v = _print_v

    global v
    v = _v


# error messages
def error(*msg):
    print('Error:', *msg)


# show a progress bar
def show_progress(val, maxval):
    # print() didn't do what I wanted so I'm doing this
    minval = min(val, maxval)
    sys.stdout.write('\r  {:>5.1f}% {:>10} / {}'.format(
        (minval / maxval) * 100, minval, maxval)
    )
    sys.stdout.flush()


def parse_args() -> argparse.Namespace:
    '''Parses and returns the command-line arguments'''

    parser = argparse.ArgumentParser(
        prog='3dsconv.py',
        description='Convert Nintendo 3DS CCI (.3ds/.cci) to CIA'
    )

    parser.add_argument(
        '-o', '--output',
        metavar='output-directory',
        default='',
        help=(
            'Save converted files in specified directory '
            '(default: current directory)'
        )
    )

    parser.add_argument(
        '-b', '--boot9',
        metavar='path-to-boot9',
        default=os.environ.get('BOOT9_PATH'),
        help='Path to dump of ARM9 bootROM, protected or full'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing converted files'
    )

    parser.add_argument(
        '--ignore-bad-hashes',
        action='store_true',
        help='Ignore invalid hashes and CCI files and convert anyway'
    )

    parser.add_argument(
        '--ignore-encryption',
        action='store_true',
        help='Ignore the encryption header value and assume ROM is unencrypted'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print more information'
    )

    parser.add_argument(
        '--dev-keys',
        action='store_true',
        help='Use developer-unit keys'
    )

    # deprecated arguments; we want to print out a message on this
    # in the future we can probably use an `action` to handle this.
    parser.add_argument(
        '--gen-ncchinfo', '--gen-ncch-all', '--xorpads',
        dest='use_deprecated',
        action='store_true',
        help=argparse.SUPPRESS
    )

    # arguments kept for backwards compatibility
    parser.add_argument(
        '--no-convert', '--noconvert',
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS
    )

    # positional arguments
    parser.add_argument(
        'game',
        nargs='+',
        help='Game file to convert to CIA'
    )

    # if no arguments are provided, display help message
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def main():
    '''Used to execute tool on the command line.

    First, arguments provided on the command-line are parsed, then
    the specified game files are converted to CIA.
    '''

    # check for pyaes which is used for crypto
    pyaes_found = False
    try:
        import pyaes
        pyaes_found = True
    except ImportError:
        pass  # this is handled later

    args = parse_args()

    if args.verbose:
        _enable_verbose()

    total_files = 0
    processed_files = 0

    certchain_dev = None
    if args.dev_keys:
        print(
            'Devkit keys are being used since `--dev-keys\' was passed. Note '
            'the resulting files will still be encrypted with devkit keys, '
            'and only installable on developer units without extra conversion.'
        )
        print('Looking for certchain-dev.bin...')

        def check_path(path, certchain_dev=None):
            if certchain_dev is None:
                if os.path.isfile(path):
                    with open(path, 'rb') as c:
                        certchain = c.read(0xA00)
                        correct_hash = 'd5c3d811a7eb87340aa9f4ab1841b6c4'
                        if hashlib.md5(certchain).hexdigest() == correct_hash:
                            return certchain
                return None

            else:
                return certchain_dev

        certchain_dev = check_path('certchain-dev.bin')
        certchain_dev = check_path(
            os.path.expanduser('~') + '/.3ds/certchain-dev.bin',
            certchain_dev
        )

        if not certchain_dev:
            error('Invalid or missing dev certchain. See README for details.')
            sys.exit(1)

    files = []
    for arg in args.game:
        to_add = glob.glob(arg)
        if len(to_add) == 0:
            error('"{}" doesn\'t exist.'.format(arg))
            total_files += 1
        else:
            for input_file in to_add:
                rom_name = os.path.basename(os.path.splitext(input_file)[0])
                cia_name = os.path.join(args.output, rom_name + '.cia')
                if not args.overwrite and os.path.isfile(cia_name):
                    error(
                        '"{}" already exists. Use `--overwrite\' to force'
                        'conversion.'.format(cia_name)
                    )
                    continue
                total_files += 1
                files.append([input_file, rom_name, cia_name])

    if args.use_deprecated:
        print(
            'Note: Deprecated options are being used. XORpads are no longer '
            'supported. See the README at '
            'https://github.com/ihaveamac/3dsconv for more details.'
        )

    # print if pyaes is found, and search for boot9 if it is
    # then get the original NCCH key from it
    orig_ncch_key = None
    if pyaes_found:
        print_v('pyaes found, Searching for protected ARM9 bootROM')

        def set_keys(boot9_file) -> int:
            keys_offset = 0
            if os.path.getsize(boot9_file) == 0x10000:
                keys_offset += 0x8000
            if args.dev_keys:
                keys_offset += 0x400
            with open(boot9_file, 'rb') as f:
                # get Original NCCH (slot 0x2C key X)
                f.seek(0x59D0 + keys_offset)
                key = f.read(0x10)
                key_hash = hashlib.md5(key).hexdigest()
                correct_hash = (
                    '49aa32c775608af6298ddc0fc6d18a7e'
                    if args.dev_keys else
                    'e35bf88330f4f1b2bb6fd5b870a679ca'
                )
                if key_hash == correct_hash:
                    print_v('Correct key found.')
                    return int.from_bytes(key, byteorder='big')

                print_v('Corrupt file (invalid key).')
                return None

        def check_path(path, orig_ncch_key=None) -> int:
            if orig_ncch_key is None:
                print_v('... {}: '.format(path), end='')
                if os.path.isfile(path):
                    return set_keys(path)
                else:
                    print_v('File doesn\'t exist.')
                    return None

            else:
                return orig_ncch_key

        # check supplied path by boot9_path or --boot9
        if args.boot9:
            check_path(args.boot9)
        orig_ncch_key = check_path('boot9.bin')
        orig_ncch_key = check_path('boot9_prot.bin', orig_ncch_key)

        orig_ncch_key = check_path(
            os.path.expanduser('~') + '/.3ds/boot9.bin',
            orig_ncch_key
        )
        orig_ncch_key = check_path(
            os.path.expanduser('~') + '/.3ds/boot9_prot.bin',
            orig_ncch_key
        )

        if orig_ncch_key is None:
            error('bootROM not found, encryption will not be supported')
    else:
        error('pyaes not found, encryption will not be supported')

    # create output directory if it doesn't exist
    if args.output != '':
        os.makedirs(args.output, exist_ok=True)

    if not total_files:
        error('No files were given.')
        sys.exit(1)
    if not files:
        error('No inputted files exist.')
        sys.exit(1)

    for rom_file in files:
        with open(rom_file[0], 'rb') as rom:
            print_v('----------\nProcessing {}...'.format(rom_file[0]))
            # check for NCSD magic
            # 3DS NAND dumps also have this
            rom.seek(0x100)
            ncsd_magic = rom.read(4)
            if ncsd_magic != b'NCSD':
                error('"{}" is not a CCI file (missing NCSD magic).'.format(
                    rom_file[0]
                ))
                continue

            # get title ID
            rom.seek(0x108)
            title_id = rom.read(8)[::-1]
            title_id_hex = binascii.hexlify(title_id).decode('utf-8').upper()
            print_v('\nTitle ID:', format(title_id_hex))

            # get partition sizes
            rom.seek(0x120)

            # find Game Executable CXI
            game_cxi_offset = struct.unpack('<I', rom.read(4))[0] * MU
            game_cxi_size = struct.unpack('<I', rom.read(4))[0] * MU
            print_v('\nGame Executable CXI Size: {:X}'.format(game_cxi_size))

            # find Manual CFA
            manual_cfa_offset = struct.unpack('<I', rom.read(4))[0] * MU
            manual_cfa_size = struct.unpack('<I', rom.read(4))[0] * MU
            print_v('Manual CFA Size: {:X}'.format(manual_cfa_size))

            # find Download Play child CFA
            dlpchild_cfa_offset = struct.unpack('<I', rom.read(4))[0] * MU
            dlpchild_cfa_size = struct.unpack('<I', rom.read(4))[0] * MU
            print_v('Download Play child CFA Size: {:X}\n'.format(
                dlpchild_cfa_size
            ))

            # check for NCCH magic
            # prevents NAND dumps from being "converted"
            rom.seek(game_cxi_offset + 0x100)
            ncch_magic = rom.read(4)
            if ncch_magic != b'NCCH':
                error('"{}" is not a CCI file (missing NCCH magic).'.format(
                    rom_file[0]
                ))
                continue

            # get the encryption type
            rom.seek(game_cxi_offset + 0x18F)
            # pay no mind to this ugliness...
            encryption_bitmask = struct.pack('c', rom.read(1))[0]
            encrypted = not (
                encryption_bitmask & 0x4 or args.ignore_encryption
            )
            zerokey_encrypted = encryption_bitmask & 0x1

            if encrypted:
                if orig_ncch_key is None:
                    error(
                        '"{}" is encrypted using Original NCCH and pyaes or '
                        'the bootROM were not found, therefore this can not '
                        'be converted. See the README at '
                        'https://github.com/ihaveamac/3dsconv for details.'
                        .format(rom_file[0])
                    )
                    continue
                else:
                    # get normal key to decrypt parts of the file
                    key = b''
                    ctr_extheader_v = int(
                        title_id_hex + '0100000000000000',
                        16
                    )
                    ctr_exefs_v = int(title_id_hex + '0200000000000000', 16)
                    if zerokey_encrypted:
                        key = ZEROKEY
                    else:
                        rom.seek(game_cxi_offset)
                        key_y_bytes = rom.read(0x10)
                        key_y = int.from_bytes(key_y_bytes, byteorder='big')
                        key = rol(
                            (
                                rol(orig_ncch_key, 2, 128) ^ key_y
                            ) + 0x1FF9E9AAC5FE0408024591DC5D52768A,
                            87,
                            128
                        ).to_bytes(0x10, byteorder='big')

                        print_v('Normal key:',
                                binascii.hexlify(key).decode('utf-8').upper())

            encryption_status = 'decrypted'
            if args.ignore_encryption:
                encryption_status = 'ignore encryption'
            elif zerokey_encrypted:
                encryption_status = 'zerokey encrypted'
            elif encrypted:
                encryption_status = 'encrypted'

            print(f"Converting {rom_file[1]} ({encryption_status})...")

            # Game Executable fist-half ExtHeader
            print_v('\nVerifying ExtHeader...')
            rom.seek(game_cxi_offset + 0x200)
            extheader = rom.read(0x400)
            if encrypted:
                print_v('Decrypting ExtHeader...')
                ctr_extheader = pyaes.Counter(initial_value=ctr_extheader_v)
                cipher_extheader = pyaes.AESModeOfOperationCTR(
                    key, counter=ctr_extheader)
                extheader = cipher_extheader.decrypt(extheader)
            extheader_hash = hashlib.sha256(extheader).digest()
            rom.seek(0x4160)
            ncch_extheader_hash = rom.read(0x20)
            if extheader_hash != ncch_extheader_hash:
                print(
                    'This file may be corrupt (invalid ExtHeader hash). '
                    'If you are certain that the rom is decrypted, '
                    'use --ignore-encryption'
                )
                if args.ignore_bad_hashes:
                    print(
                        'Converting anyway because --ignore-bad-hashes '
                        'was passed.'
                    )
                else:
                    continue

            # patch ExtHeader to make an SD title
            print_v('Patching ExtHeader...')
            extheader_list = list(extheader)
            extheader_list[0xD] |= 2
            extheader = bytes(extheader_list)
            new_extheader_hash = hashlib.sha256(extheader).digest()

            # get dependency list for meta region
            dependency_list = extheader[0x40:0x1C0]

            # get save data size for tmd
            save_size = extheader[0x1C0:0x1C4]

            if encrypted:
                print_v('Re-encrypting ExtHeader...')
                ctr_extheader = pyaes.Counter(initial_value=ctr_extheader_v)
                cipher_extheader = pyaes.AESModeOfOperationCTR(
                    key, counter=ctr_extheader)
                extheader = cipher_extheader.encrypt(extheader)

            # Game Executable NCCH Header
            print_v('\nReading NCCH Header of Game Executable...')
            rom.seek(game_cxi_offset)
            ncch_header = list(rom.read(0x200))
            ncch_header[0x160:0x180] = list(new_extheader_hash)

            if args.ignore_encryption:
                print_v(
                    '\nEncryption is ignored, setting ncchflag[7] to NoCrypto'
                )
                ncch_header[0x18F] |= 0x4

            ncch_header = bytes(ncch_header)

            # get icon from ExeFS
            print_v('Getting SMDH...')
            exefs_offset = struct.unpack(
                '<I',
                ncch_header[0x1A0:0x1A4]
            )[0] * MU

            rom.seek(game_cxi_offset + exefs_offset)
            # exefs can contain up to 10 file headers but use only 4 normally
            exefs_file_header = rom.read(0x40)
            if encrypted:
                print_v('Decrypting ExeFS Header...')
                ctr_exefs = pyaes.Counter(initial_value=ctr_exefs_v)
                cipher_exefs = pyaes.AESModeOfOperationCTR(
                    key, counter=ctr_exefs)
                exefs_file_header = cipher_exefs.encrypt(exefs_file_header)
            exefs_icon = None
            for header_num in range(0, 4):
                header_chunk = exefs_file_header[
                    header_num * 0x10:0x8 + (header_num * 0x10)
                ].rstrip(b'\0')

                if header_chunk == b'icon':
                    exefs_icon_offset = struct.unpack(
                        '<I', exefs_file_header[0x8 + (header_num * 0x10):
                                                0xC + (header_num * 0x10)])[0]
                    rom.seek(exefs_icon_offset + 0x200 - 0x40, 1)
                    exefs_icon = rom.read(0x36C0)
                    if encrypted:
                        ctr_exefs_icon_v = ctr_exefs_v +\
                            (exefs_icon_offset // 0x10) + 0x20
                        ctr_exefs_icon = pyaes.Counter(
                            initial_value=ctr_exefs_icon_v)
                        cipher_exefs_icon = pyaes.AESModeOfOperationCTR(
                            key, counter=ctr_exefs_icon)
                        exefs_icon = cipher_exefs_icon.decrypt(exefs_icon)
                    break
            if exefs_icon is None:
                error('Icon not found in the ExeFS.')
                continue

            # Since we will only have three possible results to these,
            # these are hardcoded variables for convenience
            # These could be generated but given this, I'm not doing that
            # I made it a little better
            tmd_padding = bytes(12)  # padding to add at the end of the tmd
            content_count = 1
            tmd_size = 0xB34
            content_index = 0b10000000
            if manual_cfa_offset != 0:
                tmd_padding += bytes(16)
                content_count += 1
                tmd_size += 0x30
                content_index += 0b01000000
            if dlpchild_cfa_offset != 0:
                tmd_padding += bytes(16)
                content_count += 1
                tmd_size += 0x30
                content_index += 0b00100000

            # CIA
            with open(rom_file[2], 'wb') as cia:
                print_v('Writing CIA header...')

                # 1st content: ID 0x, Index 0x0
                chunk_records = struct.pack('>III', 0, 0, 0)
                chunk_records += struct.pack(">I", game_cxi_size)
                chunk_records += bytes(0x20)  # SHA-256 to be added later
                if manual_cfa_offset != 0:
                    # 2nd content: ID 0x1, Index 0x1
                    chunk_records += struct.pack('>III', 1, 0x10000, 0)
                    chunk_records += struct.pack('>I', manual_cfa_size)
                    chunk_records += bytes(0x20)  # SHA-256 to be added later
                if dlpchild_cfa_offset != 0:
                    # 3nd content: ID 0x2, Index 0x2
                    chunk_records += struct.pack('>III', 2, 0x20000, 0)
                    chunk_records += struct.pack('>I', dlpchild_cfa_size)
                    chunk_records += bytes(0x20)  # SHA-256 to be added later

                content_size = (
                    game_cxi_size +
                    manual_cfa_size +
                    dlpchild_cfa_size
                )

                cia.write(
                    # initial CIA header
                    struct.pack('<IHHII', 0x2020, 0, 0, 0xA00, 0x350) +
                    # tmd size, meta size, content size
                    # this is ugly as well
                    struct.pack('<III', tmd_size, 0x3AC0, content_size) +
                    # content index
                    struct.pack('<IB', 0, content_index) + (bytes(0x201F)) +
                    # cert chain
                    (
                        certchain_dev
                        if args.dev_keys else
                        zlib.decompress(base64.b64decode(CERTCHAIN_RETAIL))
                    ) +
                    # ticket, tmd
                    zlib.decompress(base64.b64decode(TICKET_TMD)) +
                    (bytes(0x96C)) +
                    # chunk records in tmd + padding
                    chunk_records + tmd_padding
                )

                # changing to list to update and hash later
                chunk_records = list(chunk_records)

                # write content count in tmd
                cia.seek(0x2F9F)
                cia.write(bytes([content_count]))

                # write title ID in ticket and tmd
                cia.seek(0x2C1C)
                cia.write(title_id)
                cia.seek(0x2F4C)
                cia.write(title_id)

                # write save size in tmd
                cia.seek(0x2F5A)
                cia.write(save_size)

                # Game Executable CXI NCCH Header + first-half ExHeader
                cia.seek(0, 2)
                game_cxi_hash = hashlib.sha256(ncch_header + extheader)
                cia.write(ncch_header + extheader)

                # Game Executable CXI second-half ExHeader + contents
                print('Writing Game Executable CXI...')
                rom.seek(game_cxi_offset + 0x200 + 0x400)
                left = game_cxi_size - 0x200 - 0x400
                tmpread = ''
                for __ in itertools.repeat(
                        0, int(math.floor((game_cxi_size / READ_SIZE)) + 1)):
                    to_read = min(READ_SIZE, left)
                    tmpread = rom.read(to_read)
                    game_cxi_hash.update(tmpread)
                    cia.write(tmpread)
                    left -= READ_SIZE
                    show_progress(game_cxi_size - left, game_cxi_size)
                    if left <= 0:
                        print('')
                        break
                print_v('Game Executable CXI SHA-256 hash:')
                print_v('  {}'.format(game_cxi_hash.hexdigest().upper()))
                cia.seek(0x38D4)
                cia.write(game_cxi_hash.digest())
                chunk_records[0x10:0x30] = list(game_cxi_hash.digest())

                cr_offset = 0

                # Manual CFA
                if manual_cfa_offset != 0:
                    cia.seek(0, 2)
                    print('Writing Manual CFA...')
                    manual_cfa_hash = hashlib.sha256()
                    rom.seek(manual_cfa_offset)
                    left = manual_cfa_size
                    for __ in itertools.repeat(
                        0,
                        int(math.floor((manual_cfa_size / READ_SIZE)) + 1)
                    ):
                        to_read = min(READ_SIZE, left)
                        tmpread = rom.read(to_read)
                        manual_cfa_hash.update(tmpread)
                        cia.write(tmpread)
                        left -= READ_SIZE
                        show_progress(manual_cfa_size - left, manual_cfa_size)
                        if left <= 0:
                            print('')
                            break
                    print_v('Manual CFA SHA-256 hash:')
                    print_v('  {}'.format(manual_cfa_hash.hexdigest().upper()))
                    cia.seek(0x3904)
                    cia.write(manual_cfa_hash.digest())
                    chunk_records[0x40:0x60] = list(manual_cfa_hash.digest())
                    cr_offset += 0x30

                # Download Play child container CFA
                if dlpchild_cfa_offset != 0:
                    cia.seek(0, 2)
                    print('Writing Download Play child container CFA...')
                    dlpchild_cfa_hash = hashlib.sha256()
                    rom.seek(dlpchild_cfa_offset)
                    left = dlpchild_cfa_size
                    # i am so sorry
                    for __ in itertools.repeat(
                        0,
                        int(math.floor((dlpchild_cfa_size / READ_SIZE)) + 1)
                    ):
                        to_read = min(READ_SIZE, left)
                        tmpread = rom.read(to_read)
                        dlpchild_cfa_hash.update(tmpread)
                        cia.write(tmpread)
                        left -= READ_SIZE
                        show_progress(
                            dlpchild_cfa_size - left,
                            dlpchild_cfa_size
                        )
                        if left <= 0:
                            print('')
                            break
                    print_v(
                        '- Download Play child container CFA SHA-256 hash:'
                    )
                    print_v(f"  {dlpchild_cfa_hash.hexdigest().upper()}")
                    cia.seek(0x3904 + cr_offset)
                    cia.write(dlpchild_cfa_hash.digest())
                    chunk_records[0x40 + cr_offset:0x60 + cr_offset] = list(
                        dlpchild_cfa_hash.digest()
                    )

                # update final hashes
                print_v('\nUpdating hashes...')
                chunk_records_hash = hashlib.sha256(bytes(chunk_records))
                print_v('Content chunk records SHA-256 hash:')
                print_v('  {}'.format(chunk_records_hash.hexdigest().upper()))
                cia.seek(0x2FC7)
                cia.write(bytes([content_count]) + chunk_records_hash.digest())

                cia.seek(0x2FA4)
                info_records_hash = hashlib.sha256(
                    bytes(3) + bytes([content_count]) +
                    chunk_records_hash.digest() + (bytes(0x8DC))
                )
                print_v('Content info records SHA-256 hash:')
                print_v('  {}'.format(info_records_hash.hexdigest().upper()))
                cia.write(info_records_hash.digest())

                # write Meta region
                cia.seek(0, 2)
                cia.write(
                    dependency_list + bytes(0x180) + struct.pack('<I', 0x2) +
                    bytes(0xFC) + exefs_icon
                )

        processed_files += 1

    print(f"Done converting {processed_files} out of {total_files} files.")


if __name__ == "__main__":
    main()
