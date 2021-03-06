import os

__author__ = "Rahul Shah"
__status__ = "Development"
__credits__ = ["Rahul Shah", "Edward Bian"]

# Path to data directory
DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + "/../data/"

# holds all subsections in each chapter section along with the what holds

# w, h = 2, 100
# sorter_check = [[0 for _ in range(w)] for __ in range(h)]


def bracket_finder(word_to_search):
    """
    :param word_to_search:
    :return: The string between the first set of brackets
    """
    # This function is mainly for convenience and layered brackets
    first_bracket = True;
    first_bracket_location = 0;
    last_bracket_location = 0;
    layers = 0;
    counter = 0;
    for character_examined in word_to_search:
        if character_examined == "{" and first_bracket == True:
            first_bracket_location = word_to_search.index(character_examined)
            first_bracket = False;
        elif character_examined == "{" and first_bracket != True:
            layers += 1;
        elif character_examined == "}":
            if layers == 0:
                last_bracket_location = counter
            else:
                layers -= 1
        counter += 1
        # Goes through every character while recording layer to not extract the wrong string
    word_to_search2 = word_to_search[first_bracket_location + 1:last_bracket_location]
    for character_examined in word_to_search2:
        if character_examined.isalpha():
            first_char = word_to_search2.index(character_examined)
            return word_to_search2[first_char:]
        # This loop is for chapter sections that may start with numbers or other symbols, it makes the output start on the section name
    return word_to_search[first_bracket_location+1:last_bracket_location]


def chap_1_placer(chap1, kls, klsaddparas, cp1commands):
    """
    :param chap1: Chapter 1 text file
    :param kls: KLSadd, the addendum
    :param klsaddparas: Paragraphs that the code has identified to be sorted
    :return: Returns chapter 1 with the sections inserted into the right places from the introduction of KLSadd
             It's bascially a modified version of fix_chapter_sort
    """


    chapter_start = True
    index = 0
    kls_sub_chap1 = []
    kls_header_chap1 = []
    for item in kls:
        index += 1
        line = str(item)
        if "\\subsection" in line:
            temp = bracket_finder(line)
        if chapter_start and ("\\paragraph{" in line or "\\subsubsection*{" in line):
            for item in klsaddparas:
                if index < item:
                    klsloc = klsaddparas.index(item)
                    break
            t = ''.join(kls[index-1: klsaddparas[klsloc]])
            kls_sub_chap1.append(t)  # append the whole paragraph, every paragraph should end with a % comment
            kls_header_chap1.append(temp)  # append the name of subsection

            break
    intro_to_add = ''.join(kls_sub_chap1)
    chap1 = chap1[:len(chap1)-1]
    commentticker = 0

    # These commands mess up PDF reading and mus tbe commented out
    for line in cp1commands:
        prev_line = cp1commands[cp1commands.index(line) - 1]
        if "\\newcommand{\qhypK}[5]{\,\mbox{}_{#1}\phi_{#2}\!\left(" not in prev_line:
            if "\\newcommand\\half{\\frac12}" in line:
                linetoadd = "%" + line
                cp1commands[commentticker] = linetoadd

            elif "\\newcommand{\\hyp}[5]{\\,\\mbox{}_{#1}F_{#2}\\!\\left(" in line:
                linetoadd = "%" + line
                cp1commands[commentticker] = linetoadd

            elif "\\genfrac{}{}{0pt}{}{#3}{#4};#5\\right)}" in line:
                linetoadd = "%" + line
                cp1commands[commentticker] = linetoadd

            elif "\\newcommand{\\qhyp}[5]{\\,\\mbox{}_{#1}\\phi_{#2}\\!\\left(" in line:
                linetoadd = "%" + line
                cp1commands[commentticker] = linetoadd

        commentticker += 1
        if "\\newpage" in line and "\hbox{}" not in line:
            chap1[chap1.index(line)] = ""
        if '\myciteKLS' in line:
            linetoadd = line.replace('\myciteKLS', '\cite')
            cp1commands[commentticker] = linetoadd

    cp1commandsstring = ''.join(cp1commands)
    index = 0
    for word in chap1:
        index += 1
        if "\\newcommand" in chap1[index]:
            chap1[index - 1] = cp1commandsstring
            break
    ticker1 = 0
    # Formatting to make the Latex file run
    while ticker1 < len(chap1):
        if '\\myciteKLS' in chap1[ticker1]:
            chap1[ticker1] = chap1[ticker1].replace('\\myciteKLS', '\\cite')
        ticker1 += 1

    chap1 = ''.join(chap1)
    total_chap1 = chap1 + "\\paragraph{\\bf KLS Addendum: Generalities}" + intro_to_add + "\\end{document}"

    return total_chap1


def extraneous_section_deleter(entered_list):
    """
    Removes sections that are irrelevant and will slow or confuse the program

    :param entered_list: List of paragraphs
    :return: Extraneous name free output
    """
    # Returns the sections with unique names (per section) (as the following are often duplicated)
    return [item for item in entered_list if "reference" not in item.lower() and "limit relation" not in item.lower()
            and "symmetry" not in item.lower() and " hypergeometric representation" not in item.lower()]


def new_keywords(kls, kls_list):
    """
    This section checks through the Addendum and identifies words that are valid keywords of sections
    It then takes that list and removes duplicates, as well as printing the output to another file.

    :param kls: The addendum that provides the words.
    :param kls_list: List of identified keywords.
    :return: Outputs results as a list
    """

    kls_list_chap = []
    for item in kls:
        if "paragraph{" in item or "subsubsection*{" in item:
            kls_list.append(item[item.find("{") + 1: len(item) - 2])
    kls_list = extraneous_section_deleter(kls_list)

    kls_list.append("Limit Relation")
    for item in kls_list:
        if item not in kls_list_chap:
            kls_list_chap.append(item)
    #Preserves original kls_list, while allowing editting (special value is classed under symmetry)
    kls_list_chap[kls_list_chap.index("Special value")] = "Symmetry"
    kls_list_chap.append("Special value")
    w = 2
    h = len(kls_list_chap)+1
    #sorter_check tells the program which chapter the code is on and how many sections under a keyword have been sorted.
    sorter_check = [[0 for _ in range(w)] for __ in range(h)]
    return kls_list_chap, sorter_check


def fix_chapter_sort(kls, chap, word, sortloc, klsaddparas, sortmatch_2, tempref, sorter_check):
    """
    This function sorts through the input files and identifies and places sections from the addendum after their
    respective subsections in the chapter.

    :param kls: The addendum where the sections to be inserted are found.
    :param chap: The destination of inserted sections.
    :param word: The keyword that is being processed.
    :param sortloc: The location in the list of words, of the word being sorted.
    :param klsaddparas: Locations of possible sections
    :param sortmatch_2: Subsections that the program finds a match for in the chapter (a list of those that will be sorted)
    :return: This function outputs the processed chapter into a larger function for further processing.
    """
    hyper_headers_chap = []
    hyper_subs_chap = []


    special_input = 0
    name_chap = word.lower()
    if name_chap == "orthogonality":
        special_input = 1
    elif name_chap == "special value":
        special_input = 2
    elif name_chap == "symmetry":
        special_input = 3
    elif name_chap == "bilateral generating function":
        special_input = 4
    #These sections either share names with others or are categorized under others, so they must be processed specially

    khyper_header_chap = []
    k_hyper_sub_chap = []
    index = 0

    chapterstart = False
    for item in kls:
        index += 1
        line = str(item)
        if "\\subsection" in line:
            temp = bracket_finder(line)
            if temp.lower() == 'wilson':
                chapterstart = True
        if special_input in (0, 2, 4) and name_chap in line.lower() and chapterstart and ("\\paragraph{" in line or "\\subsubsection*{" in line) or \
        (special_input in (1, 3) and "orthogonality relation" not in line.lower() and name_chap in line.lower() and chapterstart
         and ("\\paragraph{" in line or "\\subsubsection*{" in line)):
            for item in klsaddparas:
                if index < item:
                    klsloc = klsaddparas.index(item)
                    break
            t = ''.join(kls[index: klsaddparas[klsloc]])
            k_hyper_sub_chap.append(t)  # append the whole paragraph, pray every paragraph ends with a % comment
            khyper_header_chap.append(temp)  # append the name of subsection

    for item in khyper_header_chap:
        if item == "Pseudo Jacobi (or Routh-Romanovski)":
            khyper_header_chap[khyper_header_chap.index(item)] = "Pseudo Jacobi"
    k_hyp_index_iii = 0
    offset = 0

    item = 0
    while item < len(khyper_header_chap):
        try:
            if khyper_header_chap[item] == khyper_header_chap[item + 1] and "generating functions" in name_chap:
                k_hyper_sub_chap[item + 1] = k_hyper_sub_chap[item] + "\paragraph{\\bf KLS Addendum: Bilateral generating functions}" + k_hyper_sub_chap[item + 1]
                khyper_header_chap[item] = "/x00"
                k_hyper_sub_chap[item] = "/x00"
                #/x00 is a filler character that must be unique, it can be changed, as long as the replacement isn't ever going to be an actual section
            elif khyper_header_chap[item] == khyper_header_chap[item+1]:
                k_hyper_sub_chap[item + 1] = k_hyper_sub_chap[item] + "\paragraph{\\bf KLS Addendum: " + \
                    word + "}" + k_hyper_sub_chap[item + 1]
                khyper_header_chap[item] = "/x00"
                k_hyper_sub_chap[item] = "/x00"
            else:
                item += 1
        except IndexError:
            item += 1

    temp_counter = 0
    while temp_counter < len(khyper_header_chap):
        if khyper_header_chap[temp_counter] == "/x00":
            del khyper_header_chap[temp_counter]
            del k_hyper_sub_chap[temp_counter]
        else:
            temp_counter += 1

    chap9 = 0

    if sorter_check[sortloc][0] == 0:
        sorter_check[sortloc][0] += 1
        chap9 = 1
    else:
        offset = sorter_check[sortloc][1]
        # if special_input == 1:
        #     offset = 8

    if special_input in (2, 3):
        name_chap = 'hypergeometric representation'


    # Uses of numbers like 12, or 9 are for specific lengths of strings (like \\subsection{) where the
    # section does not change
    '''
    '''
    for d in range(0, len(tempref)):  # check every section and subsection line
        item = tempref[d]
        line = str(chap[item])
        if "\\section{" in line or "\\subsection{" in line:
            if "\\subsection{" in line:
                temp = bracket_finder(line)
            else:
                temp = bracket_finder(line)

        if name_chap in line.lower():
            if special_input in (0, 2, 3, 4) or "orthogonality relation" not in line:
                hyper_subs_chap.append([tempref[d + 1]])  # appends the index for the line before following subsection
                hyper_headers_chap.append(temp)  # appends the name of the section the hypergeo subsection is in
                '''
                Section below should
                '''
                counteri = 0
                for i in khyper_header_chap:
                    i = i.replace(' I','~I')
                    khyper_header_chap[counteri] = i
                    counteri +=  1;

                if temp in khyper_header_chap:
                    try:
                        chap[tempref[d + 1] - 1] += "\paragraph{\\bf KLS Addendum: " + word + "}" + \
                                                    k_hyper_sub_chap[k_hyp_index_iii + offset]
                        if chap9 == 1:
                            sorter_check[sortloc][1] += 1
                        k_hyp_index_iii += 1
                        with open(DATA_DIR + "shiftedsections.tex", "a") as shifted:
                            shifted.write("KLS Addendum: " + word + " to " + temp + "\n")
                    except IndexError:
                        print chap[tempref[d+1] - 1]
                        print
                        print("Warning! Code has found an error involving section finding for '" + name_chap + "'.")

    if len(hyper_headers_chap) != 0:
        sortmatch_2.append(k_hyper_sub_chap)
    return chap


def cut_words(word_to_find, word_to_search_in):
    """
    This function checks through the outputs of later sections and removes duplicates, so that the output file does
    not have duplicates.

    :param word_to_find: Word that is being found
    :param word_to_search_in: The big word that is being searched
    :return: The big word without the word that was searched for
    """
    find_string = word_to_find
    search_string = word_to_search_in
    precheck = 1
    if find_string in search_string:
        if "\\paragraph{\\bf KLS Addendum: " in search_string or "\\subsubsection*{\\bf KLS Addendum: " in search_string:
            while True:
                if "\\paragraph{\\bf KLS Addendum: " in search_string[search_string.find(find_string)-precheck:search_string.find(find_string)] or \
                   "\\subsubsection*{\\bf KLS Addendum: " in search_string[search_string.find(find_string) - precheck:search_string.find(find_string)]:
                    return search_string[:search_string.find(find_string) - precheck] + search_string[search_string.find(find_string) + len(find_string):]
                else:
                    precheck += 1

        else:
            cut = search_string[:search_string.find(find_string)] + search_string[search_string.find(find_string) + len(find_string):]
            return cut
    else:
        return search_string


def prepare_for_pdf(chap):
    """
    Edits the chapter string sent to include hyperref, xparse, and cite packages

    :param chap: The chapter (9 or 14) that is being processed as a list of lines in each LaTeX chapter
    :return: The processed chapter, ready for additional processing
    """

    # (list) -> list
    foot_misc_index = 0
    for i, line in enumerate(chap):
        if "footmisc" in line:
            foot_misc_index += i + 1

    chap.insert(foot_misc_index, "\\usepackage[pdftex]{hyperref} \n\\usepackage {xparse} \n\\usepackage{cite} \n")
    #This is so things generate correctly
    return chap


def get_commands(kls, new_commands):
    """
    This method reads in relevant commands that are in KLS Addendum.tex and returns them as a list

    :param kls: The addendum is the source of what is being found
    :return:
    """
    index = 0
    for word in kls:
        index += 1
        if "smallskipamount" in word:
            new_commands.append(index - 1)
        if "mybibitem[1]" in word:
            new_commands.append(index)
    return kls[new_commands[0]:new_commands[1]]
    #Addendum needs these to generate correctly



def insert_commands(kls, chap, commands):
    """
    Inserts commands identified in previous functions.
    This method addresses the goal of hardcoding in the necessary comma vnds to let the chapter files run as pdf's.
    Currently only works with chapter 9

    :param kls: Addendum to look through
    :param chap: The chapter that is receiving commands (9 or 14) as a list of lines in each LaTeX chapter
    :param commands: Commands to be inserted
    :return: chap, processed
    """
    # reads in the newCommands[] and puts them in chap
    begin_index = -1  # the index of the "begin document" keyphrase, this is where the new commands need to be inserted.
    # find index of begin document in KLS Addendum
    index = 0

    for word in kls:
        index += 1
        if "begin{document}" in word:
            begin_index += index
    temp_index = 0

    for i in commands:
        chap.insert(begin_index + temp_index, i)
        temp_index += 1
    return chap
    #Puts the commands in the chapter so they do something


def find_references(chapter, chapticker, math_people):
    """
    This function searches the chapters and locates potential destinations of additions from the addendum.
    It puts these destinations in a list.

    :param chapter: The chapter being searched.
    :param chapticker: Which chapter is being searched (9 or 14).
    :return: List of references, ref9_3 and ref14_3 are references for chapter 9 and 14 specifically
    """
    ref9_3 = []
    ref14_3 = []
    references = []
    index = -1
    # chaptercheck designates which chapter is being searched for references
    chaptercheck = 0
    if chapticker == 9:
        chaptercheck = str(9)
    elif chapticker == 14:
        chaptercheck = str(14)
    # canAdd tells the program whether the next section is a reference
    add_next_section = False

    for word in chapter:
        index += 1
        special_detector = 1
        # check sections and subsections
        if("section{" in word or "subsection*{" in word) and ("subsubsection*{" not in word):
            processed_word = word[word.find("{")+1: word.find("}")]
            specially_formatted_word = word[word.find("{")+1: word.find("~")]
            if "bessel" in word.lower() and chapticker == 9:
                ref9_3.append(index)
            if ("big $q$-legendre" in word.lower() or "little $q$-legendre" in word.lower() or "continuous $q$-legendre" in word.lower()) and chapticker == 14:
                ref14_3.append(index)
            for unit in math_people:
                subunit = unit[unit.find(" ")+1: unit.find("#")]
                # System of checks that verifies if section is in chapter
                if (processed_word in subunit or specially_formatted_word in subunit) and (chaptercheck in unit) and len(processed_word) == len(subunit) or\
                ("Pseudo Jacobi" in processed_word and "Pseudo Jacobi (or Routh-Romanovski)" in subunit):
                    add_next_section = True
                    if chapticker == 9:
                        ref9_3.append(index)
                    elif chapticker == 14:
                        ref14_3.append(index)
                    special_detector = 0
        if "\\subsection*{References}" in word and add_next_section:
            # Appends valid locations
            references.append(index)
            if chapticker == 9:
                ref9_3.append(index)
            elif chapticker == 14:
                ref14_3.append(index)
            add_next_section = False
            #The if statement differentiates chapters 9 and 14
        if "subsection*{" in word and "References" not in word:
            if chapticker == 9:
                ref9_3.append(index)
            elif chapticker == 14:
                ref14_3.append(index)
        if "\\section{" in word and special_detector == 1 and chaptercheck == "14":
            w2 = word[word.find("{") + 1: word.find("}")]
            if "Bessel" not in w2:
                ref14_3.append(index)

    return references, ref9_3, ref14_3


def reference_placer(chap, references, p, chapticker2):
    """
    Places identified additions from the addendum list into the chapter list. The list returned will be turned into a
    string and written into the new text document

    :param chap: LaTeX Chapter receiving the additions, with each line an element of a list.
    :param references: List containing references to where subsections begin/end
    :param p: List containing additions to be added.
    :param chapticker2: Which chapter is being searched (9 or 14).
    :return: Returns the chapter, complete with additions
    """
    # count is used to represent the values in count
    count = 0
    # Tells which chapter it's on
    designator = 0
    if chapticker2 == 9:
        designator = "9."
    elif chapticker2 == 14:
        designator = "14."

    for i in references:
        # Place before References paragraph
        word1 = str(p[count])
        if designator in word1[word1.find("\\subsection*{") + 1: word1.find("}")]:
            chap[i - 2] += "%Begin KLS Addendum additions"
            if "In addition to the Chebyshev poly" in p[count]:
                chap[i - 2] += "\paragraph{\\bf KLS Addendum Addition}"
            chap[i - 2] += p[count]
            chap[i - 2] += "%End of KLS Addendum additions"

            count += 1
        else:
            while designator not in word1[word1.find("\\subsection*{") + 1: word1.find("}")]:
                word1 = str(p[count])
                if designator in word1[word1.find("\\subsection*{") + 1: word1.find("}")]:
                    chap[i - 2] += "%Begin KLS Addendum additions"
                    chap[i - 2] += p[count]
                    chap[i - 2] += "%End of KLS Addendum additions"
                    count += 1
                else:
                    count += 1

    return chap



def fix_chapter(chap, references, paragraphs_to_be_added, kls, kls_list_all, chapticker2, new_commands, klsaddparas, sortmatch_2, tempref, sorter_check):
    # method to change file string(actually a list right now), returns string to be written to file
    # If you write a method that changes something, it is preferred that you call the method in here
    """
    Removes specific lines stopping the latex file from converting into python, as well as running the
    functions responsible for sorting sections and placing the correct additions in the correct places

    :param chap: Chapter being processed.
    :param references: List containing references (used in reference placer).
    :param paragraphs_to_be_added: List containing additions to be added.
    :param kls: The addendum that contains sections to be added (not processed).
    :param kls_list_all: List of all identified keywords, fed into the chapter sorter.
    :param chapticker2: Which chapter is being searched (9 or 14).
    :return: entire chapter, with all other methods applied to it
    """

    sort_location = 0

    for name in kls_list_all:
        fix_chapter_sort(kls, chap, name, sort_location, klsaddparas, sortmatch_2, tempref, sorter_check)
        sort_location += 1

    for paragraph in range(len(paragraphs_to_be_added)):
        for subsection in sortmatch_2:
            for lines_in_subsection in subsection:
                if "%" == lines_in_subsection[-2]:
                     lines_in_subsection = lines_in_subsection[:-3]
                     #print "memes"
                     #print c
                elif "%" == lines_in_subsection[-1]:
                     lines_in_subsection = lines_in_subsection[:-2]
                # if "Formula (9.8.15) was first obtained by Brafman" in c and "Formula (9.8.15) was first obtained by Brafman"in paragraphs_to_be_added[a]:
                #     print c
                #     print "DING"
                #     print paragraphs_to_be_added[a]

                paragraphs_to_be_added[paragraph] = cut_words(lines_in_subsection, paragraphs_to_be_added[paragraph])

    reference_placer(chap, references, paragraphs_to_be_added, chapticker2)
    # Reference_placer is the one that does all the work
    # If anything needs to be done before commands are put in, do it here
    chap = prepare_for_pdf(chap)
    cms = get_commands(kls,new_commands)
    chap = insert_commands(kls, chap, cms)
    # The above 3 lines insert comments into the new revised chapter
    # The final output (addendum + chapter) is made here
    commentticker = 0

    # These commands mess up PDF reading and mus tbe commented out
    for line in chap:
        prev_line = chap[chap.index(line)-1]
        if "\\newcommand{\qhypK}[5]{\,\mbox{}_{#1}\phi_{#2}\!\left(" not in prev_line:
            if "\\newcommand\\half{\\frac12}" in line:
                linetoadd = "%" + line
                chap[commentticker] = linetoadd
            elif "\\newcommand{\\hyp}[5]{\\,\\mbox{}_{#1}F_{#2}\\!\\left(" in line:
                linetoadd = "%" + line
                chap[commentticker] = linetoadd
            elif "\\genfrac{}{}{0pt}{}{#3}{#4};#5\\right)}" in line:
                linetoadd = "%" + line
                chap[commentticker] = linetoadd
            elif "\\newcommand{\\qhyp}[5]{\\,\\mbox{}_{#1}\\phi_{#2}\\!\\left(" in line:
                linetoadd = "%" + line
                chap[commentticker] = linetoadd
        commentticker += 1
        if "\\newpage" in line and "\hbox{}" not in line:
            chap[chap.index(line)] = ""
    ticker1 = 0
    # Formatting to make the Latex file run
    while ticker1 < len(chap):
        if '\\myciteKLS' in chap[ticker1]:
            chap[ticker1] = chap[ticker1].replace('\\myciteKLS', '\\cite')
        ticker1 += 1
    return chap


def main(klsfile, klswrite9, klswrite14, klswrite1, klsread9, klsread14, klsread1):
    """
    Runs all of the other functions and outputs their results into an output file as well as putting together the list
    of additions that is fed into fix_chapter.

    """
    chap_nums = []
    new_commands = []  # used to hold the indexes of the commands

    # contains the locations of things with "paragraph{" in KLSadd, these are subsections that need to be sorted
    klsaddparas = []
    math_people = []

    # Stores all keywords
    kls_list_full = []

    sortmatch_2 = []

    # open the KLSadd file to do things with
    with open(DATA_DIR + klsfile, "r") as add:
        # store the file as a string
        addendum = add.readlines()
        kls_list_all = new_keywords(addendum, kls_list_full)[0]
        # Makes sections look like other sections
        sorter_check = new_keywords(addendum, kls_list_full)[1]

        for item in addendum:
            addendum[addendum.index(item)] = item.replace("\\eqref{","\\eqref{KLS Addendum: ")

        for word in addendum:
            if "paragraph{" in word:
                lenword = len(word) - 1
                temp = word[0:word.find("{") + 1] + "\\bf KLS Addendum: " + word[word.find("{") + 1: lenword]
                addendum[addendum.index(word)] = temp
            if "subsubsection*{" in word:
                lenword = len(word) - 1
                addendum[addendum.index(word)] = word[0:word.find("{") + 1] + "\\bf KLS Addendum: " + \
                word[word.find("{") + 1: lenword]
        index = 0
        indexes = []

        # Designates sections that need stuff added
        # gets the index
        startindex = 99999
        #number must be larger than all the others, thus 99999
        for word in addendum:
            index += 1
            if "." in word and "\\subsection*{" in word:
                if "9." in word:
                    chap_nums.append(9)
                    name = word[word.find("{") + 1: word.find("}")]
                    math_people.append(name + "#")
                if "14." in word:
                    chap_nums.append(14)
                    name = word[word.find("{") + 1: word.find("}")]
                    math_people.append(name + "#")
                if name == "9.1 Wilson":
                    #9.1 Wilson is here as it is the start of chapter 9, and where the introduction ends
                    startindex = addendum.index(word)
                indexes.append(index-1)
            if "paragraph{" in word and index > startindex-1:
                klsaddparas.append(index-1)
            if "subsub" in word and index > startindex-1:
                klsaddparas.append(index - 1)
            if "\subsection*{" in word and index > startindex-1:
                klsaddparas.append(index - 1)
            if "\\renewcommand{\\refname}{Standard references}" in word:
                klsaddparas.append(index-1)
                indexes.append(index - 1)

        # Looks for sections to sort
        # now indexes holds all of the places there is a section
        # using these indexes, get all of the words in between and add that to the paras[]
        paras = []

        for i in range(len(indexes)-1):

            box = ''.join(addendum[indexes[i]: indexes[i+1]-1])
            paras.append(box)


        # paras now holds the paragraphs that need to go into the chapter files, but they need to go in the appropriate
        # section(like Wilson, Racah, Hahn, etc.) so we use the mathPeople variable
        # we can use the section names to place the relevant paragraphs in the right place

        # parse both files 9 and 14 as strings

        with open(DATA_DIR + klsread1, "r") as ch1:
            entire1 = ch1.readlines()  # reads in as a list of strings

        cp1commands = get_commands(addendum, new_commands)
        with open(DATA_DIR + klswrite1, "w") as temp1:
            temp1.write(chap_1_placer(entire1, addendum, klsaddparas, cp1commands))


        # chapter 9
        with open(DATA_DIR + klsread9, "r") as ch9:
            entire9 = ch9.readlines()  # reads in as a list of strings

        # chapter 14
        with open(DATA_DIR + klsread14, "r") as ch14:
            entire14 = ch14.readlines()

        # call the findReferences method to find the index of the References paragraph in the two file strings
        # two variables for the references lists one for chapter 9 one for chapter 14

        chapticker = 9
        references9 = find_references(entire9, chapticker, math_people)
        ref9_3 = references9[1]
        references9 = references9[0]
        chapticker = 14
        references14 = find_references(entire14, chapticker, math_people)
        ref14_3 = references14[2]
        references14 = references14[0]



        # call the fixChapter method to get a list with the addendum paragraphs added in

        chapticker2 = 9
        str9 = ''.join(fix_chapter(entire9, references9, paras, addendum, kls_list_all, chapticker2, new_commands, klsaddparas, sortmatch_2, ref9_3, sorter_check))

        chapticker2 = 14
        str14 = ''.join(fix_chapter(entire14, references14, paras, addendum, kls_list_all, chapticker2, new_commands, klsaddparas, sortmatch_2, ref14_3, sorter_check))



    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # If you are writing something that will make a change to the chapter files, write it BEFORE this line, this part
    # is where the lists representing the words/strings in the chapter are joined together and updated as a string!
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # write to files
    # new output files for safety
    with open(DATA_DIR + klswrite9, "w") as temp9:
        temp9.write(str9)

    with open(DATA_DIR + klswrite14, "w") as temp14:
        temp14.write(str14)

    print "Files sorted"
    # Will print when code done

if __name__ == '__main__':
    main("KLSaddII.tex", "updated9.tex", "updated14.tex", "updated1.tex", "chap09.tex", "chap14.tex", "chap01.tex")