; Arquivo: stringLength.nasm
; Curso: Elementos de Sistemas
; Criado por: Rafael Corsi 
; Data: 28/03/2018
;
; Assuma que uma string é um conjunto de caracteres terminado
; em NULL (0).
; 
; Supondo que temos uma string que começa no endereço 8 da RAM.
; Calcule o seu tamanho e salve o resultado na RAM[0].
;
; Os caracteres estão formatados em ASCII
; http://sticksandstones.kstrom.com/appen.html
; 
; Exemplo:
;
;   Convertido para ASCII
;             |
;             v
;  RAM[8]  = `o`
;  RAM[9]  = `i`
;  RAM[10] = ` `
;  RAM[11] = `b`
;  RAM[12] =  l`
;  RAM[13] = `z`
;  RAM[14] = `?`
;  RAM[15] = NULL = 0x0000



leaw $7, %A
movw %A, %D
leaw $2 ,%A
movw %D, (%A);ram[2]=7

leaw $0 ,%A
movw $0, (%A)

LOOP:

leaw $2, %A
movw (%A), %D ;d=8
addw %D, $1,%D
movw %D, (%A)
leaw $2, %A
movw (%A), %D
movw %D, %A
movw (%A), %D
leaw $ELSE, %A
je %D
nop

leaw $0,%A
movw (%A),%D
addw $1,%D,%D
movw %D,(%A)
leaw $LOOP,%A
jmp
nop
ELSE:
