# Pipedown :shushing_face:

Pipedown is a machine learning model pipelining package for Python.  It doesn't
really *do* much, it just lets you define a directed acyclic graph (DAG) of
modeling steps, each of which is defined as a class with `fit` and `run`
methods (like [scikit-learn](https://scikit-learn.org)), and it runs your nodes
in order and provides a visualization of the DAG.

Pipedown is designed around:

* A **single code path**: use the same code for training, validation, and inference on new test data.
* **Modularity** and **testability**: each node is defined as its own class with `fit()` and `run()` methods, making it easy to unit test each node.
* **Visibility**: pipedown comes with an html viewer to explore the structure of your DAGs, and shows links to the source code associated with each node.
* **Portability**: pipedown models can easily be trained in one environment (e.g. a batch job), serialized, and then loaded into another environment (e.g. a model server) for inference.
* **State**: DAG nodes can store state; they aren't just stateless functions.
* **Flexibility**: pipedown allows you to define models as DAGs instead of just linear pipelines (like [scikit-learn](https://scikit-learn.org/)), but doesn't force your project to have a specific file structure (like [Kedro](https://github.com/quantumblacklabs/kedro)).

Pipedown is NOT an ETL / data engineering / task scheduler tool - for that use
something like Airflow, Argo, Dask, Prefect, etc.  You can do some basic and
inefficient data processing with Pipedown, but really it's focused on creating
portable model pipelines.


* Git repository: [http://github.com/brendanhasz/pipedown](http://github.com/brendanhasz/pipedown)
* Documentation:
* Bug reports: [http://github.com/brendanhasz/pipedown/issues](http://github.com/brendanhasz/pipedown/issues)

Still in the super early stages - don't use this yet!

## Requirements

To use the visualization tools, you need to have
[graphviz](https://graphviz.org/) installed.  On Ubuntu, you can install with:

```bash
sudo apt-get install graphviz
```

## Installation

Just use pip!

```bash
pip install pipedown
```

## Getting Started

Todo...

## Thanks

Syntax higlighting in the DAG viewer is done using [higlight.js](https://highlightjs.org/)
with the great Atom One Dark ReasonML theme by Gidi Morris / Daniel Gamage.
