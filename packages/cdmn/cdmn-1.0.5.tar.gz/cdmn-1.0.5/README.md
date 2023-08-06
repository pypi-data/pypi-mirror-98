# cDMN

## Welcome to the cDMN solver's code repository.

cDMN stands for Constraint Decision and Model Notation.
It is an extension to the [DMN](https://www.omg.org/spec/DMN/About-DMN/) standard, managed by the Object Management Group (OMG).
cDMN combines the readability and straighforwardness of DMN and the expressiveness and flexibility of constraint reasoning.
For more specific details, please visit our [cDMN documentation](https://cdmn.readthedocs.io/en/latest/notation.html).

## Examples

Example implementations can also be found in the [cDMN documentation](https://cdmn.readthedocs.io/en/latest/examples.html).

## Installation and usage

The full installation and usage guide for the cDMN solver can be found [here](https://cdmn.readthedocs.io/en/latest/solver.html).
In short for Linux: after cloning this repo, install the Python dependencies.

```
git clone https://gitlab.com/EAVISE/cdmn/cdmn-solver
cd cdmn-solver
pip3 install -r requirements.txt
```

After this, you can run the solver. Example usage is as follows:

```
python3 -O solver.py Name_Of_XLSX.xlsx -n "Name_Of_Sheet" -o output_name.idp
```

## Reference

If you used cDMN in a publication or in other works, reference us as follows:

BibTeX:
```
@incollection{AertsBram2020TtDC,
series = {Lecture Notes in Computer Science},
issn = {0302-9743},
pages = {23--38},
publisher = {Springer International Publishing},
booktitle = {Rules and Reasoning},
isbn = {9783030579760},
year = {2020},
title = {Tackling the DMN Challenges with cDMN: A Tight Integration of DMN and Constraint Reasoning},
copyright = {Springer Nature Switzerland AG 2020},
language = {eng},
address = {Cham},
author = {Aerts, Bram and Vandevelde, Simon and Vennekens, Joost},
}


```

or direct cite:

```
Aerts, Bram, et al. “Tackling the DMN Challenges with CDMN: A Tight Integration of DMN and Constraint Reasoning.” Rules and Reasoning, Springer International Publishing, Cham, 2020, pp. 23–38. Lecture Notes in Computer Science.
```
