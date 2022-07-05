# B - Lógica Combinacional

| Data da entrega |
|-----------------|
| ??              |

- Arquivo: `hw/components.py`

![](figs/LogiComb/sistema-comb.svg)

!!! tip "Scrum Master"
    Você é `Scrum Master` e não sabe por onde começar? De uma olhada nessas dicas: [Vixi! Sou Scrum Master](https://insper.github.io/Z01.1/Util-vixi-sou-scrum/)

Esse projeto tem como objetivo trabalhar com portas lógicas e sistemas digitais combinacionais (sem um clock) em FPGA e MyHDL. Os elementos lógicos desenvolvidos nessa etapa serão utilizados como elementos básicos para a construção do computador. 

## Instruções

O desenvolvimento será na linguagem MyHDL, o grupo deve se organizar para implementar todos os elementos propostos. O facilitador escolhido será responsável pela completude e consistência do branch master do grupo.

### Integrantes
    
Tarefas devem ser criadas no **Issues** e atribuídas aos demais colegas.
As tarefas devem ser resolvidas individualmente! Utilize a ajuda de seus colegas, mas resolva o que foi atribuído a vocês, essa é sua tarefa/ responsabilidade! 
    
!!! warning
    Este  projeto é para ser realizado por todos os integrantes do grupo em seus próprios computadores, quem não participar, não implementar os módulos que foram atribuídos, ou não realizar pull-request não ganhará nota de participação individual.
    
### Controle de Tarefas e Repositório

Nas discussões com os outros colegas o scrum master deve definir os módulos que cada um do grupo irá desenvolver. Crie uma rotina para commits e pull-request. Sempre teste os módulos e verifique se está fazendo o esperado.

=== "Facilitador (Scrum Master)"
    - Fazer a **atualização** do fork com o upstream
    - Organizar o **github + issues + project**
    - Gerenciar o grupo (atribuir tarefas)
    - **Gerenciar os pull-requests**
    - Criar relatório da performance de cada um do grupo
    - Entregar/Apresentar o projeto no final 

=== "Desenvolvedores"
    - Realizar as tarefas atribuidas pelo scrum-master
    - Ajudar na entrega final 
    - Testar os códigos
    - Realizar os pull-requests

### Testes CI

Cada desenvolvedor além de editar o arquivo `hw/components.py` deve editar o arquivo `.github/` ....

## Entrega

A entrega **final** deve ser feita no ramo `master` do git.

- [ ] Implementar todos os módulos listados
- [ ] Todos os módulos devem passar nos testes
- [ ] Actions deve estar configurado e funcionando

### Conceito C+

- AND 16 bits
    - **block**   : `and16`
    - **Descrição** : And bit a bit entre duas palavras de 16 bits.
 
- OR de 16 bits
    - **block**   : `or8way`
    - **Descrição** : OR entre as 8 entradas.
 
- OR 8 Way  
    - **block**   : `or8way`
    - **Descrição** : OR entre 8 bits, resulta em uma única saída
    
- Barrel Shifter
    - **block**   : `barrelShifter`
    - **Descrição** : 
    
- Demultiplexador de 2 saídas 
    - **block**   : `DMux2Way.`
    - **Descrição** : Demultiplexa uma entrada binária em duas saídas.
    
- Demultiplexador de 4 saídas
    - **block**   : `DMux4Way.`
    - **Descrição** : Demultiplexa uma entrada binária em quatro saídas.
    
- Demultiplexador de 8 saídas
    - **block**   : `DMux8Way.`
    - **Descrição** : Demultiplexa uma entrada binária em oito saídas.
    
- Multiplexador de duas entradas de 16 bits 
    - **block**   : `Mux16.`
    - **Descrição** : Multiplexa duas entradas de 16 bits para uma de 16 bits.
    
-  Multiplexador 2 entradas de um bit cada
    - **block**   : `Mux2Way.`
    - **Descrição** : Multiplexa 2 entradas binárias em uma saída binária
    
-  Multiplexador 4 entradas de um bit cada
    - **block**   : `Mux4Way.`
    - **Descrição** : Multiplexa 4 entradas binárias em uma saída binária
    
-  Multiplexador 8 entradas de um bit cada
    - **block**   : `Mux8Way.`
    - **Descrição** : Multiplexa 8 entradas binárias em uma saída binária
    
-  Multiplexador 4 entradas de 16 bits cada
    - **block**   : `Mux4Way16.`
    - **Descrição** : Multiplexa 4 entradas de 16 bits cada em uma saída de 16 bits.
    
-  Multiplexador 8 entradas de 16 bits cada
    - **block**   : `Mux8Way16`

-  Deslocador de bits
    - **block**   : `BarrelShifter16.vhd`


### Conceito B+

- Circuito lógico 
    - **Arquivo** : `circuito.vhd`
    - **Descrição**: Primeira questão da lista de exercícios [Álgebra Booleana 2](https://insper.github.io/Z01.1/Exercicio-Algebra-Booleana-2/)

- Detector de moedas
    - **Arquivo** : `detectorDeMoedas.vhd`
    - **Descrição**: Questão do detector de moedas da lista de exercícios [Álgebra Booleana 2](https://insper.github.io/Z01.1/Exercicio-Algebra-Booleana-2/)

- Impressora
    - **Arquivo** : `impressora.vhd`
    - **Descrição**: Questão da impressora da lista de exercícios [Álgebra Booleana 2](https://insper.github.io/Z01.1/Exercicio-Algebra-Booleana-2/)

- Display de 7s
    - **Arquivo**: `sevenSeg.vhd'
    - **Descrição**: Questão do display de sete segmentos da lista de exercícios [Álgebra Booleana 2](https://insper.github.io/Z01.1/Exercicio-Algebra-Booleana-2/)

!!! tip "Display 7s"
    1. Esse item é uma continuação do que foi realizado no [Lab4](/LogiComb-Lab-1/), onde vocês tiveram que exibir um valor constante no display de 7s. 
    1. Para cada segmento do display, vocês devem encontrar uma equação booleana que o represente, e então implementar em VHDL e testar na FPGA.
<!--
- O grupo deve apresentar um vídeo da FPGA mostrando nos display de 7 segmentos o seguinte:
    - (C) O valor em hexadecimal da palavra binária formada pelas chaves SW(3 .. 0)
    - (C) O valor em hexadecimal da palavra binária formada pelas chaves SW(9 .. 0)
    - (B) O valor em decimal da palavra binária formada pelas chaves SW(9 .. 0)
-->

## Rubricas para avaliação do projeto

Cada integrante do grupo irá receber duas notas: Uma referente ao desenvolvimento total do projeto (Projeto) e outra referente a sua participação individual no grupo.

### Grupo


Para atingir os objetivos A e B, deve-se antes atingir o C.

| Conceito | Descritivo                                                  |
|----------|-------------------------------------------------------------|
| **A+**   | Exibe três dígitos em Hexadecimal na FPGA - anexar video ao repositório                  |
|          | (exibir até o valor 0x3FF = 2^10 - 1)                       |
| **B+**   | Módulos adicionais implementados e funcionado (circuito, detector de moedas, impressora) |
|          | Implementar um único display de 7s (conta de 0x0 0xF) - anexar video ao repositório |
| **C+**   | Ter criado o project no github                              |
|          | Actions configurado e funcionando                           |
|          | Todos os módulos básicos implementados e funcionado         |
| **D**    | Até dois Módulos com falha/ não apresentou o vídeo da FPGA  |
| **I**    | Mais de três módulos com falha                              |
    

### Individual

As rubricas a serem seguidas serão comuns a todos os projeto e está descrito no link:

- [Rubricas Scrum e Desenvolvedor](/Z01.1/Sobre-Rubricas/)

### Formulários
- [Scrum Master](https://forms.gle/LqmbrhUFbxpEhubSA)
- [Desenvolvedores](https://forms.gle/jTrSaBegjKZZF6za6)
