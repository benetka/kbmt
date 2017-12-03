# Towards Building a Knowledge Base of Monetary Transactions from a News Collection

This repository contains resources developed within the following paper:

	Towards Building a Knowledge Base of Monetary Transactions from a News Collection, J. Benetka, K. Balog, and K. Nørvåg. 
	In proceedings of 17th ACM/IEEE-CS Joint Conference on Digital Libraries (JCDL ’17), June 2017.


You can find the [paper](https://github.com/benetka/kbmt/blob/master/benetka-2017-Towards_Building_a_Knowledge_Base_of_Monetary_Transactions.pdf) and the [presentation](https://github.com/benetka/kbmt/blob/master/presentation/benetka-kbmt-presentation-jcdl2017.pdf) in this repository.

## Contents of the repository
This repository contains resources used and described in the paper.

The repository is structured as follows:

- `algorithms/`: Formal description of algorithm for entity normalization and sentence clustering.
- `data/`: Dataset with two types of monetary transactions used for training/evaluation of proposed methods.
- `evaluation/`: Evaluation script.
- `ontology/`: Proposed ontology as OWL file and PDF preview.
- `presentation/`: PDF of paper presentation from JCDL 2017.

## Paper abstract
We address the problem of extracting structured representations of economic events from a large corpus of news articles, using a combination of natural language processing and machine learning techniques. The developed techniques allow for semi-automatic population of a financial knowledge base, which, in turn, may be used to support a range of data mining and exploration tasks.

The key challenge we face in this domain is that the same event is often reported multiple times, with varying correctness of details.  We address this challenge by first collecting all information pertinent to a given event from the entire corpus, then considering all possible representations of the event, and finally, using a supervised learning method, to rank these representations by the associated confidence scores. A main innovative element of our approach is that it jointly extracts and stores all attributes of the event as a single representation (quintuple). 

Using a purpose-built test set we demonstrate that our supervised learning approach can achieve 25\% improvement in F1-score over baseline methods that consider the earliest, the latest or the most frequent reporting of the event.


## Citation

If you use the resources presented in this repository, please cite:

```
@inproceedings{Benetka:2017:TBK,
	author = {Benetka, Jan R. and Balog, Krisztian and N{\o}rv{\aa}g, Kjetil},
	title = {Towards Building a Knowledge Base of Monetary Transactions from a News Collection},
	booktitle = {Proceedings of the 17th ACM/IEEE-CS Joint Conference on Digital Libraries},
	series = {JCDL '17},
	doi = {10.1109/JCDL.2017.7991575},
	year = {2017}
}
```

## Contact

If you have any questions, feel free to drop an e-mail to Jan R. Benetka at <benetka@idi.ntnu.no>.
