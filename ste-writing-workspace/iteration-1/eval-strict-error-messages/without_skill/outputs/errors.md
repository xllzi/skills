# Error messages: configuration file validator

Each message goes to the terminal. Each message gives the cause and the action.
Use the exact text below. Replace the text in angle brackets with the real value.

## 1. File not found

```
ERROR: Cannot find the configuration file "<path>".
Action: Make sure that the path is correct. Then run the command again.
```

## 2. Invalid YAML

```
ERROR: The configuration file "<path>" contains invalid YAML.
Cause: The YAML parser stopped at line <line>, column <column>.
Action: Correct the YAML syntax at line <line>. Then run the command again.
```

## 3. Missing required field

```
ERROR: The configuration file "<path>" has no value for the required field "<field>".
Action: Add the field "<field>" to the configuration file. Then run the command again.
```

## 4. Value out of range

```
ERROR: The value of the field "<field>" is out of range.
Cause: The value is <value>. The permitted range is <min> to <max>.
Action: Set the value of the field "<field>" to a number from <min> to <max>. Then run the command again.
```

## Rules for these messages

- One message gives one error. Do not put two errors in one message.
- Use the labels `ERROR:`, `Cause:`, and `Action:` in this sequence. Give the cause only when the tool knows it.
- Write the action as a command. Use the imperative form.
- Keep each sentence to 20 words or less.
- Use the present tense and the active voice.
- Use "must" for a requirement and "can" for a possible condition. Do not use "should".
- Do not use contractions. Write "do not", not "don't".
- Do not use "-ing" verb forms.
- Write "configuration file". Do not write "config file".
- Give the file path, the field name, and the line number. A user does not have to open the file to find the error.
- Use angle brackets for variable text. Do not use angle brackets for other purposes.
