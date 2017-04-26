Evaluation script for economic event extraction from natural lang. text
as described in paper: Building a Knowledge Base of Monetary Transactions.

To run:
eval.py -r <ground_truth_file>  -t <ml_results> -o <output folder> -v <verbose>

Example:
python eval.py -r ./data/ground_truth.tsv -t ./data/results_sl.tsv -o ./data/eval_output.txt -v true

Settings:
In config.py you can set temporal tolerance (# years) and financial tolerance (# percent).
All events with matching subject and object and containing arguments that are within these
limits will be considered as corrrectly extracted. 

Data files:
./data/ground_truth.tsv	- ground truth file for acquisitions in NYTC for selected companies
./data/results_sl.tsv	- results produced by our method (supervised learning)
./data/results_ble.tsv	- results produced by baseline-earliest method
./data/results_bll.tsv	- results produced by baseline-latest method

