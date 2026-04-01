from pathlib import Path

import matplotlib.pyplot as plt
import panel as pn

from foodapi import FOODAPI as f
import plots as pl

pn.extension('plotly')

_ROOT = Path(__file__).resolve().parent

# Initialize the food api (CSV next to this script)
api = f()
api.load_food(str(_ROOT / 'indian_food.csv'))

# WIDGET DECLARATIONS

# Sankey diagram widgets
sankey_source = pn.widgets.Select(
    name="Source Column",
    options=api.get_available_filters(),
    value='course'
)

sankey_target = pn.widgets.Select(
    name="Target Column",
    options=api.get_available_filters(),
    value='diet'
)

sankey_threshold = pn.widgets.IntSlider(
    name="Min Count Threshold",
    start=0,
    end=20,
    step=1,
    value=0
)

# Venn diagram widgets
food_select = pn.widgets.MultiChoice(
    name="Food",
    options=api.get_foods(),
    value=['balu shahi','boondi','gajar ka halwa'],
    max_items=3
    )

# Scatter plot widgets
x_axis = pn.widgets.Select(
    name='X-Axis',
    options=['flavor_profile', 'course', 'prep_time', 'cook_time','region'], 
    value='cook_time')

y_axis = pn.widgets.Select(
    name='Y-Axis',
    options=['flavor_profile', 'course', 'prep_time', 'cook_time','region'],
    value='prep_time')

color_by = pn.widgets.Select(
    name='Color By', 
    options = api.get_available_filters(), 
    value='region')

prep_time_range = pn.widgets.RangeSlider(
    name='Preparation Time (min)',
    start=0, end=120, value=(15, 120), step=5)


# Plotting widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=750)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=400)

# CALLBACK FUNCTIONS
def get_venn(foods, width, height):
    '''Creates a venn diagram of three foods and their ingredients'''
    
    ingredient_dict = api.get_food_ingredients(foods)
    venn = pl.get_venn(ingredient_dict, width=width, height=height)
    plt.close('all')
    return pn.pane.Matplotlib(venn)

def get_scatter_plot(x_col, y_col, color_col, prep_range, width, height):
    '''Creates an interactive scatter plot of two variables,
      excluding the name and state variables'''
    
    scatter = pl.get_scatter(api.get_frame(),
                           x_col, y_col, color_col, prep_range,
                           width=width, height=height) 
    return pn.pane.Plotly(scatter)

def get_heatmap_plot(x_col, y_col, threshold, width, height):
    '''Creates a heatmap of two categorical variables'''

    heatmap = pl.get_heatmap(api.get_frame(), x_col, y_col, threshold=threshold,
                              width=width, height=height)
    return pn.pane.Plotly(heatmap)

def get_sankey_plot(source, target, threshold, width, height):
    '''Creates a sankey diagram of two categorical variables'''

    flow_df = api.get_flows(source_col=source, target_col=target, min_count=threshold)
    sankey = pl.make_sankey(flow_df, 'source', 'target', vals='count', width=width, height=height)
    return pn.pane.Plotly(sankey)

# CALLBACK BINDINGS
venn = pn.bind(get_venn, food_select, width, height)
scatter = pn.bind(get_scatter_plot, x_axis, y_axis, color_by, prep_time_range, width, height)
heatmap = pn.bind(get_heatmap_plot, sankey_target, sankey_source, sankey_threshold, width, height)
sankey = pn.bind(get_sankey_plot, sankey_source, sankey_target, sankey_threshold, width, height)

# DASHBOARD WIDGET CONTAINERS ("CARDS")
card_width = 320

venn_card = pn.Card(
    pn.Column(
        food_select
    ),
    title="Venn Selections", width=card_width, collapsed=True
)

category_card = pn.Card(
    pn.Column(
        sankey_source,
        sankey_target,
        sankey_threshold
    ),
    title="Sankey/Heatmap Controls", width=card_width, collapsed=True
)

scatter_card = pn.Card(
    pn.Column(
        x_axis,
        y_axis,
        color_by,
        prep_time_range
    ),
    title="Scatter Plot Controls", width=card_width, collapsed=True
)

plot_card = pn.Card(
    pn.Column(
        width,
        height
    ),
    title="Plot Size", width=card_width, collapsed=False
)

# LAYOUT
layout = pn.template.EditableTemplate(
    title="Indian Food Explorer",
    sidebar=[
        venn_card,
        scatter_card,
        category_card,
        plot_card,
    ],
    main=[
        pn.Tabs(
            ('Ingredients in Common', venn),
            ('Scatter Analysis', scatter),
            ('Category Heatmap', heatmap),
            ('Sankeys', sankey)
        )
    ],
    header_background='#587b7f',
).servable()
