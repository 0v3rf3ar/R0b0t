# R0b0t.py

**R0b0t.py** is a powerful tool designed for ethical hackers and security researchers to retrieve and merge archived `robots.txt` files from the [Wayback Machine](https://web.archive.org/). It helps in recon tasks by downloading historical versions of `robots.txt` from a target domain and merging them for easy analysis. The tool supports timestamp file input, retry logic, progress bars, and customizable timeout for downloads.

## Features

- **Retrieve robots.txt**: Downloads archived `robots.txt` files from the Wayback Machine for a target domain.
- **Timestamp log support**: Either generates timestamp files automatically or allows custom `ts.log` file input.
- **Retry logic**: Automatically retries failed downloads after a 10-second delay.
- **Timeouts**: Customizable timeout for each download attempt.
- **Delay**: Delay between downloads so you dont ge blocked by archive.org for donwloading too many files at once.
- **Verbose mode**: Provides detailed output with progress bars and logs every action taken.
- **Merging & Sorting**: Merges and sorts the downloaded files, while skipping files with HTML tags.

## Requirements

- Python 3.x
- Libraries: `requests`, `tqdm`, `colorama`

## Installation Guide

1. Normal installation:
    ```bash
    cd  && python3 -m venv venv
    source venv/bin/activate
    git clone https://github.com/0v3rf3ar/R0b0t.git
    cd R0b0t
    pip3 install -r requirements.txt
    python3 R0b0t.py
    ```
2. Using Docker
    ```bash
    git clone https://github.com/0v3rf3ar/R0b0t.git
    cd R0b0t
   docker build -t r0b0t .
   docker run --rm -it r0b0t -h
    ```
## Usage
    usage: R0b0t.py [-u URL] [-l LIMIT] [-t TSLOG] [-v] [--timeout TIMEOUT]

    Download robots.txt from the Wayback Machine

    options:
      -u URL, --url URL     The domain to retrieve robots.txt for
      -l LIMIT, --limit LIMIT
                        Limit on the number of timestamps to retrieve
      -t TSLOG, --tslog TSLOG
                        Path to a custom ts.log file with timestamps
      -v, --verbose         Enable verbose mode
      --timeout TIMEOUT     Set a timeout for each download attempt (default: 5 seconds)
