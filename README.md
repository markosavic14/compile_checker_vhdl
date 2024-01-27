﻿# compile_checker_vhdl
Развијено за потрбе ЛПРС1 наставне групе.
Захтева Python i vcom алате. Vcom долази уз инсталацију Quartusa/Queste.
По потреби променити путању до алата унутар скрипте:
```
# Quartus -> C:/intelFPGA_lite/xx.x/modelsim_ase/win32aloem/
# Questa -> (C:/questasim64_xx.xx/win64/)
path_to_tool = 'C:/questasim64_2022.4/win64/'
```
Очекивано је да се унутар input фолдера налази подфолдер са радовима или произвољно дубоко угњежђених фолдера са радовима.
На пример:
```
Input
├───Grupa7
│   └───MarkoSavic
│       ├──zadatak.vhd
│       ├──zadatak_tb.vhd
└───Termin10h
    └───PetarPetrovic
        ├──zadatak.vhd
        ├──zadatak_tb.vhd
или
Input
├───MarkoSavic
│   ├──zadatak.vhd
│   ├──zadatak_tb.vhd
└───PetarPetrovic
    ├──zadatak.vhd
    ├──zadatak_tb.vhd
```
