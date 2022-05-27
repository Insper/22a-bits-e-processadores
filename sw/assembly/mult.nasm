; Arquivo: Abs.nasm
; Curso: Elementos de Sistemas
; Criado por: Luciano Soares
; Data: 27/03/2017

; Multiplica o valor de RAM[1] com RAM[0] salvando em RAM[3]

leaw $3, %A
movw $0, (%A)

loop:

  leaw $0, %A
  movw (%A), %D

  ; Verifica se RAM[0] = 0
  leaw $end, %A 
  jle
  nop

  ; Soma RAM[3] = RAM[3] + RAM[1]
  leaw $3, %A
  movw (%A), %D
  leaw $1, %A
  movw (%A), %A
  addw %D, %A, %D
  leaw $3, %A
  movw %D, (%A)

  ; subtrai RAM[0] = RAM[0] - 1
  leaw $0, %A
  movw (%A), %D
  decw %D
  movw %D, (%A)

  ; loop
  leaw $loop, %A
  jmp
  nop

end:


