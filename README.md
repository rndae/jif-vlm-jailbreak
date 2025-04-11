# Falcon 3 Test

## Overview
This project is about testing the multimodal large language model Falcon 3

## Project Structure
```
falcon-3-test
├── src
│   ├── models
│   │   ├── __init__.py
│   │   └── falcon.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── singleton.py
│   └── main.py
├── tests
│   ├── __init__.py
│   └── test_falcon.py
├── data
│   ├── images
│   │   └── SafeBench
│   └── question
│       ├── safebench.csv
│       └── SafeBench-Tiny.csv
├── requirements.txt
└── README.md
```

## Installation
To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To run the application, execute the following command:

```
python src/main.py
```

## Testing
To run the unit tests, use the following command:

```
python -m unittest discover -s tests
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.