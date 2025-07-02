""#!/usr/bin/env python3
"""
Script: download_images.py
Description:
    Bulk-download EV charging station, roadside obstacle, and background images
    using icrawler's GoogleImageCrawler, with de-duplication and post-filtering
    support to ensure category relevance.
Usage:
    python scripts/download_images.py \
        --ev-count 70 \
        --obs-count 50 \
        --bg-count 40 \
        [--output-dir data/raw] [--dedupe]
"""
import argparse
import os
import logging
from icrawler.builtin import GoogleImageCrawler
from PIL import Image
import imagehash
import imghdr

# Configure logging
def setup_logging():
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO,
        datefmt='%H:%M:%S'
    )

# Query lists
ev_queries = [
    "EV charging station",
    "electric vehicle charging point",
    "Tesla supercharger station",
    "public charging station",
    "electric car",
    "ChargePoint station",
    "Electrify America charging",
    "EV charging cable plugged in",
    "electric vehicle charging outdoor",
    "fast charging station electric car"
]
obstacle_queries = [
    "roadside barriers traffic cones",
    "construction barrels highway",
    "road work signs orange cones",
    "street barriers metal posts",
    "roadside bollards posts",
    "traffic delineators road",
    "highway construction equipment",
    "road closure barriers",
    "temporary fencing roadside",
    "street maintenance obstacles"
]
context_queries = [
    "parking lot with cars",
    "highway rest stop",
    "shopping mall parking",
    "gas station forecourt",
    "urban street parking",
    "roadside service area",
    "highway shoulder",
    "commercial parking lot"
]

# Deduplication helper
def is_duplicate(image_path, seen_hashes, hash_size=8, thresh=5):
    try:
        img = Image.open(image_path)
        h = imagehash.phash(img, hash_size=hash_size)
        for old_h in seen_hashes:
            if abs(h - old_h) < thresh:
                return True
        seen_hashes.add(h)
        return False
    except Exception:
        return False

# Basic filtering to remove invalid or unrelated files
def filter_images(directory):
    for fname in os.listdir(directory):
        path = os.path.join(directory, fname)
        if imghdr.what(path) not in ['jpeg', 'png']:  # filter invalid images
            os.remove(path)
            continue
        try:
            with Image.open(path) as img:
                img.verify()  # PIL throws if corrupt
        except Exception:
            os.remove(path)

# Download category
def download_category(queries, category_name, limit, output_dir, dedupe=False):
    target_dir = os.path.join(output_dir, category_name)
    os.makedirs(target_dir, exist_ok=True)
    logging.info(f"Downloading {category_name}: {limit} images per query into {target_dir}")

    seen_hashes = set()
    crawler = GoogleImageCrawler(storage={"root_dir": target_dir})

    for query in queries:
        logging.info(f"  Query: {query}")
        try:
            crawler.crawl(
                keyword=query,
                max_num=limit,
                min_size=(200, 200),
                file_idx_offset='auto'
            )
        except Exception as e:
            logging.warning(f"  Failed {query}: {e}")

    filter_images(target_dir)

    if dedupe:
        for fname in os.listdir(target_dir):
            fpath = os.path.join(target_dir, fname)
            if is_duplicate(fpath, seen_hashes):
                os.remove(fpath)

    logging.info(f"  Done with {category_name}")

if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(description='Download EV dataset images with Google Crawler')
    parser.add_argument('--ev-count',   type=int, default=70, help='Images per EV charging query')
    parser.add_argument('--obs-count',  type=int, default=50, help='Images per obstacle query')
    parser.add_argument('--bg-count',   type=int, default=40, help='Images per background query')
    parser.add_argument('--output-dir', type=str, default='data/raw', help='Root directory for downloaded images')
    parser.add_argument('--dedupe', action='store_true', help='Enable perceptual de-duplication')
    args = parser.parse_args()

    download_category(ev_queries, 'ev_charging',    args.ev_count,  args.output_dir, dedupe=args.dedupe)
    download_category(obstacle_queries, 'obstacles', args.obs_count, args.output_dir, dedupe=args.dedupe)
    download_category(context_queries,  'backgrounds',args.bg_count,  args.output_dir, dedupe=args.dedupe)

    logging.info('Download complete.')
