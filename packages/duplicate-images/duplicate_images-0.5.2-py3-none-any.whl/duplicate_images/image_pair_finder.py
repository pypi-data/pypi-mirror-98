__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import logging
from multiprocessing.pool import ThreadPool as Pool
from pathlib import Path
from typing import Dict, List, Iterator, Optional

from PIL import Image

from duplicate_images.common import path_with_parent
from duplicate_images.function_types import Cache, CacheEntry, HashFunction, ImagePair, Results
from duplicate_images.parallel_options import ParallelOptions
from duplicate_images.progress_bar_manager import ProgressBarManager


class ImagePairFinder:

    @classmethod
    def create(  # pylint: disable = too-many-arguments
            cls, files: List[Path], hash_algorithm: HashFunction,
            parallel_options: ParallelOptions, show_progress_bar: bool = False,
            hash_store: Optional[Cache] = None
    ) -> 'ImagePairFinder':
        if parallel_options.parallel:
            return ParallelImagePairFinder(
                files, hash_algorithm, parallel_options, show_progress_bar, hash_store
            )
        return ImagePairFinder(files, hash_algorithm, show_progress_bar, hash_store)

    def __init__(
            self, files: List[Path], hash_algorithm: HashFunction, show_progress_bar: bool = False,
            hash_store: Optional[Cache] = None
    ) -> None:
        self.files = files
        self.algorithm = hash_algorithm
        self.hash_store = hash_store if hash_store is not None else {}
        self.progress_bars = ProgressBarManager.create(len(files), show_progress_bar)
        self.precalculated_hashes = self.get_hashes(files)
        self.progress_bars.close_reader()

    def get_pairs(self) -> Results:
        image_files = list(self.precalculated_hashes.keys())
        logging.info("%d hashes calculated", len(self.precalculated_hashes))
        all_pairs = (
            (file, other_file)
            for file in image_files
            for other_file in image_files[image_files.index(file) + 1:]
        )
        logging.info("Filtering duplicates")
        matches = self.filter_matches(all_pairs)
        self.progress_bars.close()
        return matches

    def precalculate_hashes(self, image_files: List[Path]) -> List[CacheEntry]:
        return [self.get_hash(file) for file in image_files]

    def filter_matches(self, all_pairs: Iterator[ImagePair]) -> Results:
        self.progress_bars.create_filter_bar(len(self.precalculated_hashes))
        return [
            (file, other_file) for file, other_file in all_pairs
            if self.are_images_equal(file, other_file)
        ]

    def are_images_equal(self, file: Path, other_file: Path) -> bool:
        self.progress_bars.update_filter()
        hash_distance = self.precalculated_hashes[file] - self.precalculated_hashes[other_file]
        logging.debug(
            "%-30s - %-30s = %d", file.stem, other_file.stem, hash_distance
        )
        return hash_distance == 0

    def get_hash(self, file: Path) -> CacheEntry:
        self.progress_bars.update_reader()
        try:
            cached = self.hash_store.get(file)
            if cached is not None:
                return file, cached

            image_hash = self.algorithm(Image.open(file))
            self.hash_store[file] = image_hash
            return file, image_hash
        except OSError as err:
            logging.warning("%s: %s", path_with_parent(file), err)
            return file, None

    def get_hashes(self, image_files: List[Path]) -> Dict[Path, int]:
        return {
            file: image_hash for file, image_hash in self.precalculate_hashes(image_files)
            if image_hash is not None
        }


class ParallelImagePairFinder(ImagePairFinder):
    def __init__(  # pylint: disable = too-many-arguments
            self, files: List[Path], hash_algorithm: HashFunction,
            parallel_options: ParallelOptions, show_progress_bar: bool = False,
            hash_store: Optional[Cache] = None
    ):
        self.parallel_options = parallel_options
        super().__init__(files, hash_algorithm, show_progress_bar, hash_store)

    def precalculate_hashes(self, image_files: List[Path]) -> List[CacheEntry]:
        with Pool() as pool:
            return pool.map(self.get_hash, image_files)


class ParallelFilteringImagePairFinder(ParallelImagePairFinder):
    """
    Not using this class at the moment since it seems too much trouble to get it to work correctly.
    See https://stackoverflow.com/a/44186168 for the reasons why.
    Keeping the code around anyway in case I want to tackle the problem of running the filtering in
    parallel one day. In that case ImagePairFinder.create() needs to return a
    ParallelFilteringImagePairFinder to utilize it.
    """
    def filter_matches(self, all_pairs: Iterator[ImagePair]) -> Results:
        pairs = list(all_pairs)
        with Pool() as pool:
            to_keep = pool.starmap(
                self.are_images_equal, pairs, chunksize=self.parallel_options.chunk_size
            )
        return [c for c, keep in zip(pairs, to_keep) if keep]
