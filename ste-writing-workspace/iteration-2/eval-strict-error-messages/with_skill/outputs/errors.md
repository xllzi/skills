# Error messages

## The file is not found

```
Error: The system cannot find the file <path>.
Make sure that the path is correct, then try again.
```

`<path>` is the path of the config file from the command line.

## The YAML is not correct

```
Error: The file <path> contains YAML that is not correct.
Line <number>: <message>.
Correct the YAML, then try again.
```

`<path>` is the path of the config file. `<number>` is the line number of the error. `<message>` is the text from the YAML parser.

## A necessary field is missing

```
Error: The field <field> is missing in the file <path>.
Add the field <field> to the file <path>.
```

`<field>` is the name of the field. `<path>` is the path of the config file.

## The value is out of range

```
Error: The value <value> of the field <field> is out of range.
The limits are <minimum> and <maximum>.
Set the field <field> to a value between <minimum> and <maximum>.
```

`<value>` is the value in the config file. `<field>` is the name of the field. `<minimum>` and `<maximum>` are the limits of the range.
