# compile_checker_vhdl
Захтева Python i vcom алате. Vcom долази уз инсталацију Quartusa/Queste.
Очекивано је да се унутар input фолдера налази подфолдер са радовима или угњежђен фолдер са радовима.
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