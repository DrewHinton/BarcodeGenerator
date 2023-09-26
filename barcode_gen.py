# this program will read a input file. 
# map lines according to their item name
# posts to clipboard

from re import split
import sys
import os
import subprocess
    

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def getCopies(last):
    copies = 0

    # x at the end variable copies
    if(last[-1] == 'x'): # x at the very end
        if(is_integer(last[-3:-1])): # x at very end, but 2 digits before it [##]x
            copies = int(last[-3:-1])
        elif(last[-2].isdigit()): # x at end, but 1 digit before it. e.g. 5x
            copies = int(last[-2]) # get [5]x

    # double digit copies
    elif(len(last) > 1 and last[-3] == 'x'): # searches for: x[##]
        if(is_integer(last[-2:])):
            copies = int(last[-2:])

    elif(len(last) == 2 and is_integer(last[-2:])): # searches for: [##] without an x
        copies = int(last[-2:])

    # single digit copies
    elif(len(last) > 1 and last[-2] == 'x'): # x before the digit like x5
        if(last[-1].isdigit()):
            copies = int(last[-1])  # get last digit x[5]

    elif(len(last) == 1 and last[-1].isdigit()): # no x but is digit, 
        copies = int(last[-1])


    return copies

def run(filename, title, item_code, OVERRIDE_COPIES):

    tmpfilename = "_tmp_bc_args.txt"

    infile = open(filename)
    outfile = open(tmpfilename, 'w')

    _items = {}
    output = ""

    for line in infile:
        line = line.strip()
        
        if line == '': continue
        
        item = line
        if item not in _items:
            _items[item] = list()
        
        _items[item].append(line)

    # capitalize the first char of each word for title.
    lst = [word[0].upper() + word[1:] for word in str(title).split()]
    title = " ".join(lst)

    # header area
    output += "[HEADER START] ----------------------------------------\n"

    output += "\ntitle=" + title
    output += "\nitemcode=" + str(item_code)
    # output += "\ncwd=" + str(os.getcwd()) # cant pass cwd. bc_gen needs to know cwd to even read the tempfile
    

    output += "\n\n[HEADER END] ------------------------------------------\n"

    # build the list.
    for calls in sorted(_items.values()):

        for call in calls:
            output += '\n'
            print(call)

            words = call.split()
            first = words[0]
            last = words[-1].strip()

            no_copies = False
            copies = 0

            copies = getCopies(last)


            if copies == 0:
                no_copies = True


            if(no_copies == False):
                del words[-1]
                call = ' '.join(words)


            # this is for copies of a barcode.
            if (OVERRIDE_COPIES != -1):
                count = range(OVERRIDE_COPIES)
                for i in count:
                    output += call + " " + str(i) + '\n'
            elif (no_copies == False):
                # getting into this block means that you will pull the end-numbers from each line.
                # example allowed formats for end-numbers: 9, x9, 9x
                count = range(copies)
                for i in count:
                    output += call + " " + str(i) + '\n'
            else:
                output += call + '\n'

    
    outfile.write(output)

    infile.close()
    outfile.close()

    # call cmd line to start up msword -- i don't use the result code atm. still call it.
    result = subprocess.run(["winword", "/mbarcodegen", "barcode generator.docm"])

    os.remove(tmpfilename)

def process_args(argv, ref_args):
    error_badargs_msg = \
        '\n\tPlease provide arguments >> [! = required] [? = optional] <<\n\n\t' \
        'Permitted format: python [!filename] [!title=X] [!itemscode=X] [?copies=X]\n\n\t' \
        'e.g: > python items.txt itemscode=5 title="men\'s clothing"'


    # do not go above 8 flag bits.
    req_flags_sum = 0
    REQ_FLAG_TITLE = 1
    REQ_FLAG_ITEMSCODE = 2


    if len(argv) > 1:
        filename = str(sys.argv[1].lower())
        try:    
            tryfile = open(filename)
            tryfile.close()
            ref_args[FILENAME] = filename
        except:
            print("could not find file '" + filename + "'.")
            return False

        for i in range(2, len(sys.argv)):

            arg = str(sys.argv[i].lower())

            if(arg[ : arg.index('=')] == 'title'):
                ref_args[TITLE] = arg[arg.index('=') + 1: ]
                req_flags_sum += REQ_FLAG_TITLE
            
            if(arg[ : arg.index('=')] == 'itemscode'):
                ref_args[ITEM_CODE] = int(arg[arg.index('=') + 1: ])
                req_flags_sum += REQ_FLAG_ITEMSCODE

            if(arg[ : arg.index('=')] == 'copies'):
                ref_args[NUM_COPIES] = int(arg[arg.index('=') + 1: ])
        
    else:
        print(error_badargs_msg)
        return False

    if(req_flags_sum != 3):
        print(error_badargs_msg)
        print('\n\t>> missing args:', end=' ')
        
        binary_code = '{0:08b}'.format(req_flags_sum)

        if(binary_code[7] == '0'):
            print('title', end=' | ')

        if(binary_code[6] == '0'):
            print('itemscode')


        return False
    
    return True

if __name__ == "__main__":

    # args will be filename > title="w/e" > itemscode=X > copies=X
    # where:
    # filename = file holding the items
    # title = something like "womens clothing"
    # itemscode = 0-9
    # copies = overrides the numbers next to each item and generates x number of every item.
    
    FILENAME = 0
    TITLE = 1
    ITEM_CODE = 2
    NUM_COPIES = 3

    filename = ''
    title = ''
    item_code = -1
    num_copies = -1
    ref_args = [filename, title, item_code, num_copies]

    safe = process_args(sys.argv, ref_args)
    
    # print(ref_args[TITLE], ref_args[ITEM_CODE], ref_args[NUM_COPIES])
        
    # print(safe)

    if(safe):
        run(ref_args[FILENAME], ref_args[TITLE], ref_args[ITEM_CODE], ref_args[NUM_COPIES])
