# portableQDA

portableQDA makes information exchange smooth using the  REFI-QDA Standard, leveraging:

- Codebooks (QDC files)
- Projects (QDPX files, not yet implemented)

Import/Export formats [QDC and QDPX](https://www.qdasoftware.org/wp-content/uploads/2019/09/REFI-QDA-1-5.pdf) are:
  - suitable for structured archiving of any kind of files, including:
    + personal corpus of information analysis (text coding, cites, comments)
    + the source documents themselves (any arbitrary format, including office docs, PDF, html, audio, surverys)
  - well-defined and maintained by the [REF-QDA working group](http://qdasoftware.org)
  - supported and developed by a growing number of participants

QDA stands for Qualitative Data Analysis, as known in social sciences. Related Wikipedia article states: “Qualitative research relies on data obtained by the researcher by first-hand observation, interviews, recordings, […]. The data are generally non-numerical. Qualitative methods include ethnography, grounded theory, discourse analysis […]. These methods have been used in sociology, anthropology, and educational research.”

## Installation

```bash
# pip install portableqda
```

## Basic usage


### testing the output format

```bash
# python -m portableqda
```

produces an empty codebook file in your home directory, should be suitable for import by your CAQDAS software. 

### testing the input format

- export a codebook from the QDA software of your choise
- run the following script:
```python
import portableqda
codebook = portableqda.codebookCls(output=None) #create a codebook, will export to the screen
codebook.readQdcFile(input="/path/to/your/exported.qdc")
codebook.writeQdcFile()
```
- no errors should ocurr, check the output for completeness


### developing


```python
# examples/ex1_codesAndSets.py
import portableqda
#look for output in system logging

codebook = portableqda.codebookCls(output="codebook_example.qdc") #create a codebook

# create 3 codes and group them in two sets
for number in range(3):
    codebook.createElement(elementCls=portableqda.codeCls,
                                                name=f"code{number}",
                                                sets=["set1","set2"])
    # for error checking, see examples/ex2_flowControl.py 
    
codebook.writeQdcFile() # export the codebook as a REFI-QDA 1.5 compatible QDC file
```

Look for the file `codebook_example.qdc` at your home directory. You can see more of what's happening (portableQDA is a library thus not intended for direct use), inserting the following code where the comment "look for output in system logging" is, right after the `import portableqda` statement:

```python
import logging
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
portableqda.log.addHandler(handler)
portableqda.log.setLevel(logging.DEBUG)
```

Something like this will be shown:

 ```log
 portableqda.refi_qda - DEBUG - tree created, root node: 'CodeBook'. see REFI-QDA 1.5
portableqda.refi_qda - INFO - output is C:\Users\X\codebook_example.qdc
portableqda.refi_qda - DEBUG - added code code0 to set set1 
portableqda.refi_qda - DEBUG - added code code0 to set set2 
portableqda.refi_qda - DEBUG - added code code1 to set set1 
portableqda.refi_qda - DEBUG - added code code1 to set set2 
portableqda.refi_qda - DEBUG - added code code2 to set set1 
portableqda.refi_qda - DEBUG - added code code2 to set set2 
portableqda.refi_qda - INFO - exporting as REFI-QDC  codebook to file: C:\Users\X\codebook_example.qdc
 ```


## Documentation

## Contributing

### Acknowledges

LMXL: portableQDA relies on the excellent [lxml package](http://lxml.de) for the  underlying tree data structure and  XML handling
REFI-QDA: [working group](http://qdasoftware.org) pushing interoperability and open standards



## License

GNU Lesser General Public License v3 (LGPLv3)