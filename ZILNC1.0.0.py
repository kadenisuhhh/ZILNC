# this program was made to convert Genius lyric notation to
# Musixmatch lyric notation and vice versa because I was fucking over manually
# doing it lol.
# To use this program, call it in the python terminal with the
# file you want to convert, as well as 'gen' to convert to Genius,
# and 'mus' to convert to Musixmatch. Alternatively, you can
# just call it without any arguments for a text walkthrough.

import sys
import os

SUPPORTED_NOTATIONS = ['gen', 'mus']

GENIUS_NOTATION = {'intro': '[Intro]', 'verse': '[Verse ',
                   'pre-chorus': '[Pre-Chorus]', 'chorus': '[Chorus]',
                   'hook': '[Chorus]', 'refrain': '[Refrain]',
                   'bridge': '[Bridge]', 'breakdown': '[Breakdown]',
                   'outro': '[Outro]'}
MUSIX_NOTATION = {'intro': '#INTRO', 'verse': '#VERSE',
                  'pre-chorus': '#PRE-CHORUS', 'chorus': '#CHORUS',
                  'hook': '#HOOK', 'refrain': '#MANUALLY CHOOSE',
                  'bridge': '#BRIDGE', 'breakdown': '#MANUALLY CHOOSE',
                  'outro': '#OUTRO'}

DIRECTORY = os.getcwd() + '\\'


def main():
    try:
        sys.argv[1]
    except IndexError:
        inputs = get_inputs()
    else:
        inputs = get_sys_inputs()

    check_inputs(inputs)

    if inputs[2] == 'gen':
        convert_to_genius(inputs[0], inputs[1])
    if inputs[2] == 'mus':
        convert_to_musix(inputs[0], inputs[1])


def get_inputs():
    input_file = input('What file do you want to convert? ')
    notation = input('What notation do you want to convert to? \n'
                     '(\'gen\' for Genius and \'mus\' for Musixmatch.) ')
    output_file = input('Custom name for output file (default is '
                        '\'input-file_notation\')? ')

    return [input_file, output_file, notation]


def get_sys_inputs():
    input_file = sys.argv[1]

    try:
        sys.argv[3]
    except IndexError:
        output_file = ''
    else:
        output_file = sys.argv[3]

    try:
        sys.argv[2]
    except IndexError:
        sys.exit('Error: No notation was specified.')
    else:
        notation = sys.argv[2]

    return [input_file, output_file, notation]


def check_inputs(inputs):
    if not inputs[0].endswith('.txt'):
        inputs[0] = DIRECTORY + inputs[0] + '.txt'
    elif not os.path.isfile(inputs[0]):
        inputs[0] = DIRECTORY + inputs[0]

    if not os.path.isfile(inputs[0]):
        sys.exit('Error: The file you entered doesn\'t exist.')

    if not inputs[2] in SUPPORTED_NOTATIONS:
        sys.exit('Error: Unknown lyric notation.\n'
                 'Use the parameter \'gen\' to convert to Genius notation.\n'
                 'Use the parameter \'mus\' to convert to Musixmatch notation.')

    if inputs[1] == '':
        inputs[1] = inputs[0][:-4] + '_' + inputs[2] + '.txt'
    elif not inputs[1].endswith('.txt'):
        inputs[1] = DIRECTORY + inputs[1] + '.txt'

    if inputs[0].upper() == inputs[1].upper():
        sys.exit('Error: Output file name cannot be the same '
                 'as input file name!')


def convert_to_genius(input_file, output_file):
    verse_count = 1
    changes = 0

    input_opened = open(input_file, 'r')
    output_opened = open(output_file, 'w')
    for line in input_opened:
        line = line.strip()
        if line.upper() in MUSIX_NOTATION.values():
            key = get_keys_from_value(MUSIX_NOTATION, line.upper())
            if line.upper() == MUSIX_NOTATION['verse']:
                line = GENIUS_NOTATION['verse'] + str(verse_count) + ']'
                verse_count += 1
            elif line == '':
                line = ''
            else:
                line = GENIUS_NOTATION[key]
            changes += 1
        output_opened.write(line + '\n')

    input_opened.close()
    output_opened.close()

    if changes == 0:
        os.remove(str(output_file))
        sys.exit('This is already a Genius-notated file, silly!')


def convert_to_musix(input_file, output_file):
    changes = 0

    input_opened = open(input_file, 'r')
    output_opened = open(output_file, 'w')
    for line in input_opened:
        line = line.strip()

        if line.startswith(GENIUS_NOTATION['verse']):
            line = MUSIX_NOTATION['verse']
            changes += 1
        if line in GENIUS_NOTATION.values():
            key = get_keys_from_value(GENIUS_NOTATION, line)
            if line == '':
                line = ''
            else:
                line = MUSIX_NOTATION[key]
            changes += 1

        output_opened.write(line + '\n')

    input_opened.close()
    output_opened.close()

    if changes == 0:
        os.remove(output_file)
        sys.exit('This is already a Musixmatch-notated file, silly!')


def get_keys_from_value(notation, val):
    return [k for k, v in notation.items() if v == val][0]


main()
