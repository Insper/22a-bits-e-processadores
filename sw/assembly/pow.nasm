; Arquivo: Pow.nasm
; Curso: Elementos de Sistemas
; Criado por: Luciano Soares
; Data: 27/03/2017

; Eleva ao quadrado o valor da RAM[1] e armazena o resultado na RAM[0].
; Só funciona com números positivos

leaw $R1, %A
movw (%A), %D
leaw $R0, %A
movw %D, (%A)
leaw $R2, %A
movw (%A), %D
incw %D
movw %D, (%A)

pow:
leaw $R2, %A
movw (%A), %D
leaw $R1, %A
subw (%A), %D, %D

leaw $FIM, %A
je %D
nop

leaw $R1, %A
movw (%A), %D
leaw $R0, %A
addw (%A), %D, %D
movw %D, (%A)
leaw $R2, %A
movw (%A), %D
incw %D
movw %D, (%A)

leaw $pow, %A
jmp
nop

FIM:
