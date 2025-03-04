# DeepGrail 2021

This part-of-speech tagger and supertagger has been developed as part of my Habilitation (Moot 2021). The file `requirements.txt` lists the Python dependencies.

You will need to download the French language model from ELMoForManyLangs for this code as well. 

https://github.com/HIT-SCIR/ELMoForManyLangs

## Depracation warning

This code is mainly preserved for historical reasons. For modern applications, I recommend the completely rebuilt version using BERT/Transformers instead of ELMo/LSTM. This gives a full parser and much more accurate supertagger.

https://www.ins2i.cnrs.fr/fr/deepgrail

## Usage

`super.py --inputfile INPUT --outputfile OUTPUT --beta B --modelfile MODEL`

- `INPUT` is the input file, a text file, defaults to `input.txt`
- `OUTPUT` is the output file, defaults to `super.txt` (the output format is explained below)
- `BETA` is the beta value, defaults to 1.0 (see below)
- `MODEL` is the model file, defaults to the included model `best_elmo_superpos.h5`

## Output format

The output format has been chosen to be compatible with the format of the old Clark and Curran supertaggers. Each sentence is one line, words are separated by space, and each supertagged word is of the following form.

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

Moot, Richard. "Type-logical investigations: proof-theoretic, computational and linguistic aspects of modern type-logical grammars." (2021).
