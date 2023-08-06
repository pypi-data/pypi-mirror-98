![build](https://github.com/jfcrenshaw/uw_stempals_demos/workflows/build/badge.svg)
# UW STEM Pals Demos

Demo simulations for the UW STEM Pals outreach program.

Demo links (opens in Google Colabs):
1. [Pandemic Simulation](https://colab.research.google.com/github/jfcrenshaw/uw_stempals_demos/blob/main/notebooks/pandemic-demo.ipynb)
2. Galaxy Collision Simulation (need to write!)

## Details

The demos are in the `notebooks` directory.
The notebooks can be run locally by cloning the repo and installing the package.
However, they can also be from any browser via Google Colabs without any setup (which is the intended use case).
To do this, click on one of the links above.

The code code for the simulations is in the `uw_stempals_demos` directory.

## How to contribute

Anyone is welcome to contribute to the demos in this repo.
To contribute, follow these steps:
1. Fork the repo.
2. Clone your fork to your workstation.
3. From the root directory of the repo, install the package in edit mode (i.e. `pip install -e .[dev]`).
4. Create your new demo. Add the code for the new simulations as a new file in the `uw_stempals_demos` directory. Create a new Jupyter notebook for the demo in the `notebooks` directory. Make sure you add plenty of markdown text to the demo to make it self-explanatory and pedagogical. Look at the other notebooks in that folder for inspiration.
5. Add a Colab link to the list above and make sure your demo runs on Colab. Just use this link and replace `your-github-username` with your Github username and `new-demo-name.ipynb` with the name of the Jupyter notebook for your demo: `https://colab.research.google.com/github/your-github-username/uw_stempals_demos/blob/main/notebooks/new-demo-name.ipynb`
6. Open a pull request to have your new demo added to the main package.

If you want to contribute, feel free to reach out for help with any of this!
Also reach out if you want to write a simulation, but don't have any ideas.

