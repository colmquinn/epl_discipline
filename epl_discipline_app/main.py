from os.path import join, dirname
import pandas as pd
from bokeh.plotting import ColumnDataSource, figure, curdoc
import numpy as np
from sklearn.linear_model import LinearRegression
from bokeh.models import Slope
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap

discipline = pd.read_csv(join(dirname(__file__), 'data/epl_discipline.csv'))

source = ColumnDataSource(data=dict(
    x=discipline['mins_played'],
    y=discipline['total_yellow'],
    desc=discipline['player_name'],
    yellows=discipline['total_yellow'],
    reds=discipline['total_red'],
    redsize=discipline['redsize'],
    position=discipline['position_mapped']
))

color_map = factor_cmap('position', palette=Category10[4], factors=discipline['position_mapped'].unique())

TOOLTIPS = [
    ("player", "@desc"),
    ('yellows', '@yellows'),
    ('reds', '@reds')
]

x=np.array(discipline['mins_played'])
y=np.array(discipline['total_yellow'])

# Make and fit a linear regression model
model = LinearRegression().fit(x.reshape(-1, 1), y)
# x values need to be in a two-dimensional array, so use .reshape(-1, 1)

# Find the slope and intercept from the model
slope = model.coef_[0] # Takes the first element of the array
intercept = model.intercept_

# Make the regression line
regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="red")

p = figure(plot_width=800, plot_height=400, tooltips=TOOLTIPS,
           title="EPL Discipline", x_axis_label="Minutes played", y_axis_label="Yellow cards")

p.circle('x', 'y', size='redsize', fill_alpha=0.5, source=source, line_color='white', fill_color=color_map, legend_field='position')
p.add_layout(regression_line)
curdoc().add_root(p)
curdoc().title = "EPL Discipline"