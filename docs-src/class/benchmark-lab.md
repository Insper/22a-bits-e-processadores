# Benchmark

!!! info "pensadeira"
    - Forncer um ssd com a infra já instalada?
    - Rodar testes no monstrão/ aws/ rasp3/ rasp4
    - Quais tipos de benchmark?
        - processamento
        - cache
        - acesso a disco
        - 

Neste laboratório iremos explorar os diferentes tipos de hardware existentes e qual o impacto no desempenho de alguns tipos de programa. Para isso iremos utilizar o [phoronix-test-suite](https://www.phoronix-test-suite.com/), que disponibiliza uma série de testes do https://openbenchmarking.org/.

## configurando

No terminal, execute:

```
 phoronix-test-suite batch-setup
```

E configure como indicado a seguir:

```
 Save test results when in batch mode (Y/n): y
 Open the web browser automatically when in batch mode (y/N): y
 Auto upload the results to OpenBenchmarking.org (Y/n): y
 Prompt for test identifier (Y/n): y
 Prompt for test description (Y/n): n
 Prompt for saved results file-name (Y/n): n
 Run all test options (Y/n): y
```

## Informacão do sistema

Agora vamos extrair algumas informações do sistema, para isso execute no terminal:

```
phoronix-test-suite system-properties
```

Você deve obter uma lista com informações detalhadas do seu sistema, com os dados preencha a tabela a seguir:

!!! info "Disco"
    A tabela pede informações extras sobre o seu disco rígido, sugerimos você procurar no google usando como base o modelo, remova da busca a capacidade do disco, isso pode atrapalhar.
    
    Caso não encontre todas as informações tudo bem!
    
## Executando o primeiro teste

Vamos executar o primeiro teste, que envolve compilar o kernel do Linux:

!!! tip
    O teste deve demorar alguns minutos:

```
phoronix-test-suite benchmark build-linux-kernel
```

