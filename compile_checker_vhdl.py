# version: 0.1
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
from shutil import rmtree, copy
from dependencies import transliterate

path_to_tool = 'C:/questasim64_2022.4/win64/'   # putanja do vcom i vlib alata (Quartus -> C:/intelFPGA_lite/xx.x/modelsim_ase/win32aloem/)
                                                # Questa -> (C:/questasim64_xx.xx/win64/)
filename = 'GrupaA'                             # npr GrupaA -- bez .vhd ekstenzije i bez _tb sufiksa

#ostavljam funkciju u slucaju ukoliko bi bilo potrebo da se sufiks obrise iz naziva datoteke (npr _assignsubmission_file_)
def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s


if __name__ == "__main__":
    if not os.path.exists('input/'):
        print("Ne postoji input folder")
        exit(1)

    # ukoliko vec postoji folder output, obrisi njegov sadrzaj
    if os.path.exists('output/'):
        for path in Path('output/').glob("**/*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
        rmtree('output/')

    os.makedirs('output/')

    os.chdir('input/')
    input_subdir = [name for name in os.listdir('.') if os.path.isdir(name)] # pokupi sve subfoldere unutar foldera input (npr Termin10h, Termin12h itd.)
    for index, name_of_folder in enumerate(input_subdir):
        dir_normalised = transliterate.transliterate(name_of_folder)        # transliteracija cirilicnih i latinicnih slova sa dijakriticima na "osisanu latinicu"
        os.rename(name_of_folder, dir_normalised)
        input_subdir[index] = dir_normalised

    all_subdirs = {}
    for dir in input_subdir:                     # pokupi sve subfoldere (foldere stud. resenja) unutar foldera po terminima (Termin10h, Termin12h itd.)
        os.chdir('{dir}/'.format(dir=dir))
        subdir = [name for name in os.listdir('.') if os.path.isdir(name)]
        for index, name_of_folder in enumerate(subdir):
            dir_normalised = transliterate.transliterate(name_of_folder)  # transliterate diacritics and cyrilic letters
            os.rename(name_of_folder, dir_normalised)
            subdir[index] = dir_normalised
        all_subdirs[dir] = subdir
        os.chdir('../')

    os.chdir('../')
    

    os.system(f"{path_to_tool}vlib.exe work")
    
    # ukoliko se rad ne kompajlira prekopirati na output/folder_termina/compile_fail/student/
    # ukoliko se rad kompajlira prekopirati na output/folder_termina/compile_pass/student/
    for super_dir in all_subdirs:
        os.makedirs(f'output/{super_dir}')
        os.makedirs(f'output/{super_dir}/compile_fail')
        os.makedirs(f'output/{super_dir}/compile_pass')
        for dir in all_subdirs[super_dir]:
            if (os.system(path_to_tool + f'vcom.exe "input/{super_dir}/{dir}/{filename}.vhd" "input/{super_dir}/{dir}/{filename}_tb.vhd"')):
                os.makedirs(f'output/{super_dir}/compile_fail/{dir}/')
                copy(f"input/{super_dir}/{dir}/GrupaA.vhd",
                     f"output/{super_dir}/compile_fail/{dir}/GrupaA.vhd")
                copy(f"input/{super_dir}/{dir}/GrupaA_tb.vhd",
                     f"output/{super_dir}/compile_fail/{dir}/GrupaA_tb.vhd")
            else:
                os.makedirs(f'output/{super_dir}/compile_pass/{dir}/')
                copy(f"input/{super_dir}/{dir}/GrupaA.vhd",
                     f"output/{super_dir}/compile_pass/{dir}/GrupaA.vhd")
                copy(f"input/{super_dir}/{dir}/GrupaA_tb.vhd",
                     f"output/{super_dir}/compile_pass/{dir}/GrupaA_tb.vhd")

    # po zavrsetku skripte izbrisi radni folder vcom alata
    if os.path.exists('work/'):
        for path in Path('work/').glob("*"):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                rmtree(path)
        rmtree('work/')
