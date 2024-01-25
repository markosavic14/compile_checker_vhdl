# version: 0.2
# autor Marko Savic (markosavic14@gmail.com)
# Januar 2023.
# za potrebe LPRS1 nastavne grupe
#
# zahteva python i vcom+vlib (dolaze uz instalaciju quartusa/queste)
# pokrenuti sa admin pravima (preimenuje datoteke, moze da baci gresku ako nema prava)
# skripta pisana i testirana na Windowsu
# po potrebi izmeniti path_to_tool i filename stringove

import os
from pathlib import Path
from shutil import rmtree, copy, copytree
import transliterate

# putanja do vcom i vlib alata
# (Quartus -> C:/intelFPGA_lite/xx.x/modelsim_ase/win32aloem/)
# Questa -> (C:/questasim64_xx.xx/win64/)
path_to_tool = 'C:/questasim64_2022.4/win64/'


# ostavljam funkciju ukoliko bi bilo potrebno da se sufiks obrise iz naziva datoteke (npr _assignsubmission_file_)
def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s


def strip_end(text, split_char):
    for i, char in enumerate(reversed(text)):
        if char == split_char:
            return text[:len(text)- (i+1)]

def rm_folder_and_conts(name):
    if os.path.exists(name):
        for path in Path(name).glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
        rmtree(name)


def m_dfs(s, tree, filepath=""):
    filepath += s
    os.chdir(s)
    subfiles = [name for name in os.listdir('.')]
    transliterate.t_and_rename(subfiles)
    ret_str = []
    for file in subfiles:
        if os.path.isdir(f"{file}"):
            m_dfs(f'{file}/', tree, filepath)
        elif 1 <= len(subfiles) <= 3:
            if file.endswith('.vhd'):
                ret_str.append(filepath + file)
        else:
            print("Nepravilan broj datoteka unutar foldera.")
    if len(ret_str) != 0:
        tree.append(ret_str)
    os.chdir("../")


def make_subfolders(dst):
    if not os.path.exists(dst):
        for i, char in enumerate(dst):
            if char == '/':
                temp = dst[:i]
                dst = dst[i+1:]
                if not os.path.exists(temp):
                    os.makedirs(temp)
                os.chdir(temp)
                if dst != '':
                    make_subfolders(dst)
                os.chdir('../')
                break

#dodati output u string

def copy_tree(src, dst):
        for file in src:
            text = file
            for i, char in enumerate(reversed(text)):
                if char == '/':
                    temp_filename = text[len(text) - i:]
                    temp_src = text[:len(text) - i]
                    make_subfolders('output/' + dst + temp_src[5:])
                    copy(file, 'output/' + dst + file[5:])
                    break

if __name__ == "__main__":
    os.chdir("../")
    if not os.path.exists('input/'):
        print("Ne postoji input folder")
        exit(1)
    elif len(os.listdir('input/')) == 0:
        print("Input folder je prazan")
        exit(1)

    # ukoliko vec postoji folder output, obrisi njegov sadrzaj
    rm_folder_and_conts('output/')

    # modifikovani algoritam rekurzivne pretrage po dubini za prikupljanje putanje do vhd datoteka
    file_tree = []
    m_dfs('input/', tree=file_tree)

    #napravi radni folder za alat, ako i output folder
    os.system(f"{path_to_tool}vlib.exe work")
    os.makedirs('output/')

    for file in file_tree:
        instr = path_to_tool + 'vcom.exe'
        for elem in file:
            instr += f' "{elem}"'

        if os.system(instr):
            copy_tree(file, 'comp_fail')
        else:
            copy_tree(file, 'comp_pass')

    # po zavrsetku skripte izbrisi radni folder vcom alata
    rm_folder_and_conts('work/')
