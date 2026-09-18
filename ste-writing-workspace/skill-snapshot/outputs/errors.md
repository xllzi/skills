# Error messages

## Configuration not found

ERROR: Cannot find the configuration "config.yaml".
Make sure that the name and the path are correct.

## Incorrect YAML

ERROR: The YAML syntax in the configuration "config.yaml" is incorrect at line 12.
Correct the syntax at line 12.

## Missing mandatory field

ERROR: The configuration "config.yaml" does not contain the mandatory field "timeout".
Add the mandatory field and start the tool again.

## Value out of range

ERROR: The value 7200 of the field "timeout" in the configuration "config.yaml" is more than the maximum 3600.
Set the value to a number between 1 and 3600.
