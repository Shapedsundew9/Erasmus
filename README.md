# Erasmus GP


Erasmus GP (Genetic Programming) is a scalable system to evolve computer programs.

:warning: **Erasmus GP is currently being built. It is not in a functioning state at the moment.**

## Why


Before getting in to the 'what' and 'how' the 'why' is needed for context. Erasmus GP has been built on a whim. It has been built because I
have an interest in AI, evolution and intelligence and have been in the SW industry so long I do not get to write code anymore. The architecture
and technologies used are influenced by things outside of the goals of Erasmus .i.e. what my real world teams use so I can understand what they
are doing better. The flexibility in the problem or solution space, or lack there of, is a direct reflection of my areas of interest
in the domain and my naivity of previous work. If you are reading this then maybe I have done something worthing looking at oryou are a like minded
soul. I am not closed to new directions or contributions please feel free to feedback, comment or constructively criticise.

## What


In theory there is little bound to what can be evolved the limiting factor is compute resource. In its first version Erasmus GP will be
targeted at simple classification and regression problems. The sort of stuff that is easily solved by classicial algorithms and, more recently,
artificial neural networks. If it manages that then lets see where we go from there.

## How

The lack of non-trivial results in any evolutionary domain has largely been put down to the compute resources needed. Even the primordial sludge
which could only be incorporated by the most loose definition of the word 'life' took a long time and an unimaginable
number of parallel reactions to form. For an interesting disection
on where it is all going wrong see Roman Yampolskiy's article 
[What Evolutionary Algorithms Can and Can't Do.](https://medium.com/@romanyam/what-evolutionary-algorithms-can-and-cant-do-bd8d3c86e435)
 
How will Erasmus GP break through this barrier and take evolutionary algorithms, specifically genetic programming, out of the primevil
backwaters? To answer that we need to go back to the [evolution of life](https://en.wikipedia.org/wiki/Timeline_of_the_evolutionary_history_of_life)
analogy (and it is an analogy - I do not expect that one day [HAL 9000](https://en.wikipedia.org/wiki/HAL_9000) will pop out of Erasmus GP
v[42](https://en.wikipedia.org/wiki/42_%28number%29#Popular_culture>).
Though maybe sometimes, after a few beers, I might dream that - with notibly less murder). After the sludge phase things got moving,
relatively speaking, as building block built on building block and the 
[maximum complexity](https://en.wikipedia.org/wiki/Evolution_of_biological_complexity)<sup>1</sup> of life accelerated<sup>2</sup>.
It took about 2 billion years to 
get from single celled organisms to multicellular organisms, another billion to get to the beginning of animal evolution (we are still close to
sludge at this stage), 500 millions years on and it is the start of the Triassic and dinosaurs, 250 million more and here I am typing this.
In my unenlightened opinion the key is common ancestory (analogous to transfer learning in the world of artificial neural networks) building blocks
that can make more complex blocks which themselves become primatives to even more complex blocks. Diversity of the problems being solved leads to
generalisation of the primatives and ultimately to the extinction of those that are not generalised.

A building block is a more complex concept than it is often given credit for. Building blocks need to bias useful possibilities. DNA is not
randomly combined - you cannot cross-breed a fish with a cat. There are complex and subtle checks and balances happening from the molecular
chemistry level up. It is just physics but layer upon layer of it restricting the options, constraining the solution space, evolving the evolution
mechanims. 

Erasmus GP wraps this all up with 4 features:

1. A common genomic library: Every instance uses and contributes to the same gene pool<sup>3</sup>.
2. A classification system for genes identifying the evolutionary mechanisms it is most suited too.
3. A common library for evolutionary mechanisms.
4. An infinitely scalable architecture.

This all sounds very grand but the plan is to start (very) simply and see where we go.

## Index

* [Architecture](docs/architecture.md)
* [Genomic Library](docs/genomic_library.md)
* [Glossary](docs/Glossary.md)

1. A more comprehensive discussion on complexity https://academic.oup.com/bioscience/article/59/4/333/346877
2. I have no reference to support using the term 'accelerated'. That is my opinion.
3. Well, to the extent that it is practical. Genetic isolation is a thing in the bigger picture(e.g. [Madagascar](https://en.wikipedia.org/wiki/Madagascar)