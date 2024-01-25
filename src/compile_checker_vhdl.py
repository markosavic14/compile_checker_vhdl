# version: 0.2c
# autor Marko Savic (markosavic14@gmail.com)
# Januar 2023.
# za potrebe LPRS1 nastavne grupe
#
# zahteva python i vcom+vlib (dolaze uz instalaciju quartusa/queste)
# pokrenuti sa admin pravima (preimenuje datoteke, moze da baci gresku ako nema prava)
# skripta pisana i testirana na Windowsu
# po potrebi izmeniti path_to_tool string

import os
import subprocess
from pathlib import Path
from shutil import rmtree, copy, copytree
import transliterate

# putanja do alata
# Quartus -> C:/intelFPGA_lite/xx.x/modelsim_ase/win32aloem/
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
            return text[:len(text) - (i + 1)]


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
    transliterate.t_and_rename(subfiles)            # transliteracija cirilice i slova sa dijakriticima
    ret_str = []
    for s_file in subfiles:
        if os.path.isdir(f"{s_file}"):
            m_dfs(f'{s_file}/', tree, filepath)
        elif 1 <= len(subfiles) <= 4:
            if s_file.endswith('.vhd'):
                ret_str.append(filepath + s_file)
        else:
            print(s_file)
            print("Nepravilna struktura foldera.")
    if len(ret_str) != 0:
        tree.append(ret_str)
    os.chdir("../")


def make_subfolders(dst):
    if not os.path.exists(dst):
        for i, char in enumerate(dst):
            if char == '/':
                temp = dst[:i]
                dst = dst[i + 1:]
                if not os.path.exists(temp):
                    os.makedirs(temp)
                os.chdir(temp)
                if dst != '':
                    make_subfolders(dst)
                os.chdir('../')
                break


# dodati output u string

def copy_tree(src, dst):
    for s_file in src:
        text = s_file
        for i, char in enumerate(reversed(text)):
            if char == '/':
                temp_src = text[:len(text) - i]
                make_subfolders('output/' + dst + temp_src[5:])
                copy(s_file, 'output/' + dst + s_file[5:])
                break


if __name__ == "__main__":
    #os.chdir("../")        # po potrebi zakomentarisati ukoliko se skripta pokrece rucno a ne preko run.bat skripte

    # Provera da li postoji input folder i da li je popunjen
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

    # napravi radni folder za alat, ako i output folder
    subprocess.run(f"{path_to_tool}vlib.exe work")
    os.makedirs('output/')

    for file in file_tree:
        instr = path_to_tool + 'vcom.exe'
        for elem in file:
            instr += f' "{elem}"'

        ret = subprocess.run(instr, capture_output=True);
        if ret.returncode:
            copy_tree(file, 'comp_fail')
            print(file[0] + '\n' + file[1])
            print("COMP FAIL")
        else:
            copy_tree(file, 'comp_pass')
            print(file[0] + '\n' + file[1])
            print("COMP PASS")

        print('\n############################\n')

    # po zavrsetku skripte izbrisi radni folder vcom alata
    rm_folder_and_conts('work/')
