# file_encrypter

## Table of Contents
1. [How to run](#how-to-run)
    - 1.1. [Arguments](#arguments)
    - 1.2. [Tests](#tests)

## How to run
Run the following command:
```bash
cd src
python3 main.py [-h] [-d] -p [--env-path ENV_PATH] paths [paths ...]
```

### Arguments
1. `[-h]` pr `[--help]`: Shows a help message and exits.
2. `[-d]` or `[--decrypt]`: This flag tells the program to decrypt the files instead of encrypting.
3. `[-p]` or `[--password]: Prompts the user to insert their password.
4. `[--env-path]`: The path to the .env file to which the salt will be saved.
5. `[paths ...]`: **Positional argument;** will always come after all the others. The paths of the files to be encrypted separated by a space.

### Tests
