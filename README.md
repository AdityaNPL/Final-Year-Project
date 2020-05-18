### GWO-EA Runing Instructions

#### Run EA optimiser

```bash
python ./runEASim.py
```

#### Run one GWO-EA instance

```bash
python ./runOneSim.py
```


### VA Testing Instructions

```bash
python ./Tester/runtests.py
```

### Troubleshooting Errors:

Usually they will be packages not installed, a quick fix may be to use pip installer

```bash
pip install <package to be installed>
```

Implementation uses the following references:
#### GWO Method
S. Mirjalili, S.M. Mirjalili, and A. Lewis. “Grey Wolf Optimizer”. In: Advances in Engineering Software. Vol. 69. 2014, pp. 46–61. doi: https : / / doi . org / 10 . 1016 / j .
advengsoft.2013.12.007. url: http://www.sciencedirect.com/science/article/
pii/S0965997813001853.
#### RotorS simulation framework
Fadri Furrer et al. “RotorS – A Modular Gazebo MAV Simulator Framework”. In: vol. 625.
Jan. 2016, pp. 595–625. isbn: 978-3-319-26054-9. doi: 10.1007/978-3-319-26054-9_23
