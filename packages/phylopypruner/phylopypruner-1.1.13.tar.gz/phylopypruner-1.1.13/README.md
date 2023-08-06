<img src="https://gitlab.com/fethalen/phylopypruner/raw/master/doc/images/ppp_logo.png" alt="ppp_logotype" width="350"/>

## About

*Orthologs* are genes that are related through a speciation event, while
*paralogs* are genes that are related through a gene duplication event.
Accurate identification of orthologs is a prerequisite for phylogenomics, since
including genes that diverged because of a gene duplication event for species
tree inference can cause an erroneous inference of speciation nodes, due to
disparencies between individual gene trees and the species tree. Unfortunately,
contaminants present in even a single taxon can cause a tree-based orthology
inference method to erroneuosly infer paralogy and unnecessarily exclude
sequences.

PhyloPyPruner is a Python package for phylogenetic tree-based orthology
inference, using the species overlap method. It uses trees and alignments
inferred from the output of a graph-based orthology inference approach, such
as [OrthoMCL](https://www.ncbi.nlm.nih.gov/pubmed/12952885),
[OrthoFinder](https://www.ncbi.nlm.nih.gov/pubmed/26243257) or
[HaMStR](https://www.ncbi.nlm.nih.gov/pubmed/19586527), in order to obtain sets
of sequences that are 1:1 orthologous. In addition to algorithms seen in
pre-existing tree-based tools (for example,
[PhyloTreePruner](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3825643/),
[UPhO](https://academic.oup.com/mbe/article/33/8/2117/2578877),
[Agalma](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3840672/) or
[Phylogenomic Dataset
Reconstruction](https://www.ncbi.nlm.nih.gov/pubmed/25158799)), this package
provides new methods for reducing potential contamination.

![proteomes2orthologs](https://gitlab.com/fethalen/phylopypruner/raw/master/doc/images/proteomes2orthologs.png)

**Figure 1.** A rough overview of a tree-based orthology inference approach.

## Quick installation

The easiest way to install PhyloPyPruner is by using the package manager for
Python, [pip](https://pypi.org/project/pip/):

```bash
pip install phylopypruner # install for all users
pip install --user phylopypruner # install for the current user only
```

Once installed, the program is located within `$HOME/.local/bin`. Depending on
your OS, you might have to add the directory to your `$PATH` to avoid typing
the entire path. Once in your path, you run the program like this:

```bash
phylopypruner
```

## [Documentation](https://gitlab.com/fethalen/phylopypruner/wikis)

1. [About PhyloPyPruner](https://gitlab.com/fethalen/phylopypruner/wikis/introduction)
2. [Tutorial](https://gitlab.com/fethalen/phylopypruner/wikis/tutorial#phylopypruner-tutorial)
3. [Installation](https://gitlab.com/fethalen/phylopypruner/wikis/installation)
4. [Input data](https://gitlab.com/fethalen/phylopypruner/wikis/input-data)
5. [Output files](https://gitlab.com/fethalen/phylopypruner/wikis/output-files)
6. [Methods](https://gitlab.com/fethalen/phylopypruner/wikis/methods)
7. [Options](https://gitlab.com/fethalen/phylopypruner/wikis/options)

## Cite

Our manuscript is still in preparation, it will be posted here once a preprint
of the article is available.

© [Kocot Lab](https://www.kocotlab.com/) 2019
