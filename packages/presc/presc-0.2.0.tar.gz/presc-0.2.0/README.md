# PRESC: Performance and Robustness Evaluation for Statistical Classifiers

[![CircleCI](https://circleci.com/gh/mozilla/PRESC.svg?style=svg)](https://circleci.com/gh/mozilla/PRESC)
[![Join the chat at https://gitter.im/PRESC-outreachy/community](https://badges.gitter.im/PRESC-outreachy/community.svg)](https://gitter.im/PRESC-outreachy/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

PRESC is a toolkit for the evaluation of machine learning classification
models.
Its goal is to provide insights into model performance which extend beyond
standard scalar accuracy-based measures and into areas which tend to be
underexplored in application, including:

- Generalizability of the model to unseen data for which the training set may
  not be representative
- Sensitivity to statistical error and methodological choices
- Performance evaluation localized to meaningful subsets of the feature space
- In-depth analysis of misclassifications and their distribution in the feature
  space

More details about the specific features we are considering are presented in the
[project roadmap](./docs/ROADMAP.md).
We believe that these evaluations are essential for developing confidence in
the selection and tuning of machine learning models intended to address user
needs, and are important prerequisites towards building
[trustworthy AI](https://foundation.mozilla.org/en/internet-health/trustworthy-artificial-intelligence/).

As a tool, PRESC is intended for use by ML engineers to assist in the
development and updating of models.
It is usable in the following ways:

- As a standalone tool which produces a graphical report evaluating a given
  model and dataset
- As a Python package/API which can be integrated into an existing pipeline

A further goal is to use PRESC:

- As a step in a Continuous Integration workflow: evaluations run as a part of
  CI, for example, on regular model updates, and fail if metrics produce
  unacceptable values.

For the time being, the following are considered __out of scope__:

- User-facing evaluations, eg. explanations
- Evaluations which depend explicitly on domain context or value judgements of
  features, eg. protected demographic attributes. A domain expert could use
  PRESC to study misclassifications across such protected groups, say, but the
  PRESC evaluations themselves should be agnostic to such determinations.
- Analyses which do not involve the model, eg. class imbalance in the training
  data

There is a considerable body of recent academic research addressing these
topics, as well as a number of open-source projects solving related problems.
Where possible, we plan to offer integration with existing tools which align
with our vision and goals.

## Documentation

Project documentation is available
[here](https://mozilla.github.io/PRESC/index.html)
and provides much more detail, including:

- Getting set up
- Running a report
- Computing evaluations
- Configuration
- Package API

### Examples

An example script demonstrating how to run a report is available
[here](./examples/report/sample_report.py).

There are a number of notebooks and explorations in the
[`examples/`](./examples/)
dir, but they are not guaranteed to run or be up-to-date as the package has
undergone major changes recently and we have not yet finished updating these.

Some well-known datasets are provided in CSV format in the
[`datasets/`](./datasets/)
dir for exploration purposes.


## Notes for contributors

Contributions are welcome.
We are using the repo [issues](https://github.com/mozilla/PRESC/issues) to
manage project tasks in alignment with the [roadmap](./docs/ROADMAP.md), as well
as hosting discussions.
You can also reach out on [Gitter](https://gitter.im/PRESC-outreachy/community).

We recommend that submissions for new feature implementations include a Juypter
notebook demonstrating their application to a real-world dataset and model.

This repo adheres to [Python black](https://pypi.org/project/black/)
formatting, which is enforced by a pre-commit hook (see below).


## Setting up a dev environment

Make sure you have conda (eg. [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
installed. `conda init` should be run during installation to set the PATH
properly.

Set up and activate the environment. This will also enable a pre-commit hook to
verify that code conforms to flake8 and black formatting rules.
On Windows, these commands should be run from the Anaconda command prompt.

```shell
$ conda env create -f environment.yml
$ conda activate presc
$ python setup.py develop
$ pre-commit install
```

To run tests:

```shell
$ pytest
```

## MozFest 2021: AI IRL Hackathon

Welcome MozFest participants!

Please log into the MozFest Slack instance and join the `#presc` channel, as
this will be our main medium of communication. We will also be chatting over
Spatial Chat and Zoom.

Please see the
[documentation](https://mozilla.github.io/PRESC/index.html)
for help on getting started.
As described there, you can either install the package using `pip` for
immediate use, or clone this repository and set up the environment for
development work.

The main tasks we would ask you to work on are the following:

- Test out the package functionality. Try running the report on a
  classification model and dataset. You can also try running individual
  evaluations in a Jupyter notebook.
    * If you don't have a dataset or classification model to work with, you can
      use one of the datasets in the repo, and create a classifier using
      `scikit-learn`. Some examples are given in the [`examples/`](./examples)
      dir. Feel free to share your results in the Slack channel.
    * If you can apply PRESC to a classification problem you have already been
      working on, we'd be very excited to hear your feedback. If your data &
      model can be considered public, you are welcome to submit any artifacts to
      our `examples/` dir.
- Please open issues for any bugs you encounter (including things that don't
  work as you expect or aren't well explained).
    * If you want to offer a PR for a fix, that is welcome too.
- We would welcome any feedback on the general approach, the evaluations
  described in the roadmap, the results you get from running PRESC, etc,
  including similar projects you're familiar with. We can discuss in Slack, and
  you can also open an issue to post specifics and to open the discussion to the
  broader community.
- There are a few issues listed in the repo, and more will likely be opened
  during the day. Because the project is still relatively young, they are more
  related to implementing major features and exploring methodologies than fixing
  specific bugs. If you are interested to work on one of these you are welcome
  to, and it's fine if you are not able to fully complete the task during the
  limited timespan of the hackathon.


