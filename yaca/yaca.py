#!/usr/bin/env python3
"""
YACA - Yet Another Content Auditor
"""

import argparse
import csv
import os
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main(args):
    print("YACA: Starting...")

    # Override settings from input arguments
    settings = get_project_settings()
    settings['DEPTH_LIMIT'] = args.depth
    settings['DOWNLOAD_DELAY'] = args.delay

    process = CrawlerProcess(settings)

    spider_name = 'yaca_content_audit'
    process.crawl(spider_name, domain=args.domain, children=args.children, ahrefs=args.ahrefs,
                  parent=args.parent, subdomains=args.subdomains, content_types=args.contenttype)
    # The script will block here until the crawling is finished
    process.start()
    print("YACA: Crawl finished.")

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    sanitized_domain = re.sub(r'\.', '-', re.sub(r'(https?|www\.|[^a-zA-Z0-9-\.])+', '', args.domain))
    output_file_csv = os.path.join(output_dir, sanitized_domain + ".csv")
    output_file_json = os.path.join(output_dir, sanitized_domain + ".json")

    if os.path.exists(output_file_csv):
        os.remove(output_file_csv)
    if os.path.exists(output_file_json):
        os.remove(output_file_json)

    os.rename(spider_name + ".csv", output_file_csv)
    os.rename(spider_name + ".json", output_file_json)

    # Fix empty parent column
    if not args.parent:
        with open(output_file_csv, "r") as original:
            reader = csv.reader(original)
            with open(output_file_csv + "tmp", "w+") as result:
                writer = csv.writer(result)
                header = next(reader)
                col_index = header.index("parent_url")
                del header[col_index]
                writer.writerow(header)
                for row in reader:
                    del row[col_index]
                    writer.writerow(row)
        os.remove(output_file_csv)
        os.rename(output_file_csv + "tmp", output_file_csv)

    print("YACA: Post-crawl cleanup finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Domain/URL - Starting point. "
                        "<example>.<tld>")
    parser.add_argument("-d", "--depth", action="store", default=0,
                        help="Maximum depth of the crawl (default 0=unlimited)")
    parser.add_argument("-dl", "--delay", action="store", default=0.0,
                        type=float,
                        help="Delay between individual page downloads in"
                        " seconds (float supported)")
    parser.add_argument("-c", "--children", action="store_true", default=False,
                        help="Include links within the domain in JSON output")
    parser.add_argument("-ah", "--ahrefs", action="store_true", default=False,
                        help="Include links outside the domain in JSON output")
    parser.add_argument("-p", "--parent", action="store_true", default=False,
                        help="Include parent in CSV output")
    parser.add_argument("-sd", "--subdomains", action="store_true", default=False,
                        help="Include subdomains")
    parser.add_argument("-ct", "--contenttype", action="append", default=["text/html"],
                        help="Content-Type of pages that should be crawled (default = only text/html)")
    args = parser.parse_args()
    main(args)
