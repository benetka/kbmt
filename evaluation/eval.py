#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Evaluation script for economic event extraction from natural lang. text
as described in paper: Cross-document Extraction of Economic Events.

To run:
eval.py -r <ground_truth_file>  -t <ml_results> -o <output folder> -v <verbose>

Example:
python eval.py -r ./data/ground_truth.tsv -t ./data/results_ml.tsv -o ./data/eval_output.txt -v true

Settings:
In config.py you can set temporal tolerance (# years) and financial tolerance (# percent).
All events with matching subject and object and containing arguments that are within these
limits will be considered as corrrectly extracted. 

Data files:
./data/ground_truth.tsv	- ground truth file for acquisitions in NYTC for selected companies
./data/results_sl.tsv	- results produced by our method (supervised learning)
./data/results_ble.tsv	- results produced by baseline-earliest method
./data/results_bll.tsv	- results produced by baseline-latest method

"""

from __future__ import division

import sys
import os
import os.path
import getopt
import csv
import math
from pprint import pprint
from twisted.web.html import output
from utils import ExtractionUtils
from config import EVAL_MONEY_TOLERANCE_PERCENT, EVAL_DATE_TOLERANCE_YEARS


class Evaluator:

    def __init__(self, gold_file, test_file, output_file, verbose=False):
        self.transactions_gold = self.readCSV(gold_file)
        self.transactions_test = self.readCSV(test_file)
        self.output_file = output_file
        self.verbose = verbose

    def evaluate_transactions(self):
        """Evaluating transaction extraction"""
        tp = 0 # correct
        fn = 0 # missed
        fp = 0 # incorrectly returned

        # file for output
        out = open(self.output_file, 'w')

        # first, iterate through the gold transactions
        for tg in self.transactions_gold:
            # check if this transaction is returned

            found = False
            for tt in self.transactions_test:
                if tg['transaction'] == tt['transaction']: # transaction type (e.g., acquire) must match
                    if self.are_equal_transactions(tg, tt):
                        found = True # at least one fitting transaction was found
                else:
                    print "Transaction types (e.g. acquire) don't match."

            if found:
                tp += 1
                expl = "Correct   => TP"
            else:
                fn += 1
                expl = "Missed    => FN"

            log = expl.ljust(20) + tg['agent_name'].ljust(40) + tg['recipient_name'].ljust(50) + tg['fin_value'].ljust(30) + tg['date'].ljust(30)
            out.write(log + "\n")

            if self.verbose:
                print log



        # go through all returned transactions, count the incorrect ones
        # duplicate TPs are ignored
        expl = "Incorrect => FP"
        for tt in self.transactions_test:
            # check if this transaction is in gold
            found = False

            for tg in self.transactions_gold:
                if tg['transaction'] == tt['transaction']:  # transaction type (e.g., acquire) must match
                    if self.are_equal_transactions(tg, tt):
                        found = True

            if (found == False):
                fp += 1
                log = expl.ljust(20) + tt['agent_name'].ljust(40) + tt['recipient_name'].ljust(50) + tt['fin_value'].ljust(30) + tt['date'].ljust(30)
                if self.verbose:
                    out.write(log + "\n")

                if self.verbose:
                    print log

        prec = tp / (tp+fp)
        rec = tp / (tp+fn)

        log = "----" + "\n" + \
              "value tolerance: " + str(EVAL_MONEY_TOLERANCE_PERCENT) + "\n" + \
              "years tolerance: " + str(EVAL_DATE_TOLERANCE_YEARS) + "\n" + \
              "----\n" + \
              "sum: TP(" + str(tp) + ") + FP(" + str(fp) + ") = " + str(tp+fp) +"\n" + \
              "# transactions test: \t"+ str(len(self.transactions_test)) +"\n" + \
              "# transactions gt: \t\t"+ str(len(self.transactions_gold)) +"\n" + \
              "----\n" + \
              "correct (TP):    " + str(tp) + "\n" +\
              "missed (FN):     " + str(fn) + "\n" +\
              "incorrect (FP):  " + str(fp) + "\n" + \
              "----\n" + \
              "Precision:       " + str(prec)[0:5]  + "\n" +\
              "Recall:          " + str(rec)[0:5] + "\n" + \
              "F1:              " + str(2*((rec*prec)/(rec+prec)))[0:5] + "\n"
        print log
        out.write("\n" + log)

        out.close()

    def are_equal_transactions(self, t1, t2):

        uri_match = False
        year_match = False
        value_match = False

        """Returns true if at least one of the agent and at least one of the
        recipient ids match"""

        # multiple uris are separated by space => split
        t1_a_d = set(t1['agent_dbpedia_id'].split(" "))
        t1_a_f = set(t1['agent_freebase_id'].split(" "))
        t1_a_c = set(t1['agent_crunchbase_id'].split(" "))
        t2_a_d = set(t2['agent_dbpedia_id'].split(" "))
        t2_a_f = set(t2['agent_freebase_id'].split(" "))
        t2_a_c = set(t2['agent_crunchbase_id'].split(" "))

        t1_r_d = set(t1['recipient_dbpedia_id'].split(" "))
        t1_r_f = set(t1['recipient_freebase_id'].split(" "))
        t1_r_c = set(t1['recipient_crunchbase_id'].split(" "))
        t2_r_d = set(t2['recipient_dbpedia_id'].split(" "))
        t2_r_f = set(t2['recipient_freebase_id'].split(" "))
        t2_r_c = set(t2['recipient_crunchbase_id'].split(" "))

        if ((len(t1_a_d) > 0 and len(t1_a_d.intersection(t2_a_d)) > 0) or \
            (len(t1_a_f) > 0 and len(t1_a_f.intersection(t2_a_f)) > 0) or \
            (len(t1_a_c) > 0 and len(t1_a_c.intersection(t2_a_c)) > 0)) \
            and \
            ((len(t1_r_d) > 0 and len(t1_r_d.intersection(t2_r_d)) > 0) or \
            (len(t1_r_f) > 0 and len(t1_r_f.intersection(t2_r_f)) > 0 ) or \
            (len(t1_r_c) > 0 and len(t1_r_c.intersection(t2_r_c)) > 0 )):
            uri_match = True

        if (self.__year_match(t1, t2, EVAL_DATE_TOLERANCE_YEARS)):
            year_match = True

        if (self.__value_match(t1, t2, EVAL_MONEY_TOLERANCE_PERCENT)):
            value_match = True

        return (uri_match and year_match and value_match)

    def __year_match(self, t1, t2, tolerance_years=0):
        """
        Extracts and compares two years.
        Possible inputs: 31/12/2005, 2008
        :param t1: record from file containing ["date"] field
        :param t2: record from file containing ["date"] field
        :param tolerance_years: tolerate margin in years
        :return: are dates equal?
        """
        y1 = ExtractionUtils.parse_date(t1.get("date")).get("year")
        y2 = ExtractionUtils.parse_date(t2.get("date")).get("year")

        return ExtractionUtils.date_equals(y1, y2, tolerance_years)

    def __value_match(self, t1, t2, threshold=0):
        """
        Compares two financial values (incl. currencies).
        If one is equal or, if there is a threshold set, in
        allowed margin, returns True.

        :param t1: record from file containing ["fin_value"] and ["currency"] fields
        :param t2: record from file containing ["fin_value"] and ["currency"] fields
        :param threshold: allowed tolerance, e.g., 0.2 = 20%
        :return: are financial values equal?
        """
        v1 = float(t1.get("fin_value"))
        v2 = float(t2.get("fin_value"))
        c1 = t1.get("currency")
        c2 = t2.get("currency")

        return ExtractionUtils.money_equals(v1, c1, v2, c2, EVAL_MONEY_TOLERANCE_PERCENT)
    
    def readCSV(self, file):
        """
        Read and parse input TSV file into a list.
        Order of tab separated values in the file:
        """
        trans = []
            
        with open(file) as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            reader.next() # skip header
            for line in reader:
                # skip empty lines
                if line[0] != "":
                    trans.append({'transaction' : line[0],
                                  'agent_name' : line[1],
                                  'agent_dbpedia_id' : line[2],
                                  'agent_freebase_id' : line[3],
                                  'agent_crunchbase_id' : line[4],
                                  'recipient_name' : line[5],
                                  'recipient_dbpedia_id' : line[6],
                                  'recipient_freebase_id' : line[7],
                                  'recipient_crunchbase_id' : line[8],
                                  'fin_value' : line[9],
                                  'currency' : line[10],
                                  'date' : line[11],
                                  'sentence' : line[12],
                                  'sentence_id' : line[13]
                                  })

        print "Document loaded: " + file + " (" + str(len(trans)) + " transactions)"

        return trans


def usage():
    print """usage: eval.py -r <reference> -t <test> -v
    -r is the gold standard (file in tsv format)
    -t is the result to be tested (file in tsv format)
    -v sets the evaluation to verbose

    example:
    -r "./gold.tsv" -t "./test.tsv" -v
    """

def main():
    gold = None
    test = None
    output = None
    verbose = False

    shortargs = 'r:t:o:v:h'
    longargs = ['ref=', 'test=', 'output=','verbose', 'help']

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-r", "--ref"):
            print "Setting reference doc to: " + a
            gold = a
        if o in ("-t", "--test"):
            print "Setting test doc to: " + a
            test = a
        if o in ("-o", "--output"):
            print "Setting output file to: " + a
            output = a
        if o in ("-v", "--verbose"):
            print "Setting output to verbose"
            verbose = True
        if o in ("-h", "--help"):
            usage()
            sys.exit()
            
    if gold is None or test is None:
        usage()
        sys.exit()

    eval = Evaluator(gold, test, output, verbose)
    eval.evaluate_transactions()

if __name__ == '__main__': 
    main()