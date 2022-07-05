# Lab 5: MyHDL

Leitura prévia necessária:

- `MyHDL/MyHDL Básico`
- `Teoria/FPGA` (TODO)

Este laboratório é introdutório para o desenvolvimento do projeto ([`Lógica-Combinacional`](/bits-e-proc/class/logiComb-Projeto)), onde iremos criar componentes de hardware que serão os alicerces do nosso computador. Primeiro precisamos praticar um pouco de `MyHDL` e entender a ferramenta e o fluxo de compilação, teste e como conseguimos executar o hardware em uma FPGA.

Os exercícios dos laboratórios estão localizados no repositório:  https://github.com/rafaelcorsi/bits-e-proc-labs, cada aluno de forma individual deve realizar um fork do repositório e trabalhar individualmente nele. Os laboratórios não po ffssuem entregas, mas devem ser realizados para estudo.

!!! exercise
    1. Realize um fork do repositório de labs
    1. Clone o repositório para a sua máquina
    
!!! exercise
    Nós iremos trabalhar sempre com um ambiente virtual do python 3.8, para isso será necessário realizar as seguintes operações ==dentro da pasta clonada==:

    ```
    python3.8 -m venv env
    . env/bin/activate
    pip3 install -r requirements.txt
    ```

!!! warning 
    Sempre que for abrir um terminal novo e acessar a pasta, será necessário ativar o ambiente virtual:
   
    ```
    . env/bin/activate
    ```
    
    Se for utilizar o VSCODE para fazer o desenvolvimento dos projetos e exercícios, basta abrir a pasta raiz do repositório que o code já utiliza o ambiente virtual (eu criei o arquivo `.vscode/settings.json` que configura isso.)
    
!!! progress
    Começando o laboratório.

### pytest

Bits e Processadores utiliza uma metodologia de desenvolvimento de projeto chamada de **test driven development (TDD)**, ou seja, para cada etapa do projeto teremos um teste associado a ele. Os testes podem ser do tipo unitário e de integraćão. Para realizarmos os testes em python utilizaremos o módulo `pytest` e o plugin de dev-life (para fazer o report do progresso de vocês para o servidor).

Cada exercício possui um arquivo com o prefixo `test_` que excita o componente que vocês irão desenvolver e valida a saída esperada. 

## Praticando - Parte 1

Vamos comecar descrevendo algumas circuitos lógicos combinacionais bem simples em MyHDL. 

!!! exercise
    Para cada exercício implemente a solucão no arquivo `componente.py` e teste com `pytest`. A descricão do exercício está no próprio arquivo.

    - [ ]  `logComb/exe1`
    - [ ]  `logComb/exe2`
    - [ ]  `logComb/exe3`

## Rodando na FPGA

Agora vamos entender como conseguimos usar o nosso hardware descrito em `MyHDL` em um hardware real (FPGA), para isso temos que primeiro converter o `MyHDL` para `VHDL` e então usar a ferramenta da Intel (Quartus) para **sinterizar** o nosso hardware. Depois disso temos que programar a FPGA.

Notem que agora o nosso módulo precisa ler e acionar pinos (interface com o mundo externo), normalmente a última camada de um projeto de hardware (aquela que realmente acessa os pinos) é chamada de toplevel. Os pinos dessa camada possuem nomes fixos, por isso temos que mapear os pinos do HW para os sinais do nosso módulo. Nessa primeira etapa iremos utilizar os seguintes componentes da nossa placa:

![](figs/logComb-new/toplevel.png)

Onde:

- `LED`: 10 leds que acendem com lógica `1`
- `Push Buttons`: 4 botões que quando apertados fornecem lógica `0`
- `Slide Switchs`: 10 Slides que quando acionados forcem lógica `1`
- `HEX Displays`: 6 displays de 7 segmentos (anodo comum)

### Gerando `toplevel.vhd`

| Caminho           |
|-------------------|
| `1-logComb/exe4/` |

O programa `toplevel.py` faz o mapeamento do componente para os pinos da FPGA e gera o arquivo `toplevel.vhd` que será utilizado pelo Quartus para gerar o arquivo binário que irá ser programado na FPGA, a ideia desse módulo é mapear os sinais do componente para nomes e tamanhos fixos que serão utilziados pelo programa.

 ```py title="toplevel.py"
 @block
 def toplevel(LEDR, SW, KEY, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5):
     ic1 = componente(HEX0, SW)

 # pinos
 LEDR = Signal(intbv(0)[10:]) # (1)
 SW = Signal(intbv(0)[10:])
 KEY = Signal(intbv(0)[4:])
 HEX0 = Signal(intbv(1)[7:])
 HEX1 = Signal(intbv(1)[7:])
 HEX2 = Signal(intbv(1)[7:])
 HEX3 = Signal(intbv(1)[7:])
 HEX4 = Signal(intbv(1)[7:])
 HEX5 = Signal(intbv(1)[7:])
 
 # instance e generate vhd
 top = toplevel(LEDR, SW, KEY, HEX0, HEX1, HEX2, HEX3, HEX4, HEX5)
 top.convert(hdl="VHDL") # (2)
 ```
 
 1. Vetor de tamanho 10
 2. Aqui indicamos para o MyHDL gerar o vhdl a partir do componente `top`
 
 Notem que os sinais criados são do tipo `Signal(intbv(0)[X:])`, isso indica que estamos manipulando um vetor de bits de tamanho **X**, no caso do LED, indicamos que o vetor é do tamanho 10, e no caso das KEY de tamanho 4. Com isso, podemos dentro do componente acessar individualmente cada um dos elementos do vetor:
 
 ```py title="componente.py"
 @block
 def componente(led, sw):
 @always_comb
 def comb():
     led[0].next = sw[0] and (not sw[1])

 return instances()
 ```
    
!!! info
    Notem que o `componente` recebe como argumentos os `LEDS` e as chaves `SW` da FPGA e implementa a lógica `sw[0] and (not sw[1])`.

!!! exercise
    1. Analise os arquivos `componente.py` e `toplevel.py`
    1. Execute o `toplevel.py` e note a geracão do arquivo `toplevel.vhd`
    1. Analise o arquivo `toplevel.vhd`
    
    ```bash
    ./toplevel.py 
    ```

### Gerando `.sof`

O processo de gerar um hardware que posso ser executado na FPGA é complexo e até pouco tempo não existiam ferramentas opensource que fazem isso. Iremos utilizar um software da Intel chamado de Quartus que é capaz de sintetizar um hardware paras as FPGAs que a Intel possui, no nosso caso a Cyclone V. Para facilitar o desenvolvimento criamos um makefile que recebe como input a pasta do exercício e gera o `sof`. O projeto do quartus será o mesmo para todos os exercícios.

Para isso, devemos passar como parâmetro `VHDL=../PASTA` do exercício que desejamos gerar o binário, e o makefile se encarrega de configurar o quartus e gerar o `.sof`.

!!! tip
    O processo é demorado para quem está acostumado a apenas programar em python, a geracão do arquivo pode demorar alguns minutos.

!!! exercise
    1. Entre na pasta `1-logCom/Quartus-Default`
    1. Execute `make VHDL=../exe4 all`
    1. Aguardem compilar
    1. Verifiquem que um novo arquivo `DE0_CV_Default.sof` foi gerado

### Programando FPGA

Agora com a FPGA plugada no computador podemos programar, para isso usaremos o comando `make program` que deve enviar para a ROM da FPGA o bitstream.

!!! exercise
    1. execute `make program`
    1. Mexa nas chaves 0 e 1 e notem o LED 0 obedece a equacao `sw0 and (not sw1)`
    
## Praticando - parte 2

!!! exercise
    Para cada exercício implemente a solução no arquivo `componente.py` e programe na FPGA para testar. Lembre de gerar o `toplevel.vhd` e de rodar o `make ...`.
    

    - [ ]  `logComb/exe5`
    - [ ]  `logComb/exe6`
    - [ ]  `logComb/exe7`
