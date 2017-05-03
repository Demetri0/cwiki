# cwiki
Wikipedia searching from the command line!

## Installation
(This probably isn't the best way, but here it goes)

1. Download the latest version of cwiki - [https://github.com/Demetri0/cwiki/releases](https://github.com/Demetri0/cwiki/releases).
2. Open up your terminal app of choice.
3. Navigate to the folder containing the "cwiki.py" file.
4. Add the executable permission to the file: `chmod +x cwiki.py`.
5. Move the file to the usr/local/bin directory so it can be launched as a command: `mv cwiki.py /usr/local/bin`.

Then you can run a wikipedia search by typing `cwiki.py` followed by your query (If it's a multi-word query you'll need to use speech marks.). 

## Usage
- `cwiki.py anime`
- `cwiki.py anime -c 4` or `cwiki.py anime --count 4`
- `cwiki.py anime -l ru` or `cwiki.py anime --lang ru`
