#!/usr/bin/env python
"""
An example of a step using MLflow and Weights & Biases
"""
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_local_path = artifact.file()

    df = pd.read_csv(artifact_local_path)

    logger.info("Cleaning artifact")

    logger.info(df.count())

    logger.info("Dropping duplicates")

    df = df.drop_duplicates()

    logger.info(df.count())

    #dropping NaNs also dropped the out-of-area location which caused not to assert with sample2.csv
    #commenting out but leaving it for future reference
    
    #logger.info("Dropping NaNs")

    #df = df.dropna()

    #logger.info(df.count())

    logger.info("Dropping outliers")
    #min_price = 10
    #max_price = 350
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info("Convert last_review to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Final count")

    logger.info(df.count())

    #idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    #df = df[idx].copy()

    df.to_csv(args.output_artifact, index=False)


    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Output file type",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Output description",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Min price to consider when searching",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Max price to consider when searching",
        required=True
    )


    args = parser.parse_args()

    go(args)
