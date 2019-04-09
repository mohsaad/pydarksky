# PyCsk

## Clear Sky Charts in your terminal

![ClearSkyChat](https://i.imgur.com/DAZFlAC.png)

This is a program to pull stargazing conditions from [Clear Sky Charts](http://www.cleardarksky.com/csk/).

The colors will change according to when is the best stargazing forecast. For example, red will indicate that conditions are not great for that particular day, while green indicates that it will be a good day. For more information on which each sections means, see [here](http://www.cleardarksky.com/c/BdmIDkey.html?1#how).

### Requirements:

`python3` (>= 3.6)

`appdirs` (>= 1.4.3)

`sty` (>= 1.0.0b9)


### Installation

`$ pip3 install pycsk`

### Usage

`$ csk`

To search for cities by states:

`$ csk --search-by-state`

To search for a specific city:

`$ csk --search-by-city`
