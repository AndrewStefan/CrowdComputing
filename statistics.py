import argparse
from pathlib import Path

import pandas as pd


def get_column_names(
        results: pd.DataFrame, variable: str) -> "tuple[list, list]":
    """Return the columns that correspond to `variable`

    Arguments:
        - results (DataFrame) : A pandas DataFrame of Toloka's results.
        - variable (str) : Variable to search the corresponding columns for.
    """
    cols = []
    names = []
    for col in results.columns:
        if col.endswith(variable):
            cols.append(col)
            names.append(col.removesuffix(variable))

    return cols, names


def ns_table(
        results: pd.DataFrame, nonspecific: pd.DataFrame, variable: str,
        statistic: str = "mean") -> pd.DataFrame:
    """Return the table of `statistic` with respect to `variable` for the
    non system-specific questions.

    Arguments:
        - results (DataFrame) : A pandas DataFrame of Toloka's results.
        - nonspecific (DataFrame) : A pandas DataFrame of data for the non
                                    system-specific questions.
        - variable (str) : Variable to search the corresponding columns for.
        - statistic (str) : Type of statistic to calculate. (Default: mean)
    """
    statistic_cols, names = get_column_names(results, variable)
    qdf = pd.DataFrame()
    for i in range(1, 5):
        fam_df = pd.DataFrame()
        cols = nonspecific.filter(
            like=f"Q{i}", axis=1).join(
            results.filter(like=variable, axis=1))

        for j in range(len(names)):
            var_groupby = cols.filter(
                like=names[j],
                axis=1).groupby(
                statistic_cols[j])

            if statistic == "mean":
                temp = var_groupby.mean()
            elif statistic == "median":
                temp = var_groupby.median()
            elif statistic == "std":
                temp = var_groupby.std()
            else:
                temp = var_groupby.count()

            temp = pd.DataFrame(temp.iloc[:, 0], index=[1, 2, 3, 4, 5])
            fam_df = pd.concat([fam_df, temp], axis=1)

        fam_df.columns = fam_df.columns.str.replace(f"nonspecificQ{i}", "")
        qdf = pd.concat([qdf, fam_df], axis=0)

    return qdf


def sp_table(
        results: pd.DataFrame, specific: pd.DataFrame, variable: str,
        statistic: str = "mean") -> pd.DataFrame:
    """Return the table of `statistic` with respect to `variable` for the
    system-specific questions.

    Arguments:
        - results (DataFrame) : A pandas DataFrame of Toloka's results.
        - specific (DataFrame) : A pandas DataFrame of data for the
                                 system-specific questions.
        - variable (str) : Variable to search the corresponding columns for.
        - statistic (str) : Type of statistic to calculate. (Default: mean)
    """
    metric_cols, names = get_column_names(results, variable)
    df = pd.DataFrame(columns=[1.0, 2.0, 3.0, 4.0, 5.0])
    for i in range(len(names)):
        cols = specific.join(
            results.filter(like=variable, axis=1)).filter(
            like=names[i],
            axis=1)
        if statistic == "mean":
            cols = cols.groupby(metric_cols[i]).mean().T
        elif statistic == "median":
            cols = cols.groupby(metric_cols[i]).median().T
        elif statistic == "std":
            cols = cols.groupby(metric_cols[i]).std().T
        else:
            cols = cols.groupby(metric_cols[i]).count().T
        df = pd.concat([df, cols])

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

    # Table for non system-specific questions
    nonspecific = results.filter(like="nonspecificQ", axis=1)
    nonspecific_table = ns_table(
        results, nonspecific, args.variable, args.statistic)
    nonspecific_table.to_csv(
        root / Path(f"{args.variable}_nonspecific_{args.statistic}.csv"),
        index=False, float_format='%.3f')

    # Table for system-specific questions
    specific = results.drop(
        nonspecific.columns, axis=1).filter(
        like="specificQ", axis=1).drop(
            results.filter(like="quality").columns, axis=1)
    specific_table = sp_table(results, specific, args.variable, args.statistic)
    specific_table.to_csv(
        root / Path(f"{args.variable}_specific_{args.statistic}.csv"),
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
                        choices=['mean', 'median', 'std', 'count'])

    args = parser.parse_args()

    main(args)
