# EP2 Tech Scripts

These scripts work on the files created by the tutor tools and therefore use the same core library.
As the tasks are usually only performed by the tech team, these tools aren't distributed along with the other tools.

## Installation

From this directory run:

```shell script
pip install .
```

This command fetches all dependencies and installs the launch scripts in the python runnable path.
This path is located at `python -c 'import site; print(site.USER_BASE + "/bin")'` on linux or `python -c 'import site; print(site.USER_BASE + "\\Scripts")'` on Windows.

Once this directory is added to the `PATH` environment variable, the script can be called as `ep2_tech`.

## Collecting Test Results

To collect the results of test runs use the `ep2_tech tests collect` command.
This command reads the automatic testing results of an exercise and writes a summary to the evalutation file in the tutors repository.
Additionally a statistic is generated, which displays it's information per group and as a total.

```
Usage: ep2_tech.py tests collect 
           [OPTIONS]

  Tool to collect test results produced by
  automatic testing. The results are collected,
  written to the tutor evaluation files and a
  simple statistic is created.

Options:
  --ue INTEGER  number of the exercise, WITHOUT
                leading zero  [required]

  --help        Show this message and exit.
```

To define for which exercise the results should be collected use the `--ue` option.
The tool will show a progress bar while reading the groups and will display a statistic with compilation results and test success in per cent.
Only successful compilations are used as a basis for the success rating of a test. 