"""Search PGS catalog scores by trait, optionally filter out scores associated with a given cohort, and output results files."""

import argparse
import json
import os
import requests

import pgs_catalog_client


def write_to_json(results, filename):
    """Write out the results to a JSON file.

    Args:
        results: A list of model instances from pgs_catalog_client.
        filename: The output filename to write the JSON to.

    Note:
        You can recreate the model instance with Model(**record.to_dict())
        eg: Score(**score.to_dict())
    """

    with open(filename, "w") as f:
        f.write(json.dumps([x.to_dict() for x in results], default=str, indent=2))
        f.write("\n")


def write_filtered_score_ids(filtered_score_records, filename):
    """Write out the list of filtered score IDs to a text file.

    Args:
        filtered_score_records: List of score records (instances of Score model).
        filename: The output filename to write the score IDs to.

    Note:
        Each score ID will be written on a new line.
    """
    with open(filename, "w") as f:
        for score in filtered_score_records:
            f.write(f"{score.id}\n")


def search_scores_by_trait(trait_ids, verbose=True):
    """Search PGS catalog scores by trait_id (ontology ID, e.g., MONDO_0005148).

    Args:
        trait_ids: A list of ontology IDs to search for. This should be the ontology ID used in the PGS catalog.
        verbose: If True, print out the number of scores found.

    Returns:
        List of score records (instances of Score model) that are associated with one of the specified trait_ids.

    Note:
        See https://ftp.ebi.ac.uk/pub/databases/spot/pgs/metadata/pgs_all_metadata_efo_traits.csv for a list of valid trait IDs.
    """
    if verbose:
        print("Searching for scores associated with traits..")

    # Create an instance of the API class.
    api_instance = pgs_catalog_client.ScoreEndpointsApi()

    all_results = []
    for trait_id in trait_ids:
        # Search scores by ontology ID
        api_response = api_instance.search_scores(trait_id=trait_id)

        if len(api_response.results) == 0:
            raise ValueError(f"No scores found for trait_id: {trait_id}")

        trait_results = api_response.results

        # Handle pagination if there are more results.
        api_response = api_response.to_dict()
        done = False
        while not done:
            next_url = api_response["next"]

            if next_url is None:
                done = True
            else:
                api_response = requests.get(next_url).json()
                trait_results += [pgs_catalog_client.Score(**x) for x in api_response["results"]]

        if verbose:
            print("- Number of scores identified for {}: {}".format(trait_id, len(trait_results)))

        all_results = all_results + trait_results

    return all_results


def get_cohort_records(cohort_short_names, verbose=True):
    """Get the record for cohorts, which includes scores associated with that cohort.

    Args:
        cohort_short_names: A list of short name for the cohorts to retrieve, as used by the PGS Catalog.
        verbose: If True, print out the name (short and full) of the cohort retrieved.

    Returns:
        A list of cohort records for the specified cohort(s).

    Note:
        See https://ftp.ebi.ac.uk/pub/databases/spot/pgs/metadata/pgs_all_metadata_cohorts.csv for a list of cohorts in the PGS catalog.
    """
    if verbose:
        print("Retrieving cohort records...")

    api_instance = pgs_catalog_client.SampleEndpointsApi()
    cohort_records = []
    for cohort_short_name in cohort_short_names:
        api_response = api_instance.get_cohorts(cohort_short_name)

        if len(api_response.results) == 0:
            raise ValueError(f"No cohort found with short name: {cohort_short_name}")

        # Make sure it has only returned one record. It should, but just in case.
        assert len(api_response.results) == 1, "Expected exactly one cohort record."

        record = api_response.results[0]
        if verbose:
            print("- Retrieved cohort record for: {} ({})".format(record.name_short, record.name_full))
        cohort_records.append(record)

    return cohort_records


def remove_score_records_for_cohorts(score_records, cohort_records, development=True, evaluation=False, verbose=True):
    """Remove score records that are associated with a given cohort.

    Args:
        score_records: List of score records (instances of Score model).
        cohort_records: List of cohort records (instances of Cohort model).
        development: If True, remove scores associated with the cohort's development set.
        evaluation: If True, remove scores associated with the cohort's evaluation set.
        verbose: If True, print out the number of scores removed and remaining.

    Returns:
        List of score records (instances of Score model) filtered to those not associated with one of the cohorts.
    """

    print("Removing scores associated with cohorts...")
    scores_to_remove = set()
    for cohort_record in cohort_records:
        # Get the score IDs to remove.
        cohort_score_ids = []
        if development:
            cohort_score_ids += [x.id for x in score_records if x.id in cohort_record.associated_pgs_ids.development]
        if evaluation:
            cohort_score_ids += [x.id for x in score_records if x.id in cohort_record.associated_pgs_ids.evaluation]

        print(
            "- Number of scores associated with cohort {}: {}".format(
                cohort_record.name_short,
                len(cohort_score_ids),
            )
        )
        scores_to_remove.update(cohort_score_ids)

    # Filter out the score records.
    filtered_score_records = [score for score in score_records if score.id not in scores_to_remove]

    if verbose:
        print("- Removed {} score(s) associated with cohorts".format(len(scores_to_remove)))
        print("- Scores remaining: {}".format(len(filtered_score_records)))

    return filtered_score_records


if __name__ == "__main__":
    # Parse arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trait-id",
        type=str,
        nargs="+",
        action="extend",
        required=True,
        help="trait_id (as defined by PGS catalog) to search for. Example: MONDO_0005148",
    )
    parser.add_argument(
        "--remove",
        type=str,
        action="extend",
        nargs="+",
        required=False,
        help="Cohort short name (as defined by PGS catalog) that should be used to remove scores. Example: GERA",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        required=False,
        help="Output directory to write results to. Default: current directory",
        default=".",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="If set, suppress verbose output.",
        default=False,
    )
    args = parser.parse_args()

    verbose = not args.quiet

    score_records = search_scores_by_trait(args.trait_id, verbose=verbose)
    if args.remove:
        cohort_records = get_cohort_records(args.remove, verbose=verbose)
        filtered_records = remove_score_records_for_cohorts(score_records, cohort_records, verbose=verbose)
    else:
        filtered_records = score_records

    # Write results out to a JSON file.
    os.makedirs(args.outdir, exist_ok=True)
    if verbose:
        print(f"Writing results to directory: {args.outdir}")
    write_to_json(score_records, os.path.join(args.outdir, "all_score_records_for_trait.json"))
    if args.remove:
        write_to_json(cohort_records, os.path.join(args.outdir, "cohort_records.json"))
    # Write out the list of scores.
    write_filtered_score_ids(filtered_records, os.path.join(args.outdir, "filtered_score_ids_for_trait.txt"))
