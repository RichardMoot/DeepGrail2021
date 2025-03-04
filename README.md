# DeepGrail 2021

:copyright: 2020-2025 [CNRS](http://www.cnrs.fr)

:copyright: 2020-2025 Richard Moot (@RichardMoot)

## Depracation warning

This code is mainly preserved for historical reasons. For modern applications, I recommend the completely rebuilt version using BERT/Transformers instead of ELMo/LSTM. This gives a full parser and much more accurate supertagger.

https://www.ins2i.cnrs.fr/fr/deepgrail

## About this software

These are the part-of-speech tagger and supertagger for the French language which have been developed as part of my Habilitation (Moot 2021). They have been trained on the data from the French TLGbank. The supertagger therefore assigns formulas in multimodal type-logical grammars to arbitrary French text.

The supertagger is intended for use with the GrailLight https://github.com/RichardMoot/GrailLight parser, but can be integrated in with a neural supertagger in the style of Kogkalidis, Moortgat and Moot (2020) as well.

## Installation

The file `requirements.txt` lists the Python dependencies.

You will need to download the French language model from ELMoForManyLangs for this code. 

https://github.com/HIT-SCIR/ELMoForManyLangs

You will need to change the directories in the file `super.py` for this script to function. There are two places this is necessary. The first is before the model and pickle files are loaded (add the filepath in your system to the line `os.chdir`), and the second is to ensure the ELMo model can be found (add the filepath to the line `e = Embedder`).


## Usage

`super.py --inputfile INPUT --outputfile OUTPUT --beta B --modelfile MODEL`

- `INPUT` is the input file, a text file, defaults to `input.txt`
- `OUTPUT` is the output file, defaults to `super.txt` (the output format is explained below)
- `BETA` is the beta value, defaults to 1.0 (see below)
- `MODEL` is the model file, defaults to the included model `best_elmo_superpos.h5`

## Output format

The output format has been chosen to be compatible with the format of the old Clark and Curran (2004) supertaggers. Each sentence is one line, words are separated by space, and each supertagged word is of the following form.

`Word|POS1-POS2|N|Form1|Prob1|...|FormN|ProbN`

Where

- `Word` is the current word
- `POS1` is the MElt part-of-speech tag
- `POS2` is the Treetagger part-of-speech tag
- `N` is the total number of formulas (supertags) for the current word
- `FormI` is formula number `I`
- `ProbI` is the probability assigned to formula `I`

## Beta value

The beta value is used as a way to assign multiple formulas in a way which depends on the probability of the most likely fomula. When `P` is the probability of the most likely formula and `beta=0.01`, all formulas with probability greater than `P*0.01` will be included. 

Lower beta values mean more formulas per word, whereas the default beta value of `1.0` gives only one formula per word. Lowering beta increases the coverage of a parser using the supertagger output, but reduces the efficiency. I recommend choosing a beta value so that the average number of formulas/word is in the 2-5 range for best results.

## Evaluation

The included model has the following accuracies

#### Pos1

| epochs | train | dev | test |
|--------|:-----:|:---:|:----:|
| 50     |  99.16     | 99.14    | 99.14 |

#### Pos2

| epochs | train | dev | test |
|--------|:-----:|:---:|:----:|
| 50     |  99.15     | 99.20    | 99.24 |

#### Super

| epochs | train | dev | test |
|--------|:-----:|:---:|:----:|
| 50     |  94.91    | 93.25    | 93.18 |


#### References

Clark, Stephen, and James R. Curran. "Parsing the WSJ using CCG and log-linear models." Proceedings of the 42nd Annual Meeting of the Association for Computational Linguistics (ACL-04). 2004.

Kogkalidis, Konstantinos, Michael Moortgat, and Richard Moot. "Neural Proof Nets." Proceedings of the 24th Conference on Computational Natural Language Learning. 2020.

Kogkalidis, Konstantinos, Michael Moortgat, and Richard Moot. "SPINDLE: Spinning Raw Text into Lambda Terms with Graph Attention." Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations. 2023.

Moot, Richard. "Type-logical investigations: proof-theoretic, computational and linguistic aspects of modern type-logical grammars." (2021).
