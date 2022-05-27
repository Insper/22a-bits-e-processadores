; ------------------------------------
; Calcule a média dos valores de um vetor
; que possui inicio em RAM[5] e tamanho
; defindo em RAM[4],
;
; 1. Salve a soma em RAM[1]
; 2. Salve a média em RAM[0]
; 
; ------------------------------------
; antes       | depois
;             |
; RAM[0]:     | RAM[0]:  2  : média 
; RAM[1]:     | RAM[1]:  8  : soma
; RAM[2]:     | RAM[2]:  
; RAM[3]:     | RAM[3]:  
; RAM[4]:  4  | RAM[4]:  4 
; RAM[5]:  1  | RAM[5]:  1 - 
; RAM[6]:  2  | RAM[6]:  2 | vetor
; RAM[7]:  1  | RAM[7]:  1 |
; RAM[8]:  4  | RAM[8]:  4 -
; ------------------------------------

leaw $5, %A
movw %A, %D
leaw $2, %A
movw %D, (%A)              ;inicia soma do vetor no ram[5] e guarda posição atual na ram[2]

leaw $4, %A
movw (%A), %D
leaw $3, %A
movw %D, (%A)               ; faz uma copia do valor de ram[4] para ram[3]

SOMA:
leaw $3, %A
movw (%A), %D

leaw $MEDIA, %A             ;se ram[3]=0 então calcula-se a média
je %D
nop

leaw $2, %A
movw (%A), %A
movw (%A), %D
leaw $1, %A
addw (%A), %D, %D
movw %D, (%A)               ;armazena soma em ram[1]

leaw $2, %A
movw (%A), %D
incw %D
movw %D, (%A)               ;incrementa ram[2]

leaw $3, %A
movw (%A), %D
decw %D
movw %D, (%A)               ;decrementa ram[3]

leaw $SOMA, %A
jmp
nop

MEDIA:
leaw $1, %A
movw (%A), %D
leaw $2, %A
movw %D, (%A)               ;faz uma copia da soma em ram[1] para ram[2]

SUBTRACAO:
leaw $2, %A
movw (%A), %D
leaw $4, %A
subw %D, (%A), %D
leaw $POSITIVO, %A
jge %D                  ;Salta se o resultado da subtração é positivo
nop

leaw $FIM, %A           ;Termina a operação se o resultado da subtração é negativo
jmp
nop

POSITIVO:
leaw $2, %A
movw %D, (%A)           ;resultado da subtração é novo valor de ram[2]
leaw $0, %A
movw (%A), %D
incw %D
movw %D, (%A)           ;Incrementa ram[0] para cada subtração realizada
leaw $SUBTRACAO, %A
jmp                     ;Retorna para subtração em novo ciclo
nop

FIM:
