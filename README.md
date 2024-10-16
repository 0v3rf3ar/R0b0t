# R0b0t.py

**R0b0t.py** is a powerful tool designed for ethical hackers and security researchers to retrieve and merge archived `robots.txt` files from the [Wayback Machine](https://web.archive.org/). It helps in recon tasks by downloading historical versions of `robots.txt` from a target domain and merging them for easy analysis. The tool supports timestamp file input, retry logic, progress bars, and customizable timeout for downloads.

## Features

- **Retrieve robots.txt**: Downloads archived `robots.txt` files from the Wayback Machine for a target domain.
- **Timestamp log support**: Either generates timestamp files automatically or allows custom `ts.log` file input.
- **Retry logic**: Automatically retries failed downloads after a 10-second delay.
- **Timeouts**: Customizable timeout for each download attempt.
- **Verbose mode**: Provides detailed output with progress bars and logs every action taken.
- **Merging & Sorting**: Merges and sorts the downloaded files, while skipping files with HTML tags.

## Requirements

- Python 3.x
- Libraries: `requests`, `tqdm`, `colorama`

## Installation Guide

1. Clone the repository:
    ```bash
    cd  && python3 -m venv venv
    source venv/bin/activate
    git clone https://github.com/0v3rf3ar/R0b0t.git
    cd R0b0t
    pip3 install -r requirements.txt
    python3 R0b0t.py
    ```
## Usage

### Basic Usage

```bash
python R0b0t.py -u target.com -l 5 -v
