# Lab 8: Lógica Sequencial

Agora vamos ver como implementamos uma lógica sequencia em MyHDL! Até agora temos utilizado o `decorator`: `@always_comb` para indicar que uma função deve ser interpretada como um trecho combinacional:

```py
@always_comb
def comb():
    led.next = l
```

Agora vamos começar usar um novo `decorator` (`@always_seq`) para indicar que uma função deve ser sequencial e depender do `clock` e do `reset`. O módulo aseguir demonstra como implementar um flip-flop tipo D em MyHDL:

```py
@block
def dff(q, d, clk, rst):
    @always_seq(clk.posedge, reset=rst)
    def seq():
        q.next = d

    return instances()
```

Notem que estamos usando `@always_seq(clk.posedge, reset=rst)`, e indicando que o módulo deve ser acionado na borda de subida do sinal `clk` e que o sinal de `reset` deve ser o `rst`.

Podemos interpretar o `def seq()` da seguinte maneira: Sempre que o sinal clock variar de `0` para `1` a função é acionada e então a saída `q` recebe a entrada `d`. Podemos visualizar isso como um `while True:` 

```py
    while True:
        q.next = d
        time.sleep(1/CLOCK)
```

## dff

!!! exercise
    - File: `seq/seq_modules.py`

    Tarefa:

    Vamos validar o flip-flop, para isso modifique o `toplevel.py`:
    
    ```py
        ic0 = dff(ledr_s[0], sw_s[0], key_s[0], RESET_N)
    ```
    
    E faça o processo completo para obtermos o hardware.
    
    Validando:
    
    Mapeamos o clock para o `KEY[0]` e a entrada do dff para o `SW[0]`, notem que ao mexer a chave `SW[0]` nada acontece, o valor do LED muda apenas após apertar o `KEY[0]` (que é o `clock`)
    
### Clock

O sinal de clock da nossa FPGA é de ==50Mhz==, ou seja: `50 000 000` vezes por segundo! Isso parece muito né? Mas, dependendo do projeto, podemos elevar o clock para 200Mhz ou usar FPGAs mais rápidas que chegam próximo do 1GHz.

## Piscando LED

Agora com o uso da lógica sequencial conseguimos contar 'tempo' e gerar eventos em determinado momento. Ou seja: podemos contar 0.5 segundos e mudar o valor do led, contar mais 0.5 s e mudar novamente (fazer o famoso **pisca led**). Para isso, teremos que conseguir contar eventos de clock, e quando o valor chegar em **25 000 000** inverter o valor do LED e zerar o contador e ficar nesse loop para sempre.

Podemos usar o nosso `adder` do lab anterior como módulo de contador, conectando a saída do `adder` na entrada `x`, mas passando por um registrador antes (para apenas mudar a cada clock). A entrada `y` será conectado ao valor `1`, como resultado teremos: `s = x + 1`. A expressão será executada a cada subida do clock. E `x` será:

``` py
if s < MAX:
    x.next = s
else:
    x.next = 0
```

Se o valor de `s` for menor que o valor máximo (define a velocidade que o LED irá piscar) copiamos a saída do somador para a entrada, e se o valor `MAX` for atingido, iremos zerar o somador, para começarmos novamente. O HW que queremos gerar é algo como:

![](figs/seq/lab-blink.svg)

A implementação em MyHDL:

```py
@block
def blinkLedAdder(led, clk, rst):
    x = [Signal(bool(0)) for i in range(32)]
    y = [Signal(bool(0)) for i in range(32)]
    s = [Signal(bool(0)) for i in range(32)]
    c = Signal(bool(0))
    status = Signal(bool(0)) 

    y[0] = 1 
    adder_1 = adder(x, y, s, c) 

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if x[21] == 0: 
            for i in range(len(x)):
                x[i].next = s[i] 
            status.next = status 
        else:
            for i in range(len(x)):
                x[i].next = 0
            status.next = not status

    @always_comb
    def comb():
        led.next = status

    return instances()
```

!!! exercise 
    File: `toplevel.py`
    
    Modifiquem o toplevel para conter o componente:
    
    ```py
       ic1 = blinkLedAdder(ledr_s[0], CLOCK_50, RESET_N)
    ```
    
    E façam o fluxo de rodar o módulo na FPGA. Verifiquem que o LED pisca!!

Alguns detalhes devem ser levados em consideração na implementação do componente:

1. Estamos lidando com vetores de bit, que devem ser acessados individualmente
1. O `seq` acontece a cada mudança do clock
1. O `comb` acontece sempre
1. Não podemos `ler` uma saída

```diff
- if s < MAX:
+ if x[24] == 0 and x[23] == 0: 
```

Temos que lembrar que estamos lidando com um vetor de `bits` que não possuem ligação entre si, então não podemos fazer uma comparação como se eles fossem um inteiro: `if x < 25000000`, mas temos que verificar os bits individualmente. Nesse caso eu estou verificando se os bits `24` e `23` são iguais a zero. Pois:

```
2^24 + 2^23 = 25165824
```

Um valor muito próximo de 25M (um erro menor que 1%). Que para o pisca led não será perceptível. Poderíamos é claro melhorar colocando mais `bits` na verificação, mas não é necessário.

-------------

Por conta de `x` e `s` serem vetores, temos que fazer uma varredura para atribuirmos cada um dos index:

```diff
- x.next = s
+ for i in range(len(x)):
+     x[i].next = s[i]
```

!!! warning
    É importante sabermos que o `for` em hardware não existe, é apenas um recurso para facilitar a descrição do componente, no lugar de escrevermos isso:
    
    ```
    x[0].next = s[0]
    x[1].next = s[1]
    ...
    ```

-------------

A ideia de piscar o LED é que temos que mudar uma variável a cada ciclo do contador. 
```
-----------           -------------
           |          |            |           Status
           |          |            |
            -----------            ----------
            
           _ 25000000  _            _
         / |         / |          / |      
      /    |      /    |       /    |          Contador
   /       |   /       |    /       |
/          |/          | /          |
```

Mas como o sinal `led` é uma saída, não podemos acessar ele diretamente. Para isso, eu criei um sinal interno auxiliar `status` que é alterado sempre que o contador é zerado:

```py
def seq():
    if x[24] == 0 and x[23] == 0:
        status.next = status
    else:
        status.next = not status
```

E então atribuímos o valor de `status` para a saída `led` na parte combinacional do módulo:

```py
def comb():
    led.next = status
```

## Melhorando

Até agora estamos usando **mal** os recursos do MyHDL, o componente anterior poderia ser muito mais simples se:

1. Pudéssemos tratar sinais como `inteiros` 
1. Não precisássemos usar o `adder`

Para isso o MyHDL possui outros dois tipos de dados além do `bool`, vamos trabalhar com o `intbv`


> Hardware design involves dealing with bits and bit-oriented operations. The standard Python type int has most of the desired features, but lacks support for indexing and slicing. For this reason, MyHDL provides the intbv class. The name was chosen to suggest an integer with bit vector flavor.
> 
> Do mamual: http://docs.myhdl.org/en/stable/manual/hwtypes.html

Alguns exemplos de como trabalhar com o tipo:

```py
>>> a = intbv(24)
>>> b = intbv(2)
>>> print(a)
24
>>> print(a + b)
26
>>> print(a == 12)
False
```

O `intbv` não limita a quantidade de bits que será utilizado
, isso funciona muito bem na simulação, mas quando formos gerar um hardware temos que definir o tamanho do vetor caso contrário teremos erro na conversão. 

O exemplo a seguir indica como criarmos um sinal `cnt` com 32 bits:

```py
# cnt com 32 bits do tipo intbv
>>> cnt = Signal(intbv(0)[32:])

>>> cnt.max
4294967296

>>> cnt.min
0
```

## blink melhorado

Vamos agora reimplementar o blink, mas usando os novos recursos:

```py
@block
def blinkLed(led, clk, rst):
    cnt = Signal(intbv(0)[32:])
    l = Signal(bool(0))

    @always_seq(clk.posedge, reset=rst)
    def seq():
        if cnt < 25000000:
            cnt.next = cnt + 1
        else:
            cnt.next = 0
            l.next = not l

    @always_comb
    def comb():
        led.next = l

    return instances()
```

!!! tip ""
    Muito mais simples em! =)

!!! exercise
    - File: `toplevel.py`
    
    Tarefa:
    
    Modifique o toplevel para usar o novo componente e verifique na placa que ele funciona como deveria.

    ```py
    ic1 = blinkLed(ledr_s[0], CLOCK_50, RESET_N)
    ```

!!! exercise short 
    O `cnt` de 32 bits está bem dimensionado? Esse valor faz alguma diferença?
    
    `cnt = Signal(intbv(0)[32:])`
    
    !!! answer
        - 32 bits = 4294967296
        - 4294967296/50M = 85s
        
        Faz diferença sim! Quando mais bits, mais registradores temos que usar e maior ficar o hardware.
        
        Poderíamos dimensionar o tamanho do vetor de acordo com o `time_ms` que foi passado para o módulo.

!!! exercise
    - File: `seq_modules.py`
    - Função: `blinkLed`
    
    Vamos deixar o componente mais genérico? Para isso modifique a função `blinkLed` para receber mais um argumento: O valor em `ms` na qual o LED irá piscar:
    
    ```py
    def blinkLed(led, time_ms, clk, rst):
    ```
    
    Depois modifique o toplevel para validar diferentes valores em diferentes leds:
    
    ```py
    ic1 = blinkLed(ledr_s[0], 100, CLOCK_50, RESET_N)
    ic2 = blinkLed(ledr_s[1], 50, CLOCK_50, RESET_N)
    ic3 = blinkLed(ledr_s[2], 1000, CLOCK_50, RESET_N)
    ```
    
    Lembre de validar na FPGA!

!!! exercise 
    - File: `seq_modules.py`
    - Função: `barLed`
    
    Tarefa:

    Vamos praticar mais! Agora faça com que os LEDs da FPGA acendam em sequência: Primeiro o LED0, depois o LED1... (como uma animação), ao chegar no final apague tudo e comece novamente.
    
    Dica:
    
    Você vai precisar de mais um contador indo de 0 a 9
    
!!! exercise
    - File: `seq_modules.py`
    - Função: `barLed`

    Modifique a barLed adicionando:
    
    - SW[0] controla a velocidade dos LEDs: Rápido ou Lento
    - SW[1] controla a direção (esquerda/ direita)
    
    ```py
    def barLed(leds, time_ms, dir, vel, clk, rst):
    ```

!!! exercise
    - File: `seq_modules.py`
    - Função: `barLed2`

    Tarefa:
    
    O barLed2 é similar ao LED porém só um LED aceso por vez!
    
    Dica:
    
    Aplique um shift de `cntLed` ao valor em binário `000000001`, onde `cntLed` é o contador de 0, 9.
    
    ```py
    @always_comb
    def comb():
        leds.next = intbv(1)[10:] << cntLed
    ```

## Desafio

Ideias de LABs com utilidade:

- Ultrasom HC-SR04?
- LED RGB
- StepMotor
- Servo
- ...
