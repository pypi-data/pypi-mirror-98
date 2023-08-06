#!/usr/bin/env python3
"""
Figure out what is the longest sequences that can be embedded on the GPU
"""
import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from bio_embeddings.embed import name_to_embedder

logger = logging.getLogger(__name__)


def bisect_embedder_memory(embedder_name: str, model_directory: Optional[str]):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    fasta_lines = Path("test-data/titin_twice.fasta").read_text().splitlines()
    titin = "".join(fasta_lines[1:]).replace("\n", "")
    embedder = name_to_embedder[embedder_name]
    if model_directory:
        embedder = embedder(
            model_directory=str(Path(model_directory).joinpath(embedder.name))
        )
    else:
        logger.info("Model directory not given, downloading model")
        embedder = embedder()
    # Evil Hack: `not model_fallback` will now evaluate to False, but using it will still fail
    embedder.model_fallback = True

    # Binary search
    low = 0
    high = len(titin)
    while True:
        middle = (low + high) // 2
        try:
            list(embedder.embed_many([titin[:middle]], batch_size=100000))
            low = middle
            print(f"{middle} passed, new range {low} to {high}")
        except Exception as e:
            high = middle
            print(
                f"{middle} failed, new range {low} to {high}: {type(e).__name__}: {e}"
            )
        if high - low == 1:
            print(f"Max amino acids for {embedder_name}: {low}")
            break


def main():
    parser = ArgumentParser()
    parser.add_argument("embedder", help="Lowercase name of the embedder")
    parser.add_argument("--model-directory")
    args = parser.parse_args()
    if args.embedder == "all":
        for embedder_name in name_to_embedder.keys():
            bisect_embedder_memory(
                embedder_name, str(Path(args.model_directory).joinpath(embedder_name))
            )
    else:
        bisect_embedder_memory(args.embedder, args.model_directory)


if __name__ == "__main__":
    main()
