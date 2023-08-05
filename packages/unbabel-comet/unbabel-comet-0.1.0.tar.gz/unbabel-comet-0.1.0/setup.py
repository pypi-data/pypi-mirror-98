# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comet',
 'comet.metrics',
 'comet.models',
 'comet.models.encoders',
 'comet.models.estimators',
 'comet.models.ranking',
 'comet.modules',
 'comet.tokenizers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.0,<5.4.0',
 'fairseq==0.9.0',
 'fsspec==0.8.7',
 'numpy<1.20.0',
 'pandas>=1.0.0,<2.0.0',
 'pytorch-lightning<=1.3',
 'pytorch-nlp==0.5.0',
 'scikit-learn==0.24',
 'scipy>=1.5.0,<1.6.0',
 'sentencepiece==0.1.91',
 'tensorboard==2.2.0',
 'torch<=1.6',
 'transformers>=4.0.0,<5.0.0']

entry_points = \
{'console_scripts': ['comet = comet.cli:comet']}

setup_kwargs = {
    'name': 'unbabel-comet',
    'version': '0.1.0',
    'description': 'High-quality Machine Translation Evaluation',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/Unbabel/COMET/master/docs/source/_static/img/COMET_lockup-dark.png">\n  <br />\n  <br />\n  <a href="https://github.com/Unbabel/COMET/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Unbabel/COMET" /></a>\n  <a href="https://github.com/Unbabel/COMET/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Unbabel/COMET" /></a>\n  <a href=""><img alt="PyPI" src="https://img.shields.io/pypi/v/unbabel-comet" /></a>\n  <a href="https://github.com/psf/black"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-black" /></a>\n</p>\n\n\n## Quick Installation\n\nDetailed usage examples and instructions can be found in the [Full Documentation](https://unbabel.github.io/COMET/html/index.html).\n\nSimple installation from PyPI\n\n```bash\npip install unbabel-comet\n```\n\nTo develop locally install [Poetry](https://python-poetry.org/docs/#installation) and run the following commands:\n```bash\ngit clone https://github.com/Unbabel/COMET\npoetry install\n```\n\n## Scoring MT outputs:\n\n### Via Bash:\n\nExamples from WMT20:\n\n```bash\necho -e "Dem Feuer konnte Einhalt geboten werden\\nSchulen und Kindergärten wurden eröffnet." >> src.de\necho -e "The fire could be stopped\\nSchools and kindergartens were open" >> hyp.en\necho -e "They were able to control the fire.\\nSchools and kindergartens opened" >> ref.en\n```\n\n```bash\ncomet score -s src.de -h hyp.en -r ref.en\n```\n\nYou can export your results to a JSON file using the `--to_json` flag and select another model/metric with `--model`.\n\n```bash\ncomet score -s src.de -h hyp.en -r ref.en --model wmt-large-hter-estimator --to_json segments.json\n```\n\n### Via Python:\n\n```python\nfrom comet.models import download_model\nmodel = download_model("wmt-large-da-estimator-1719")\ndata = [\n    {\n        "src": "Dem Feuer konnte Einhalt geboten werden",\n        "mt": "The fire could be stopped",\n        "ref": "They were able to control the fire."\n    },\n    {\n        "src": "Schulen und Kindergärten wurden eröffnet.",\n        "mt": "Schools and kindergartens were open",\n        "ref": "Schools and kindergartens opened"\n    }\n]\nmodel.predict(data, cuda=True, show_progress=True)\n```\n\n### Simple Pythonic way to convert list or segments to model inputs:\n\n```python\nsource = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]\nhypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]\nreference = ["They were able to control the fire.", "Schools and kindergartens opened"]\n\ndata = {"src": source, "mt": hypothesis, "ref": reference}\ndata = [dict(zip(data, t)) for t in zip(*data.values())]\n\nmodel.predict(data, cuda=True, show_progress=True)\n```\n\n**Note:** Using the python interface you will get a list of segment-level scores. You can obtain the corpus-level score by averaging the segment-level scores\n\n## Model Zoo:\n\n| Model              |               Description                        |\n| :--------------------- | :------------------------------------------------ |\n| ↑`wmt-large-da-estimator-1719` | **RECOMMENDED:** Estimator model build on top of XLM-R (large) trained on DA from WMT17, WMT18 and WMT19 |\n| ↑`wmt-base-da-estimator-1719` | Estimator model build on top of XLM-R (base) trained on DA from WMT17, WMT18 and WMT19 |\n| ↓`wmt-large-hter-estimator` | Estimator model build on top of XLM-R (large) trained to regress on HTER. |\n| ↓`wmt-base-hter-estimator` | Estimator model build on top of XLM-R (base) trained to regress on HTER. |\n| ↑`emnlp-base-da-ranker`    | Translation ranking model that uses XLM-R to encode sentences. This model was trained with WMT17 and WMT18 Direct Assessments Relative Ranks (DARR). |\n\n#### QE-as-a-metric:\n\n| Model              |               Description                        |\n| -------------------- | -------------------------------- |\n| `wmt-large-qe-estimator-1719` | Quality Estimator model build on top of XLM-R (large) trained on DA from WMT17, WMT18 and WMT19. |\n\n## Train your own Metric: \n\nInstead of using pretrained models your can train your own model with the following command:\n```bash\ncomet train -f {config_file_path}.yaml\n```\n\n### Supported encoders:\n- [Learning Joint Multilingual Sentence Representations with Neural Machine Translation](https://arxiv.org/abs/1704.04154)\n- [Massively Multilingual Sentence Embeddings for Zero-Shot Cross-Lingual Transfer and Beyond](https://arxiv.org/abs/1812.10464)\n- [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805.pdf)\n- [XLM-R: Unsupervised Cross-lingual Representation Learning at Scale](https://arxiv.org/pdf/1911.02116.pdf)\n\n\n### Tensorboard:\n\nLaunch tensorboard with:\n```bash\ntensorboard --logdir="experiments/"\n```\n\n## Download Command: \n\nTo download public available corpora to train your new models you can use the `download` command. For example to download the APEQUEST HTER corpus just run the following command:\n\n```bash\ncomet download -d apequest --saving_path data/\n```\n\n## unittest:\nIn order to run the toolkit tests you must run the following command:\n\n```bash\ncoverage run --source=comet -m unittest discover\ncoverage report -m\n```\n\n## Publications\n\n```\n@inproceedings{rei-etal-2020-comet,\n    title = "{COMET}: A Neural Framework for {MT} Evaluation",\n    author = "Rei, Ricardo  and\n      Stewart, Craig  and\n      Farinha, Ana C  and\n      Lavie, Alon",\n    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",\n    month = nov,\n    year = "2020",\n    address = "Online",\n    publisher = "Association for Computational Linguistics",\n    url = "https://www.aclweb.org/anthology/2020.emnlp-main.213",\n    pages = "2685--2702",\n}\n```\n\n```\n@inproceedings{rei-EtAl:2020:WMT,\n  author    = {Rei, Ricardo  and  Stewart, Craig  and  Farinha, Ana C  and  Lavie, Alon},\n  title     = {Unbabel\'s Participation in the WMT20 Metrics Shared Task},\n  booktitle      = {Proceedings of the Fifth Conference on Machine Translation},\n  month          = {November},\n  year           = {2020},\n  address        = {Online},\n  publisher      = {Association for Computational Linguistics},\n  pages     = {909--918},\n}\n```\n\n```\n@inproceedings{stewart-etal-2020-comet,\n    title = "{COMET} - Deploying a New State-of-the-art {MT} Evaluation Metric in Production",\n    author = "Stewart, Craig  and\n      Rei, Ricardo  and\n      Farinha, Catarina  and\n      Lavie, Alon",\n    booktitle = "Proceedings of the 14th Conference of the Association for Machine Translation in the Americas (Volume 2: User Track)",\n    month = oct,\n    year = "2020",\n    address = "Virtual",\n    publisher = "Association for Machine Translation in the Americas",\n    url = "https://www.aclweb.org/anthology/2020.amta-user.4",\n    pages = "78--109",\n}\n```\n',
    'author': 'Ricardo Rei, Craig Stewart, Catarina Farinha, Alon Lavie',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Unbabel/COMET',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
