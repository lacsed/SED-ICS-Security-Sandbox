{% include lib/mathjax.html %}

# Plataforma para Testes de Cibersegurança em Sistemas de Controle Industriais Modelados por SEDs

O conteúdo deste repositório está relacionado ao artigo de título: "Implementação de uma Plataforma para Testes de Cibersegurança em Sistemas de Controle Industriais Modelados por SEDs" submetido para o XVII Simpósio Brasileiro de Automação Inteligente (SBAI).

## A Plataforma

Este sistema é implementado com base em uma arquitetura cliente-servidor, utilizando a tecnologia **OPC UA** (_Open Platform Communications - Unified Architecture_). OPC UA é um padrão de comunicação amplamente adotado na automação industrial para permitir a troca de dados entre dispositivos, sistemas e softwares.

![Image](https://github.com/user-attachments/assets/09d0f87b-edca-4680-95a9-4c9c18f70f7e)

## Visão Geral

A interface gráfica do sistema representa um tanque que integra seis subsistemas distintos, os quais operam conjuntamente no processo de produção de um produto.

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

<div class="video-container">
  <iframe src="https://www.youtube.com/embed/OgW2W8uHYtQ" 
    frameborder="0" allowfullscreen></iframe>
</div>

### Software

The code for each node is available below.

- [Controller](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/controller)
- [Node 1](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/node1)
- [Node 2](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/node2)
- [Node 3](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/node3)
