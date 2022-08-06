# Kindergarten - Interactive Plotting GUI for Python Notebooks

Kindergarten is a UI on top of Plotly to visualize Pandas DataFrames.

Simply `pip install kindergarten`, and then do

```python
from kindergarten import plot
import pandas as pd

df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
plot()
```

in a Jupyter notebook to interactively visualize DataFrames. The library automatically finds all DataFrames
and populates all options with column names etc.

If you need a different number of traces, you can specify the number with `plot(num_traces=10)`.

# Examples

Plotting a single DataFrame:

![](demo1.gif)

Plotting several traces:

![](demo2.gif)


## Screenshots

![](screenshot1.png)

![](screenshot2.png)
