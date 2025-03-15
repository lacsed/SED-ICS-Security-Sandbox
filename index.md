{% include lib/mathjax.html %}

# Plataforma para Testes de Cibersegurança em Sistemas de Controle Industriais Modelados por SEDs

O conteúdo deste repositório está relacionado ao artigo de título: "Implementação de uma Plataforma para Testes de Cibersegurança em Sistemas de Controle Industriais Modelados por SEDs" submetido para o XVII Simpósio Brasileiro de Automação Inteligente (SBAI).

## Visão Geral

A interface gráfica do sistema representa um tanque que integra seis subsistemas distintos, os quais operam conjuntamente no processo de produção de um produto.

![Image](https://github.com/user-attachments/assets/09d0f87b-edca-4680-95a9-4c9c18f70f7e)

## Subsistemas

O sistema conta com os seguintes subsistemas:

- **Válvula de Entrada:** Controla a abertura e o fechamento das válvulas responsáveis pelo fluxo de três tipos de fluidos no sistema.
- **Transmissor de Nível:** Monitora o nível do tanque.
- **Dispositivo de Controle de Temperatura:** Gerencia o aquecimento e o resfriamento do tanque.
- **Mixer:** Responsável por misturar os fluidos no tanque, assegurando uma homogenização durante o processo de aquecimento.
- **Bomba:** Bombeia o fluido do tanque principal para um trocador de calor.
- **Válvula de Saída:** Controla a abertura e o fechamento da válvula responsável pelo esvaziamento do tanque.

## Tecnologias Utilizadas

- **OPC UA** para comunicação entre cliente e servidor.
- **Interface gráfica** para monitoramento e controle dos processos.

## O Processo

O processo de produção segue a sequência descrita a seguir: inicialmente, a válvula de entrada é aberta, permitindo que os fluidos entrem no tanque. O sistema monitora o nível de fluido, aguardando a ocorrência do evento de nível alto, que indica que o tanque está cheio. O controlador, ao receber o evento correspondente ao nível alto, envia o comando de fechar a válvula de entrada e a válvula é então fechada, interrompendo o fluxo de entrada.

Na etapa seguinte, o sistema de controle de temperatura é ativado para aquecer o fluido no tanque. Ao mesmo tempo, o misturador é acionado para garantir que o aquecimento ocorra de forma homogênea. O misturador permanece ativo até que o evento do tanque aquecido seja disparado, indicando que a temperatura desejada foi atingida. Após o aquecimento, o processo de resfriamento começa. A bomba é ativada para fazer com que o fluido passe pelo trocador de calor, fazendo com que o fluido seja resfriado mais rapidamente. O sistema continua o resfriamento até que o evento do tanque resfriado tenha sido disparado, sinalizando que o fluido atingiu a temperatura requerida.

Por fim, a válvula de saída é aberta para liberar o produto do tanque. O sistema aguarda o evento de nível baixo, que indica que o tanque foi esvaziado até o nível desejado. Assim que o tanque é esvaziado, a válvula de saída é fechada, encerrando o processo.

## Componentes da Plataforma

A interface gráfica da plataforma é dividida em seções. Ela conta com um menu lateral, a tela que exibe o processo físico da planta, uma central de segurança, e centros de operação para coordenação manual do sistema e controle de ataques. Visores no canto inferior indicam a localização dos eventos processados, o evento atacado e o tipo de ataque em execução.

O menu lateral permite definir as temperaturas inicial, de aquecimento e resfriamento, assim como os tempos correspondentes de aquecimento e resfriamento do fluido. Também possibilita a seleção dos modos de operação do processo e de ataque, além de conter os botões _Start_ e _Stop_ para iniciar e interromper a execução da simulação. Uma tabela exibe em tempo real a lista de eventos trafegados na rede.

![Image](https://github.com/user-attachments/assets/4268a0cc-4df4-48b9-acf4-e279b0f91bb1)

## Simulações

A plataforma conta com dois modos de operação para o atacante: furtivo e convencional. Cada modo adota uma estratégia distinta, permitindo explorar diferentes cenários de ataque e avaliar o impacto desses ataques no sistema físico.

### Modo Furtivo

No modo furtivo, o foco principal é minimizar a possibilidade de detecção pelo IDS. Para isso, o sistema adota pausas temporais após a inserção ou remoção de eventos. Essa abordagem tem como objetivo reduzir a exposição do atacante ao sistema, evitando detecções imediatas, dado que o IDS opera em ciclos de execução, verificando os eventos que estão sendo trafegados a medida que cada evento vai sendo disparado e trafegado na rede. Conforme mostrado no vídeo abaixo.

<div class="video-container">
  <iframe src="https://www.youtube.com/embed/OgW2W8uHYtQ" 
    frameborder="0" allowfullscreen></iframe>
</div>

### Modo convencional

Já o modo convencional adota uma abordagem direta, sem se preocupar em evitar a detecção pelo IDS. As ações são realizadas de forma rápida e sem cautela, com eventos sendo removidos e inseridos novamente em intervalos de tempo aleatórios tornando o ataque mais agressivo, mas também mais vulnerável à identificação.

<div class="video-container">
  <iframe src="https://www.youtube.com/embed/A9N\_vIwC0io" 
    frameborder="0" allowfullscreen></iframe>
</div>
