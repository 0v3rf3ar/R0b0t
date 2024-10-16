#!/usr/bin/env python3


import os
import re
import argparse
import requests
import time
from tqdm import tqdm  # for the progress bar
from colorama import Fore, Style, init  # for colorful output

# Initialize colorama
init(autoreset=True)

# ASCII Art Banner
def display_banner():
    banner = ''' 
  _____   ___  _      ___  _
 |  __ \\ / _ \\| |    / _ \\| |
 | |__) | | | | |__ | | | | |_   _ __  _   _
 |  _  /| | | | '_ \\| | | | __| | '_ \\| | | |
 | | \\ \\| |_| | |_) | |_| | |_ _| |_) | |_| |
 |_|  \\_\\\\___/|_.__/ \\___/ \\__(_) .__/ \\__, |
                                | |     __/ |
                                |_|    |___/
'''
    print(Fore.GREEN + banner)
    print(Fore.WHITE + "Welcome to R0b0t.py ! A Wayback Machine robots.txt downloader for recon.")
    print(Fore.WHITE + "Created by:")
    print(Fore.RED + "  Nickname  : 0v3rf3ar")
    print(Fore.RED + "  Email     : overfear@yahoo.com")
    print(Fore.RED + "  Website   : https://overfear.top\n")
    print(Fore.GREEN + "\nTS generator: https://web.archive.org/cdx/search/cdx?url=target.com/robots.txt&fl=timestamp&limit=5\n")

# Function to print messages in verbose mode
def verbose_print(verbose, message):
    if verbose:
        print(message)

# Function to download a file with progress bar and timeout handling
def download_file(url, output_path, verbose, timeout):
    retries = 2
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, disable=not verbose)
            with open(output_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()
            return True  # Successful download
        except requests.exceptions.RequestException as e:
            verbose_print(verbose, Fore.RED + f"Failed to download {url}. Retrying in 10 seconds...")
            time.sleep(10)  # Wait for 10 seconds before retrying
    return False  # Failed after retries

# Main function
def main():
    parser = argparse.ArgumentParser(description="Download robots.txt from the Wayback Machine", add_help=False)
    parser.add_argument('-u', '--url', help="The domain to retrieve robots.txt for")
    parser.add_argument('-l', '--limit', type=int, default=10, help="Limit on the number of timestamps to retrieve")
    parser.add_argument('-t', '--tslog', help="Path to a custom ts.log file with timestamps")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode")
    parser.add_argument('--timeout', type=int, default=5, help="Set a timeout for each download attempt (default: 5 seconds)")
    
    args = parser.parse_args()

    if not args.url:
        display_banner()
        parser.print_help()
        return
    
    domain_regex = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    # Clean up the domain
    clean_domain = re.sub(r'https?://', '', args.url).rstrip('/')
    if not re.match(domain_regex, clean_domain):
        print(Fore.RED + "Invalid domain format. Please use a valid domain")
        return
    
    # Create directories to store the downloaded files
    output_dir = f"robots.txt/{clean_domain}"
    os.makedirs(output_dir, exist_ok=True)

    # Download the ts.log file if not provided
    if args.tslog:
        verbose_print(args.verbose, f"Using provided timestamp file: {args.tslog}")
        ts_file = args.tslog
    else:
        timestamps_url = f"https://web.archive.org/cdx/search/cdx?url={clean_domain}/robots.txt&fl=timestamp&limit={args.limit}"
        ts_file = f"{output_dir}/ts.log"
        try:
            verbose_print(args.verbose, f"Downloading timestamps from: {timestamps_url}")
            if not download_file(timestamps_url, ts_file, args.verbose, args.timeout):
                print(Fore.RED + "Error: Could not download the timestamps. Please provide a ts.log manually.")
                return
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "Error: Could not download the timestamps. Please provide a ts.log manually.")
            return
    
    # Read timestamps from ts.log
    verbose_print(args.verbose, f"Reading timestamps from {ts_file}")
    with open(ts_file, 'r') as f:
        timestamps = f.read().splitlines()

    # Download robots.txt files for each timestamp
    downloaded_files = []
    for timestamp in timestamps:
        robot_url = f"http://web.archive.org/web/{timestamp}/http://{clean_domain}/robots.txt"
        output_file = f"{output_dir}/{timestamp}.txt"
        verbose_print(args.verbose, f"Attempting to download: {robot_url}")
        if download_file(robot_url, output_file, args.verbose, args.timeout):
            downloaded_files.append(output_file)
        else:
            print(Fore.RED + f"Failed to download robots.txt for timestamp {timestamp} after retries.")
            break  # Stop on failure after retries
    
    # Merge the downloaded files, even if some failed
    if downloaded_files:
        verbose_print(args.verbose, "Merging and sorting the downloaded files")
        merged_file = f"{output_dir}/merged.txt"
        html_tag_pattern = re.compile(r'<[^>]+>')  # Regex to detect HTML tags
        with open(merged_file, 'w') as outfile:
            lines_seen = set()
            for file_path in downloaded_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as infile:
                        content = infile.read()
                        # Check if the file contains any HTML tags
                        if html_tag_pattern.search(content):
                            verbose_print(args.verbose, f"Skipping {file_path} because it contains HTML tags")
                            continue  # Skip files containing HTML
                        for line in content.splitlines():
                            if line not in lines_seen:
                                outfile.write(line + '\n')
                                lines_seen.add(line)

        verbose_print(args.verbose, f"Done! Merged file is saved as {merged_file}")

        # If in verbose mode, print the contents of merged.txt
        if args.verbose:
            verbose_print(True, f"\n{Fore.GREEN}Content of {merged_file}:")
            with open(merged_file, 'r') as f:
                print(f.read())
    else:
        print(Fore.RED + "No files were successfully downloaded.")

if __name__ == "__main__":
    main()

