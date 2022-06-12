"""This module implements the statistics calculation for the complexity 
question about the AI systems."""
import argparse
from pathlib import Path

import pandas as pd


MAPPINGS = {
    "machinetranslation": 1,
    "games": 2,
    "spamfilter": 3,
    "searchengines": 4,
    "weatherforecasts": 5,
    "chatbots": 6
}


def complexity_table(
        complexity: pd.DataFrame, variable: str,
        statistic: str = "mean") -> pd.DataFrame:
    """Return the table of `statistic` values with respect to `variable` for 
    the complexity question.

    Arguments:
        - complexity (DataFrame) : A pandas DataFrame of data for the
                                   complexity question.
        - variable (str) : Variable to search the corresponding columns for.
        - statistic (str) : Type of statistic to calculate. (Default: mean)
    """

    df = pd.DataFrame()
    for system in MAPPINGS.keys():
        temp = complexity[["orderQ", system + variable]]
        temp["orderQ"] = temp["orderQ"].apply(
            lambda x: x.index(MAPPINGS[system]))
        if statistic == "mean":
            temp = temp.groupby(system + variable).mean().T
        elif statistic == "median":
            temp = temp.groupby(system + variable).median().T
        else:
            temp = temp.groupby(system + variable).std().T
        temp.rename(index={'orderQ': system}, inplace=True)

        df = pd.concat([df, temp], axis=0)

    return df


def main(args):
    root = Path(args.save)
    root = root.with_suffix('')
    root.mkdir(parents=True, exist_ok=True)

    results = pd.read_csv(args.filename, sep="\t")

    results.dropna(axis=1, inplace=True)
    results.columns = results.columns.str.replace('OUTPUT:', '')
    results.rename(
        {
            "cgfamiliarity": "gamesfamiliarity",
            "mltfamiliarity": "machinetranslationfamiliarity",
            "cginAIdomain": "gamesinAIdomain",
            "mltinAIdomain": "machinetranslationinAIdomain"
        }, axis=1, inplace=True)

    complexity = results.filter(
        like=args.variable, axis=1).join(
        results["orderQ"])

    complexity["orderQ"] = complexity["orderQ"].apply(
        lambda x: [int(rank) for rank in x[1:-1].split(",")])

    table = complexity_table(complexity, args.variable, args.statistic)
    table.to_csv(
        root / Path(f"complexity_{args.variable}_{args.statistic}.csv"),
        index=False, float_format='%.3f')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', '-f', required=True, type=str,
                        help="Path to results file in Toloka's format")

    parser.add_argument('--save', '-s', required=True, type=str,
                        help="Path to save the statistics.")

    parser.add_argument('--variable', '-v', default="familiarity", type=str,
                        help='Variable to calculate statistics for.',
                        choices=['familiarity', 'inAIdomain'])

    parser.add_argument('--statistic', default="mean", type=str,
                        help='Statistic to calculate.',
                        choices=['mean', 'median', 'std'])

    args = parser.parse_args()

    main(args)
