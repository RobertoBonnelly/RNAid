# MScProject
Device efficient Method for clustering and comparison of large RNA dataset

# Prerequisites
python 3.6 and above
pytest

# Getting Started
As this project is still in testing stage, you can fork this repo on your local machine and test it as
instucted below.

# Installation
```
git clone git@github.com:abdulvahab/AK_Msc_Project.git(SSH)
git clone https://github.com/abdulvahab/AK_Msc_Project.git(HTTPS)
pip install pytest
```

# Usage:
```
source MScVenv/bin/activate
python src/fingerprint.py path/to/input/file.out accuracy

> accu(tanimoto) = {  'tan80'  :'0.8 to 1',
                    'tan60'  : '0.6 to 0.8',
                    'tan40'  : '0.4 to 0.6',
                    'tan20'  : '0.2 to 0.4',
                    'tanbad' : '0 to 0.2' }
```

# Examples:

```
#when current working directory is mscproject
python src/fingerprint.py input/test.out tan80
```

# Resources

https://drive.google.com/open?id=1tyL_IMTfE4r--jSxzpnx4S79o8V0UsPO


Running the tests
python -n pytest

# Contributing


# Versioning
We use git for versioning. For the versions available, see the tags on this repository.

# Author/s
Abdulvahab Kharadi | akhara01@mail.bbk.ac.uk | vahab.n@googlemail.com

# License
Need to discuss on that

# Acknowledgments
Supervisor : Dr Irilenia Nobeli | i.nobeli@bbk.ac.uk
