# Migration Guide

This tool migrates the database to the new schema. The parser reads the
file. The tool analyzes the log. This improves performance.

## Steps

1. Replace the old configuration file.
2. Run the migration script.
3. If the logs show no errors, restart the server.
4. Start the validation procedure.
5. Tell the team about the results.

## Notes

The tool makes sure that the data stays consistent. You can get the full
report from the server. Refer to the README for more data about the
configuration.
