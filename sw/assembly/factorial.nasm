; Arquivo: Factorial.nasm
; Curso: Elementos de Sistemas
; Criado por: Luciano Soares
; Data: 27/03/2017

; Calcula o fatorial do número em R0 e armazena o valor em R1.


leaw $0, %A
movw (%A), %D
leaw $ZERO, %A
je %D
nop
subw %D, $1, %D
leaw $2, %A
movw %D, (%A)
leaw $3, %A
movw %D, (%A)
LOOPout:
LOOPin:
leaw $0, %A
movw (%A), %D
leaw $1, %A
addw (%A), %D, %D
movw %D, (%A)
leaw $2, %A
subw (%A), $1, %D
movw %D, (%A)
leaw $LOOPin, %A
jg %D
nop
leaw $1, %A
movw (%A), %D
leaw $0, %A
movw %D, (%A)
leaw $1, %A
movw $0, %D
movw %D, (%A)
leaw $3, %A
subw (%A), $1, %D
movw %D, (%A)
leaw $2, %A
movw %D, (%A)
leaw $LOOPout, %A
jg %D
nop
leaw $END, %A
jmp
nop
ZERO:
leaw $0, %A
movw $1, %D
movw %D, (%A)
END:
leaw $0, %A
movw (%A), %D
leaw $1, %A
movw %D, (%A)
