# CFW-model-extractor
Conquest: Frontier Wars model extractor

This script can extract the model information from the .3db model files and export it to Wavefront obj.

## Requirements:
 
-  Python 3

## Running the script

```
python extractor.py path/to/file [options]
Options:
    -o <file>                           Output file name
    -s <floating point value>           Scale of the model
```

- If the output file name is not given, it will use the path of the source, just the .3db extension replaced with .obj.
- Default scale is 1.    
