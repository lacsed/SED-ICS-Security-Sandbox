{% include lib/mathjax.html %}

# Plataforma para Testes de Cibersegurança em Sistemas de Controle Industriais Modelados por SEDs

O conteúdo deste repositório está relacionado ao artigo de título: "Implementação de uma Plataforma para Testes de Cibersegurança em Sistemas de Controle Industriais Modelados por SEDs" submetido para o XVII Simpósio Brasileiro de Automação Inteligente (SBAI).

## Processo

In this section we describe the physical process in which we applied the proposed control solution. The general idea is the production of batches of a liquid that is the product of reactions that happen at different temperatures inside a reactor. A depiction of the process can be seen next.

The process start by the admission of three different liquids, after the Start button is pressed by an operator. It is assumed that the flow of each liquid is defined by a previous process and is out of scope in here. There are three on-off input valves, each one for a different liquid, that receive the same control action, that is, they open and close at the same time. Since the valves remain opened by the same amount of time, the proportion of each liquid in the tank is determined by their flow.

The total amount of liquid in the tank, which has a cylindrical shape, is a controlled variable and it is measured by a level sensor. Once the level in the tank reaches the set point, the input valves are closed and the mixer is turned on. The mixer makes the mix more homogeneous and therefore diminishes the total time of the batch production.

After the mixer has started, a continuous-time PI controller makes the temperature reach a desired value and remain there for a predefined period of time. After that, the controller makes the temperature reach a second predefined value, which is lower than the previous one, for another amount of time. A heater installed in the tank makes it possible to increase the temperature. To allow the liquid to cool faster, there is a heat exchanger coupled in the tank. To make the liquid go through it, a pump is turned on. Once this part of the process is finished, the mixer and the pump stop and an output valve is opened. The valve will remain opened until the level sensor indicates that the tank has reached the low level. When this happens, the output valve is closed and the batch is finished. The system is now ready to produce another batch.

## Models

### Subsystems

We introduce the automata models of the subsystems. The models are an abstraction of the real systems and we only consider in here events that are relevant to the cordination between them. Transitions with a streak are labelled with controllable events, while the ones without a streak are labelled with uncontrollable ones. All the models have an uncontrollable reset event $$rst$$. This event is useful to restore the sync between the subsystem and supervisors if something fails.

#### Process

The process automaton does not represent a specific subsystem. Instead, it represents the whole system and it is useful when modeling specifications that restrain the behavior of a subsystem to the beggining or to the end of a production cycle. At the initial state the process is at state idle ($$I$$). After ocurrence of event $$start$$, it goes to state working ($$W$$). Once the process finishes, event $$finish$$ occurs and it goes to the initial state.

#### Input valve

The input valve is represented by a two-state automaton. At the initial state the valve is closed ($$C$$). It opens ($$O$$) with the occurrence of event $$V_{in}^{open}$$. In the open state, the sensor level may trigger event $$L_{H_1}$$, which is represented by a self-loop. The valve closes with event $$V_{in}^{close}$$.

#### Output valve

The output valve is represented by a two-state automaton. At the initial state the valve is closed ($$C$$). It opens ($$O$$) with the occurrence of event $$V_{out}^{open}$$. In the open state, the sensor level may trigger event $$L_{L_1}$$, which is represented by a self-loop. The valve closes with event $$V_{out}^{close}$$.

#### Mixer

The behavior of the mixer is represented by a two-state automaton. At the initial state, the mixer is not working ($$I$$). Upon the ocurrence of event $$M^{on}$$, the mixer goes to state working ($$W$$). It remains there until event $$M^{off}$$ occurs, leading it back to the initial state.

#### Pump

The behavior of the pump is represented by a two-state automaton. At the initial state, the pump is not working ($$I$$). Upon the ocurrence of event $$P^{on}$$, the pump goes to state working ($$W$$). It remains there until event $$P^{off}$$ occurs, leading it back to the initial state.

#### Temperature control

The behavior of the continuous-time temperature control is represented by a two-state automaton. The control is initially at the initial state ($$I$$). Once event $$T^{on}$$ occurs, the temperature control goes to state working ($$W$$). At this state, the continuous-time temperature controller controls the temperature of the liquid in the tank. How this is done, is not relevant for the DES control. For this reason, only events related to the completion of tasks are added in the model. Thus, event $$heated$$ indicates the the liquid has reached the higher temperature and remained in there for a given period of time while event $$cooled$$ represent that the liquid reached the lower temperature and also remained at it for a given amout of time. The control strategy, setpoints and the periods of time can be latter adjusted by the user.

### Software

The code for each node is available below.

- [Controller](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/controller)
- [Node 1](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/node1)
- [Node 2](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/node2)
- [Node 3](https://github.com/michelrodrigo/DES-control-system/tree/gh-pages/sources/codes/decentralized/node3)
