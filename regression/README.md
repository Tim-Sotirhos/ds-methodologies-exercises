# README logerror_zillow Clustering Project

Goals Overview: Identify any features that are driving the difference in Zestimate and sales price which is creating a “log error” as well as to construct a model to predict the targeted “log error.”

## Table of Contents

- [Installation](#installation)
- [Organization](#organization)
- [Planning](#planning)
- [Contributing](#contributing)

## Installation

Instructions on setting up the Zillow project and necessary steps to successfully run on any laptop. 

- Create a new repository on GitHub
- Install VS Code
- Install Sequel Pro
- Install Anaconda
- Use Jupyter Notebook

You must use Python version 3.7 or later and if you do not have PIP installed, you can download and install it from this page: [open](https://pypi.org/project/pip/).

You will be using common Data Science package libraries throughout 

## Project Organization

`logerror_zillow.ipynb` pipeline:

_**Acquisition**_
- Acquire from SQL the zillow database
_**Preperation**_
- Handle Nulls, outliers, drop variables, avoid overcomplications
_**Exploration**_
- Vizualize distributions, clustering for early discoveries
_**Modeling**_
- Create multiple models with fit/predict with train data
_**Evaluation**_
- Analyize evaluation metrics and run test data

To reporduce this project please follow along with the logerror_zillow clusterting project notebook [open](https://github.com/P-F-M/logerror_zillow) and set Random States equal to 123.

* Important - Replace the content below within your project's env.py file:
(host, user, password) 

## Project Planning

Goals: 
1. Predict the log error
2. Discover highlights from findings, vizualizations, and real estate domain
3. Lessons learned within data science, Python, SQL, etc.

Zilow data:

* Include properties with a transaction in 2017.
* Include only the last transaction for each properity.
* Include Zestimate error and date of transaction.
* Include properties that include a latitude and longitude value.
* Remove all properties that are not single family residencies properties.


Description
Installation instructions
Usage instructions
Support instructions
Contributing instructions


## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/fraction/readme-boilerplate/compare/).