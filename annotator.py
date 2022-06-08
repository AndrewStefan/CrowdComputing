"""This module implements the annotation of the responses 
to the open question about AI."""
import pandas as pd
import argparse
import os


def annotate(filename):
    results = pd.read_csv(filename, sep="\t")
    results.dropna(axis=1, inplace=True)
    results.drop("INPUT:Input", axis=1, inplace=True)
    results.columns = results.columns.str.replace('OUTPUT:', '')
    results = pd.DataFrame(results["artificialintelligence"])
    results["annotation"] = None

    name = input("Please enter your name:")

    i = 0
    nresponses = results.shape[0]
    while i < nresponses:
        os.system('cls||clear')
        response = results.at[i, "artificialintelligence"]
        print(f"Response [{i+1}/{nresponses}]:\n", response, "\n")
        annotation = input(
            ("Enter your annotation (0: Non-informative, 1: Neutral,"
             " 2: Informative, b: previous response, q:exit): "))
        while annotation not in ["0", "1", "2", "b", "q"]:
            annotation = input(
                ("Enter your annotation (0: Non-informative, 1: Neutral,"
                 " 2: Informative, b: previous response, q:exit): "))
        if annotation == "b":
            i -= 1
            continue
        elif annotation == "q":
            break
        results.at[i, "annotation"] = annotation
        i += 1

    results.to_csv(f"annotations_{name}.csv", sep="\t", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', "--filename", dest="f", required=True,
                        help="Path to Toloka's file with the responses.")

    args = parser.parse_args()

    annotate(args.f)
