# clstr-parser

Parses clstr file format for converstion to a tab separated file specified by UNR 
Bioinformatics.  The parser pulls out clusters with percentages. There may be 
multiple lines that list a percentage for each cluster.

The desired output columns are:
Cluster, Identifier 1, Identifier 2, Percentage

Example:

```
>Cluster 4
0       13038nt, >iceplant_tr_11521... *
1       637nt, >MCGI0001S00008421... at +/99.69%
```

The desired output of this example is:

```
'4\ticeplant_tr_11521\tMCGI0001S00008421\t0.9969'
```

The parsed data is not generally usable because it ignores important clstr fields,
and is designed to structure output data in a bizarre way.

No clstr documentation was referenced in the creation of this parser.  Nomenclature
is likely wrong.

Two scripts are included.

- clstr_to_tsv.py converts clstr files to TSV
- clstr_counter.py counts the number of lines that contain a percentage

## General usage

```
$ python clstr_to_tsv.py input_file.clstr > output.tsv
```
or
```
$ python clstr_to_tsv.py -f output.tsv input_file.clstr
```

```
$ python clstr_counter.py input_file.clstr
```

Users may make scripts executable by adding execute permissions.

```
$ chmod u+x clstr_to_tsv.py
$ chmod u+x clstr_counter.py
```