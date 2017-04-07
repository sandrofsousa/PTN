# Study of properties and robustness of the public transport network of São Paulo

[![DOI](https://zenodo.org/badge/24470228.svg)](https://zenodo.org/badge/latestdoi/24470228)

Complex systems are characteristic by having an internal network representing
the structural relationship between its elements and a natural way to interpret
this interaction is through a graph. In this work, the urban public transport
system of São Paulo is reinterpreted as a coupled (bus and subway) complex
network, bypassing operational details and focusing on connectivity. Using the
empirically generated graph, a statistical characterisation is made by network
metrics where different radius values are used to group nearby stops and
stations that were disconnected before. That can be interpreted as a public
policy tool, representing the user’s willingness to get around the nearest
point to access transportation. This process has shown that increasing this
willingness generates great reduction in the distance and in the number of
jumps between buses, trains and subways lines to achieve all the network
destinations. An exploratory model is used to test the robustness of the
network by randomly, deterministically and preferentially targeting the stops
and service lines. According to the grouping radius, aka willingness, different
fragmentation values were obtained under attack simulations. These  findings
support two main characteristics observed in such networks literature: they
have a high degree of robustness to random failures, but are vulnerable to
targeted attacks.

**This code is part of a Master's research in the field of Complex Systems and
Complex Networks with application to the study of Public transportation network
of São Paulo/Brasil.**

Thesis full text available at [ReasearchGate](https://www.researchgate.net/publication/304946197_Estudo_das_propriedades_e_robustez_da_rede_de_transporte_publico_de_Sao_Paulo)

Please read the License file for terms of use of this code.  

### For any question, please contact:
sandrofsousa@gmail.com  
[@sandrofsousa](https://twitter.com/sandrofsousa)  
https://www.researchgate.net/profile/Sandro_Sousa3


### Instructions:
* `Python 3.5` required, not tested on 2.7
* Place your `GTFS` data in the corresponding folder named _gtfs_  
* Add a folder named `result` to store data from simulations  
* Check file path and adjust it according to your needs  

For more Information about GTFS format, please check:  
https://developers.google.com/transit/gtfs/
