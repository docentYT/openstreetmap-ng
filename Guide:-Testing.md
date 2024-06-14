## Running Tests

To run tests once, simply run:

```sh
run-tests
```

This command will execute all the tests and display the results in the terminal. Additionally, a `.coverage` file will be automatically produced, which can be used by other tools and IDEs to display code coverage.

## Running Tests on Code Changes

If you prefer to run tests automatically whenever you make changes to your code, you can use:

```sh
watch-tests
```

This command will monitor the project for changes and automatically re-run the tests. The results will be displayed in the terminal. The code coverage file is also updated.