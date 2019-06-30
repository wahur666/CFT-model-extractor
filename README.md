# CFW model extractor
Conquest: Frontier Wars model extractor

This script can extract the model information from the .3db model files and export it to Wavefront obj.

## Running the executable

The program operates with a GUI if no parameters are given, else same as the script.

```
extractor.exe path/to/file [options]
Options:
    -o <file>                           Output file name
    -s <floating point value>           Scale of the model
```

## Running the script


### Requirements:
 
-  Python 3

```
python extractor.py path/to/file [options]
Options:
    -o <file>                           Output file name
    -s <floating point value>           Scale of the model
```

- If the output file name is not given, it will use the path of the source, just the .3db extension replaced with .obj.
- Default scale is 1.    

### Building the executable

It uses Pyinstaller for building.

```
pip install pyinstaller
```

Building teh executable is done by the build.bat or with the following command:

```
pyinstaller src/extractor.py --onefile
```

The output executable is in the `dist` folder.