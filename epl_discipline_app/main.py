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
    redsize=discipline['total_red'].apply(lambda x: x+5),
    position=discipline['position_mapped']
))

color_map = factor_cmap('position', palette=Category10[4], factors=discipline['position_mapped'].unique())

TOOLTIPS = [
    ("player", "@desc"),
    ('yellows', '@yellows'),
    ('reds', '@reds')
]
# fit line for all players
x=np.array(discipline['mins_played'])
y=np.array(discipline['total_yellow'])

# Make and fit a linear regression model
model = LinearRegression().fit(x.reshape(-1, 1), y)
# x values need to be in a two-dimensional array, so use .reshape(-1, 1)

# Find the slope and intercept from the model
slope = model.coef_[0] # Takes the first element of the array
intercept = model.intercept_

# Make the regression line
regression_line = Slope(gradient=slope, y_intercept=intercept, line_color="black", line_dash='dashed')

# fit line for goalkeepers

xg=np.array(discipline.loc[discipline['position_mapped'] == 'goalkeeper', 'mins_played'])
yg=np.array(discipline.loc[discipline['position_mapped'] == 'goalkeeper', 'total_yellow'])
modelg = LinearRegression().fit(xg.reshape(-1, 1), yg)
slopeg = modelg.coef_[0]
interceptg = modelg.intercept_
regression_lineg = Slope(gradient=slopeg, y_intercept=interceptg, line_color=Category10[4][3])

# fit line for defenders

xd=np.array(discipline.loc[discipline['position_mapped'] == 'defender', 'mins_played'])
yd=np.array(discipline.loc[discipline['position_mapped'] == 'defender', 'total_yellow'])
modeld = LinearRegression().fit(xd.reshape(-1, 1), yd)
sloped = modeld.coef_[0]
interceptd = modeld.intercept_
regression_lined = Slope(gradient=sloped, y_intercept=interceptd, line_color=Category10[4][0])

# fit line for midfielders

xm=np.array(discipline.loc[discipline['position_mapped'] == 'midfielder', 'mins_played'])
ym=np.array(discipline.loc[discipline['position_mapped'] == 'midfielder', 'total_yellow'])
modelm = LinearRegression().fit(xm.reshape(-1, 1), ym)
slopem = modelm.coef_[0]
interceptm = modelm.intercept_
regression_linem = Slope(gradient=slopem, y_intercept=interceptm, line_color=Category10[4][1])

# fit line for attackers

xa=np.array(discipline.loc[discipline['position_mapped'] == 'attacker', 'mins_played'])
ya=np.array(discipline.loc[discipline['position_mapped'] == 'attacker', 'total_yellow'])
modela = LinearRegression().fit(xa.reshape(-1, 1), ya)
slopea = modela.coef_[0]
intercepta = modela.intercept_
regression_linea = Slope(gradient=slopea, y_intercept=intercepta, line_color=Category10[4][2])

p = figure(plot_width=800, plot_height=400, tooltips=TOOLTIPS,
           title="EPL Discipline", x_axis_label="Minutes played", y_axis_label="Yellow cards")

p.circle('x', 'y', size='redsize', fill_alpha=0.5, source=source, line_color='white', fill_color=color_map, legend_field='position')
p.legend.location = "top_left"
p.add_layout(regression_line)
p.add_layout(regression_lineg)
p.add_layout(regression_lined)
p.add_layout(regression_linem)
p.add_layout(regression_linea)

curdoc().add_root(p)
curdoc().title = "EPL Discipline"

# to do
# - convert regression lines to p.line() to add legend and interativity funcitonality
# - add table
# - add multiselect checkboxes
# - add some sort of watermark
# - add text search
