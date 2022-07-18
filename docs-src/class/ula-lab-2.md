# Lab 7: Depurando

Depurar hardaware (debugar) não é uma tarefá fácil, o problema pode estar em vários lugares diferentes: Componente queimando, solda com mal contato, erros no projeto de hardware, erro no software, clock com jiter ..... A lista de onde um problema pode estar é enorme e envolve várias áreas. 

Aqui na disciplina vamos assumir uma lista menor de problemas, pois iremos eliminar que a placa pode estar com defeito (ou que não foi bem projetada) e que haja algum defeito na configuração do Quartus. Basicamente os problemas podem ser:

1. No entendimento da logica 
1. Na transcrição de uma lógica combinacional/ sequencial para RTL (portas lógicas)
1. No uso de recursos do MyHDL 

Com o MyHDL conseguimos depurar um módulo de diversas maneiras e em diferentes camadas. Como estamos no ambiente do python, conseguimos inserir `prints` ou usar `breakpoints()` e acompanhar a simulação **passo a passo**. Podemos também gerar um diagrama de forma de ondas, que é muito utilizado para a depuração de hardware.

Para entendermos o processo iremos usar como exemplo o módulo `fullAdder` que está em uso pelo `adder2bits` do lab anterior. 

## print

Podemos inserir prints nos componentes a fim de ajudar no desenvolvimento do mesmo. Temos que entender que o `print` não é sintetizável (não vai para a FPGA) e está limitado a apenas `inputs` e `sinais` internos do módulo, não podemos usar o print em `outputs`.

Por exemplo, se desejarmos exibir o valor da saída `soma` do `halfAdder`, poderíamos inserir um print, mas como `soma` é uma **saída**, vamos ter um erro:

``` py title="ula_modules.py" hl_lines="7"
@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b
        print(soma) # (1)

    return instances()
```

1. `print` no `soma` que é uma saída, não podemos fazer isso!

> ==myhdl.AlwaysCombError: signal ({'soma'}) used as inout in always_comb function argument==

Para solucionar esse problema podemos criar um sinal interno auxiliar (que será visível como entrada e saída):

``` py title="ula_modules.py" hl_lines="3 8"
@block
def halfAdder(a, b, soma, carry):
    s_soma = Signal(bool())
    @always_comb
    def comb():
        s_soma = a ^ b
        
        soma.next = s_soma
        carry.next = a & b
        print(s_soma)

    return instances()
```

!!! info
    Notem que nesse caso não usamos `s_soma.next = a ^ b`, se fizermos 

Agora se executarmos o teste com `pytest -k halfAdder -s`, ==-s ativa o print para o terminal==, iremos obter o resultado da `soma` a cada interação do teste:

```
False
True
True
False
```

!!! exercise
    - File: `2-ula/ula_modules.py `
    - Modulo: `def halfAdder(a, b, soma, vaiUm):`
    - Test: `pytest -k halfAdder -s`
 
    Modifique o módulo para obter um print que exibe as entradas `a`, `b` e as saídas `soma` e `carry`, como:
    
    ```
    a: 0 b: 0 | s: 0 c: 0
    a: 0 b: 1 | s: 1 c: 0
    a: 1 b: 0 | s: 1 c: 0
    a: 1 b: 1 | s: 0 c: 1
    ```
    
    Dica: utilize `bin(a)` para formatar a saída como binário.


## breakpoint

Uma outra opção muito poderosa que possuímos é de utilizarmos `breakpoint` no código, para isso basta adicionar `breakpoint()` onde você deseja interromper a execução do código,e então executar novamente o teste.

```  hl_lines="8"
@block
def halfAdder(a, b, soma, carry):
    s = Signal(bool())
    c = Signal(bool())

    @always_comb
    def comb():
        breakpoint()
        s = a ^ b
        c = a & b

        soma.next = s
        carry.next = c

        print("a: %s b: %s | s: %s c: %s" % (bin(a), bin(b), bin(s), bin(c)))

    return instances()
```

Quando o programar atingir a linha do breakpoint. Nesse momento podemos usar uma série de recursos, vamos ver os mais importantes:

- `print(a)`: Você pode imprimir o valor de qualquer variável ou operação
- `n`: (next) Podemos executar linha a linha o programa
- `c`: (continue) Podemos liberar a execução do programa até ele encontrar um novo breakpoint ou finalizar
- `w` (where) Exibi informações do local do breakpoint

<script id="asciicast-Xvb0we1j1c4jHYpBAK5uHjViz" src="https://asciinema.org/a/Xvb0we1j1c4jHYpBAK5uHjViz.js" async></script>

!!! exercise
    Insira o `breakpoint()` na linha indicada no exemplo anterior e pratique um pouco

!!! exercise
    Remova o `breakpoint()` 
    
    Lembrem de sempre remover o `breakpoint` após o uso.

## wave 

Como as coisas em hardware acontecem simultaneamente fica difícil visualizar o que está acontecendo em todo o projeto, como alternativa podemos gerar uma forma de onda do hardware e visualizar o que está acontecendo com os sinais.

Note que na pasta `2-ula` foi gerado um arquivo chamado de `adder2bits.vcd`, esse arquivo possui a forma de onda do teste. Para visualizarmos iremos usar o programa `gtkwave`. No terminal, execute: 

!!! terminal
    - gtkwave adder2bits.vcd

!!! todo
    Adicionar vídeo de como usar o gtkwave
