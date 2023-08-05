# Hemlock-Berlin

Hemlock-Berlin is a <a href="https://dsbowen.github.io/hemlock" target="_blank">hemlock</a> extension which allows you to add a <a href="http://www.riskliteracy.org/" target="_blank"> Berlin numeracy test</a> to hemlock projects.

## Installation

With the hemlock-CLI (recommended):

```bash
$ hlk install hemlock-berlin
```

With pip:

```
$ pip install hemlock-berlin
```

## Quickstart

This example shows how to add an adaptive Berlin numeracy test to your hemlock survey and display the participant's score to him/her.

In `survey.py`:

```python
from flask_login import current_user
from hemlock import Branch, Page, Label, route
from hemlock_berlin import berlin

@route('/survey')
def start():
    return Branch(
        berlin(),
        Page(
            Label(compile=display_score), 
            terminal=True
        )
    )

def display_score(label):
    label.label = '<p>Berlin score: {}</p>'.format(
        current_user.g['BerlinScore']
    )
```

`app.py` is standard from the hemlock template.

Run the app with the hemlock command line interface:

```bash
hlk serve
```

or with python:

```bash
python app.py
```

## Citation

```
@software{bowen2020hemlock-berlin,
  author = {Dillon Bowen},
  title = {Hemlock-Berlin},
  url = {https://dsbowen.github.io/hemlock-berlin/},
  date = {2020-10-05},
}

@article{cokely2012measuring,
  title={Measuring risk literacy: The Berlin numeracy test.},
  author={Cokely, Edward T and Galesic, Mirta and Schulz, Eric and Ghazal, Saima and Garcia-Retamero, Rocio},
  journal={Judgment and Decision making},
  year={2012},
  publisher={Society for Judgment and Decision Making}
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/hemlock-berlin/blob/master/LICENSE).