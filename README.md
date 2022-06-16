# bits e proc


``` bash
#gera hack de um único arquivo nasm
./bits.py assembler from-nasm sw/assembly/add.nasm add.hack

#gera hack de pasta
 ./bits.py assembler from-dir ./sw/assembly/ ./sw/hack

# gera hack de arquivo de config
./bits.py assembler from-config sw/nasm_config.yml

# testa assembly no hw
./bits.py hw from-config sw/nasm_config.yml
```
