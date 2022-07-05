# MyHDL Básico

O [MyHDL](http://docs.myhdl.org/en/stable/manual/index.html) foi a linguagem escolhida para o desenvolvimento do hardware da disciplina Bits e Processadores, o MyHDL é um pacote python que permite descrevermos um hardware (note que não é **programar um hardware**) utilizando a linguagem Python. O importante é saber que descrever um hardware é diferente de escrevermos um programa:

> Um programa em Python/Java/C é como uma receita de bolo que será executada em uma cozinha que já está montada, essa cozinha é o sua CPU (processador), e não dá para mudar com código (software), o que você muda de um programa para outro é a receita. Uma cozinha é capaz de realizar diversas receitas diferentes ....
>
> No caso do MyHDL não temos essa 'cozinha' pronta, na verdade, podemos criar qualquer cozinha que quisermos. Com ele você será um arquiteto de cozinhas, capaz de criar praticamente qualquer hardware! E então realizar suas receitas na cozinha que criou.

As linguagens de descrição de hardware são chamadas de *Hardware Description Language (HDL)* e são muito penosas de aprender (VHDL, VERILOG) pois são complexas e antigas (uma delas foi criada na guerra fria e não foi criada com o propósito que é utilizada atualmente), mas existe uma família de novos HDL que tem ganhado bastante evidência na comunidade, e uma delas é o MyHDL.

O MyHDL serve apenas como uma camada de mais alto nível, ele não é capaz de criar um hardware funcional na FPGA (hardware que usamos para criarmos nossas *cozinhas*). Mas ele consegue gerar um arquivo `VHLD` que pode ser sintetizado na FPGA e virar um hardware real.

```
    IDEA                                |  
    MIRABORANTE  ---> MyHDL  --> VHDL --|> FPGA
                                        |
```

## Conceitos básicos - Hardware

<!--  
!!! info ""
    inspirado no tutorial do MyHDL

O MyHDL faz uso de duas ferramentas da linguagem python que vocês podem não estar acostumados: `generators` e `decorators`, vamos analisar cada uma delas a seguir.

### Generators
-->

Circuitos digitais podem ser descritos como combinações de circuitos combinacional e sequenciais, circuitos combinacionais são aqueles que a saída "reage" instantaneamente a mudança do valor da entrada (equações booleanas, mux, demux, decoders, ...) e os circuitos sequências são aqueles que depende de um clock, ou que a saída não é uma ação imediata da mudança da entrada.

Primeiro iremos trabalhar apenas com os circuitos sequências e depois avançaremos para os síncronos (para criar a memória do nosso processador).

Um conceito muito importante que vocês devem tomar cuidado é que quando criamos um hardware, somos capazes de realizar ações simultaneamente, diferente de um programa que executa "linha a linha", um hardware tende a executar tudo ao mesmo tempo (paralelismo). 

Hardwares são construídos através de pequenos módulos que formam um sistema mais complexo (hierárquico), os módulos podem ser visualizados como componentes eletrônicos que interligados em uma placa de circuito impresso (PCB) formam por exemplo um computador. O mesmo módulo pode ser usado mais de uma vez e em diferentes lugares do hardware.

## Conceitos básicos - MyHDL

!!! warning
    Lembre que estamos usando o python para descrever um hardware e não um programa!

No MyHDL definimos uma instância (componente de hardware) usando o `decorator`: `@block` na classe, isso define que a classe deve ser interpretada como um componente de hardware. Cada componente de hardware pode possuir internamente vários comportamentos (no caso aqui veremos apenas o combinacional) que são definidos pelos métodos da classe com o decorator (`always_comb`).

Vamos ver um exemplo que implementa a seguinte equação lógica: `q = a or (b and c)`:

```python
from myhdl import *

@block
def equacao(q, a, b, c):

    @always_comb
    def comb():
        q.next = a or (b and c)

    return comb
```

Parece bem ok né? Mas tem alguns segredos que vamos analisando aos poucos. No exemplo aparece os decorators: `@block` (para definir um hardware) e `@always_comb` (combinacional), o hardware possui apenas uma classe que é chamada de `comb`  onde a relação entre as entradas e saída do hardware é definida. Como ilustrado no diagrama a seguir:

```
     |------------|
  a---> ********  |         
  b---> * comb * ----> q
  c---> ********  |     
     |            |
     |  equacao   |
     |------------|

```

A implementação da equação é trivial e utiliza da sintax do python `a or (b and c)`, mas a saída `q` é acessada via o atributo `next`: ==q.next==. Isso é feito porque o argumento `q` (e os demais) não são variáveis comuns do python e sim um tipo especial definido pelo MyHDL, chamada de `Signal`. 

Da documentaćão do MyHDL:

> `next`
>
> Read-write attribute that represents the next value of the signal.

!!! info
    Mais para frente iremos entender melhor o `Signal` e como utilizamos essa variável. 

### Testando

Para testarmos o bloco de hardware crido anteriormente devemos de alguma forma instanciar o hardware e adicionar estímulos a entrada dele, este processo em projetos de hardware é chamado de *testbench*. Notem que isso é diferente de apenas fazermos a chamada de uma função (que alias vamos entender mais para frente no curso como é que funciona).

Para os estímulos iremos devemos criar um método, que possui um novo decorator chamado `instance`, que indica que iremos realizar a instanciação de um componente de hardware (usar o componente), nesse método iremos criar os estímulos necessários para testarmos o nosso hardware. Temos que lembrar que quando estamos mexendo com hardware, esses estímulos acontecem no tempo, por isso temos o `yield delay(1)`, que indica para a simulação aguardar por 1 tick de tempo antes de realizar o próximo processamento.

``` python
@instance
def stimulus():
    a.next = 0
    b.next = 1
    c.next = 1
    yield delay(1)
    print("q = %s" % q)
```

Gera o diagrama:

```ascii
          : yield delay(1)
          :
a ---0----:----
          :_____
b --------/ 1   
          :_____
c --------/ 1    
          :_____  
q --------/      (q válido)
```

!!! tip
    Importante verificar o uso do ==next==, as variáveis são atualizadas todas no mesmo instante! Notem no diagrama que `a`, `b` e `c` e `q` mudam juntas! Diferente do que aconteceria em um programa python na qual a ordem da atribuição impacta em quem é alterado primeiro.

!!! info
    O `yield delay(1)` faz com que as saídas `.next` sejam atualizadas.
    
!!! info "yield python"
    Você sabe o que é o `yield`? Ele surgiu no python 2.2 e é utilizado pelo MyHDL, ele é similar ao `return` de uma função, mas quando a função é chamada novamente ela retorna do ponto que parou. Veja o exemplo a baixo:
    
    ```
    def foo():
        for i in range(3)
            yield(i)
            
    bar = foo()
    bar.next()
    >>> 1
    bar.next()
    >>> 2
    bar.next()
    >>> 3
    bar.next()
    >>> Traceback (most recent call last):
    >>> File "<stdin>", line 1, in ?
    ```
    
    A função `foo` ficou interativa!
 
Agora temos que juntar o hardware que desejamos testar com o estímulo criado:

```py
q = Signal(bool(0))
a = Signal(bool(0))
b = Signal(bool(0))
c = Signal(bool(0))
equacao_1 = equacao(q, a, b, c)

sim = Simulation(equacao_1, stimulus)
sim.run()
```

Notem que criamos quatro variáveis do tipo `Signal(bool(0))`, isso indica para o MyHDL que as variáveis `q,a,b,c` são sinais (entradas e saídas do hardware) do tipo `bool` (binárias), ou seja, só podem assumir `1` ou `0`. Todas as variáveis são do tipo `bool` e inicializadas em `0`.

!!! info
    Poderíamos inicializar as variáveis no estado '1':  `q = Signal(bool(1))`


Ao executar o projeto, obtém a seguinte saída:

```
>>> 
q = 1
<class 'myhdl.StopSimulation'>: No more events
```

O resultado obtido é o esperado: `1 = 0 or (1 and 1)`! Que bom né? 

!!! info
    Realizamos apenas o teste de uma condicão no módulo, um teste mais correto deveria ser mais amplo. Depois vamos entender como fazer isso.

## O que ainda falta aprender do MyHDL

Ainda falta entender outros tipos de dados que não binário (`intbv`), como descrever hardwares sequenciais (dependem de um clock), como converter e executar o projeto em um hardware real!
