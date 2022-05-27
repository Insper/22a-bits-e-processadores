; Arquivo: Div.nasm
; Curso: Elementos de Sistemas
; Criado por: Luciano Soares
; Data: 27/03/2017

; Divide R0 por R1 e armazena o resultado em R2.
; (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
; divisao para numeros inteiros positivos

leaw $R2, %A
movw $0, (%A)

loop:

leaw $R0, %A
movw (%A), %D ; valor R[0]

leaw $R1, %A
subw %D, (%A), %D ; R0 - R1
leaw $R0, %A
movw %D, (%A)

leaw $END, %A
jl %D
nop

leaw $R2, %A
movw (%A), %D
incw %D
movw %D, (%A)

leaw $loop, %A
jmp
nop

END:





































































