# this program was made to convert Genius lyric notation to
# Musixmatch lyric notation and vice versa because I was fucking over manually
# doing it lol.
# To use this program, call it in the python terminal with the
# input file name and (optionally) the output file name.
# Alternatively, call it without any arguments for a text walkthrough.

import sys
import os

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

    batch = is_batch(inputs[0])

    if batch:
        batch_inputs(inputs)
        for file in range(len(inputs[0])):
            if inputs[2][file] == 'gen':
                print('\n' + os.path.basename(inputs[0][file]) + ' detected to be Musixmatch notation!\n'
                      'Converting to Genius notation...', end='')
                convert_to_genius(inputs[0][file], inputs[1][file])
            if inputs[2][file] == 'mus':
                print('\n' + os.path.basename(inputs[0][file]) + ' detected to be Genius notation!\n'
                      'Converting to Musixmatch notation...', end='')
                convert_to_musix(inputs[0][file], inputs[1][file])
    else:
        check_inputs(inputs)

        if inputs[2] == 'gen':
            print('\n' + os.path.basename(inputs[0]) + ' detected to be Musixmatch notation!\n'
                  'Converting to Genius notation...', end='')
            convert_to_genius(inputs[0], inputs[1])
        if inputs[2] == 'mus':
            print('\n' + os.path.basename(inputs[0]) + ' detected to be Genius notation!\n'
                  'Converting to Musixmatch notation...', end='')
            convert_to_musix(inputs[0], inputs[1])


def get_inputs():
    input_file = input('What file do you want to convert? ')

    batch = is_batch(input_file)

    if batch:
        output_file = ''
    else:
        output_file = input('Custom name for output file (default is '
                            '\'input-file_notation\')? ')

    return [input_file, output_file, []]


def get_sys_inputs():
    input_file = sys.argv[1]

    if os.path.isdir(input_file):
        input_file = os.path.basename(input_file)

    batch = is_batch(input_file)

    if batch:
        output_file = ''
    else:
        try:
            sys.argv[2]
        except IndexError:
            output_file = ''
        else:
            output_file = sys.argv[2]

    return [input_file, output_file, []]


def is_batch(input_file):
    input_dir = DIRECTORY + input_file

    if os.path.isdir(input_dir):
        return True
    else:
        return False


def batch_inputs(inputs):

    confirm = input('\nDetected directory instead of file. Will proceed in batch mode.\n'
                    'ZILNC will attempt to convert all text documents inside.\n'
                    'Is this okay? (y for yes, n for no) ')

    if confirm == 'y':
        new_folder = inputs[0] + '\\' + inputs[0] + '_converted'
        os.mkdir(new_folder)
        inputs[0] = DIRECTORY + inputs[0]
        inputs[0] = find_files(inputs[0])
        if not inputs[0]:
            sys.exit('Error: There are no .txt files in this directory.')
    else:
        sys.exit('User cancelled batch conversion.')

    inputs[1] = []
    for file in range(len(inputs[0])):

        with open(inputs[0][file], 'r', encoding="utf8") as probe:
            for line in probe:
                line = line.strip()
                if line.startswith('['):
                    inputs[2].append('mus')
                    break
                if line.startswith('#'):
                    inputs[2].append('gen')
                    break

        inputs[1].append(DIRECTORY + new_folder + '\\' +
                         os.path.basename(inputs[0][file])[:-4] +
                         '_' + inputs[2][file] + '.txt')
    print(inputs)


def check_inputs(inputs):
    if not inputs[0].endswith('.txt'):
        inputs[0] = inputs[0] + '.txt'

    if not os.path.isfile(inputs[0]):
        sys.exit('\nError: The file you entered doesn\'t exist.')

    with open(inputs[0], 'r', encoding="utf8") as probe:
        for line in probe:
            line = line.strip()
            if line.startswith('['):
                inputs[2] = 'mus'
                break
            if line.startswith('#'):
                inputs[2] = 'gen'
                break

    if inputs[1] == '':
        inputs[1] = inputs[0][:-4] + '_' + inputs[2] + '.txt'
    elif not inputs[1].endswith('.txt'):
        inputs[1] = DIRECTORY + inputs[1] + '.txt'

    if inputs[0].upper() == inputs[1].upper():
        sys.exit('\nError: Output file name cannot be the same '
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
    print('done!')

    if changes == 0:
        os.remove(str(output_file))
        sys.exit('\nThis is already a Genius-notated file, silly!')


def convert_to_musix(input_file, output_file):
    changes = 0

    input_opened = open(input_file, 'r', encoding="utf8")
    output_opened = open(output_file, 'w', encoding="utf8")
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
    print('done!')

    if changes == 0:
        os.remove(output_file)
        sys.exit('\nThis is already a Musixmatch-notated file, silly!')


def get_keys_from_value(notation, val):
    return [k for k, v in notation.items() if v == val][0]


def find_files(search_path):
    result = []

    for root, direct, files in os.walk(search_path):
        for file in files:
            if file.endswith('.txt'):
                result.append(os.path.join(root, file))

    return result


main()
