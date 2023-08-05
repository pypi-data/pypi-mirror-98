# Hemlock Big 5

Hemlock-big5 is a <a href="https://dsbowen.github.io/hemlock/" target="_blank">hemlock</a> extension for creating big 5 personality questionnaires.

## Installation

With hemlock-CLI (recommended):

```
$ hlk install hemlock-big5
```

With pip:

```
$ pip install hemlock-big5
```

## Quickstart

This assumes you are using the hemlock template. In `survey.py`:

```python
from hemlock import Branch, Page, Label, route
from hemlock_big5 import big5

@route('/survey')
def start():
    return Branch(
        big5(page=True),
        Page(
            Label('The end.'), 
            terminal=True
        )
    )
```

## Citation

Hemlock-big5 includes several versions of big 5 personality questionnaires. Please cite the appropriate questionnaire along with hemlock.

### Hemlock-big5

```
@software{bowen2021hemlock-big5,
  author = {Dillon Bowen},
  title = {Hemlock-Big5},
  url = {https://dsbowen.github.io/hemlock-big5/},
  date = {2021-02-17},
}
```

### IPIP 50-item inventory (IPIP-50)

```
@article{donnellan2006mini,
  title={The mini-IPIP scales: tiny-yet-effective measures of the Big Five factors of personality.},
  author={Donnellan, M Brent and Oswald, Frederick L and Baird, Brendan M and Lucas, Richard E},
  journal={Psychological assessment},
  volume={18},
  number={2},
  pages={192},
  year={2006},
  publisher={American Psychological Association}
}
```

### Ten-item personality inventory (TIPI)

```
@article{gosling2003very,
  title={A very brief measure of the Big-Five personality domains},
  author={Gosling, Samuel D and Rentfrow, Peter J and Swann Jr, William B},
  journal={Journal of Research in personality},
  volume={37},
  number={6},
  pages={504--528},
  year={2003},
  publisher={Elsevier}
}
```

### Ten-item big five inventory (BFI-10)

```
@article{rammstedt2007measuring,
  title={Measuring personality in one minute or less: A 10-item short version of the Big Five Inventory in English and German},
  author={Rammstedt, Beatrice and John, Oliver P},
  journal={Journal of research in Personality},
  volume={41},
  number={1},
  pages={203--212},
  year={2007},
  publisher={Elsevier}
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/hemlock-big5/blob/master/LICENSE).