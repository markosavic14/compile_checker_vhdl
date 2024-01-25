# -*- coding: utf-8 -*-
# Autor Marko Savic (markosavic14@gmail.com)
# April 2023.

import os

cirilica_velika_slova = {u'А' : u'A',
            u'Б' : u'B',
            u'Ц' : u'C',
            u'Ч' : u'C',
            u'Ћ' : u'C',
            u'Д' : u'D',
            u'Џ' : u'DZ',
            u'Ђ' : u'DJ',
            u'Е' : u'E',
            u'Ф' : u'F',
            u'Г' : u'G',
            u'Х' : u'H',
            u'И' : u'I',
            u'Ј' : u'J',
            u'К' : u'K',
            u'Л' : u'L',
            u'Љ' : u'LJ',
            u'М' : u'M',
            u'Н' : u'N',
            u'Њ' : u'NJ',
            u'О' : u'O',
            u'П' : u'P',
            u'Р' : u'R',
            u'С' : u'S',
            u'Ш' : u'S',
            u'Т' : u'T',
            u'У' : u'U',
            u'В' : u'V',
            u'З' : u'Z',
            u'Ж' : u'Z'}

cirilica_mala_slova = {u'а' : u'a',
            u'б' : u'b',
            u'ц' : u'c',
            u'ч' : u'c',
            u'ћ' : u'c',
            u'д' : u'D',
            u'џ' : u'dz',
            u'ђ' : u'dj',
            u'е' : u'e',
            u'ф' : u'f',
            u'г' : u'g',
            u'х' : u'h',
            u'и' : u'i',
            u'ј' : u'j',
            u'к' : u'k',
            u'л' : u'l',
            u'љ' : u'lj',
            u'м' : u'm',
            u'н' : u'n',
            u'њ' : u'nj',
            u'о' : u'o',
            u'п' : u'p',
            u'р' : u'r',
            u'с' : u's',
            u'ш' : u's',
            u'т' : u't',
            u'у' : u'u',
            u'в' : u'v',
            u'з' : u'z',
            u'ж' : u'z'}

latinica_dijakritici = {u'Č' : u'C',
                        u'č' : u'c',
                        u'Ć' : u'C',
                        u'ć' : u'c',
                        u'Đ' : u'DJ',
                        u'đ' : u'dj',
                        u'Š' : u'S',
                        u'š' : u's',
                        u'Ž' : u'Z',
                        u'ž' : u'z'}

def t_string(string):
    translit_string = ""
    for char in string:
        if char in cirilica_velika_slova.keys():
            translit_string += cirilica_velika_slova[char]
        elif char in cirilica_mala_slova.keys():
            translit_string += cirilica_mala_slova[char]
        elif char in latinica_dijakritici.keys():
            translit_string += latinica_dijakritici[char]
        else:
            translit_string += char

    return translit_string

def t_and_rename(path):
    for index, name_of_folder in enumerate(path):
        dir_normalised = t_string(name_of_folder)
        os.rename(name_of_folder, dir_normalised)
        path[index] = dir_normalised
