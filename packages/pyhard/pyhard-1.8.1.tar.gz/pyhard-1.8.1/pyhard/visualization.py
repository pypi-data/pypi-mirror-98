import io
import logging
from functools import reduce
from pathlib import Path

import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
from bokeh.models import HoverTool
from bokeh.themes.theme import Theme
from holoviews import opts, dim, streams
from pandas.api.types import is_integer_dtype, is_float_dtype
from shapely.geometry import Point, Polygon, MultiPolygon
from sklearn.decomposition import PCA

from pyhard.context import Workspace
from pyhard.utils import reduce_dim


dark_color = '#292929'
light_color = '#ffffff'
footprint_colors = {'good': '#58D68D', 'best': '#9B59B6'}

dark_theme = Theme(
    json={
        'attrs': {
            'Figure': {
                'background_fill_color': dark_color,
                'border_fill_color': dark_color,
                'outline_line_color': '#444444',
            },
            'Title': {
                'text_color': 'white',
                'text_font_size': '14pt'
            },
            'Grid': {
                'grid_line_dash': [6, 4],
                'grid_line_alpha': .3,
            },

            'Axis': {
                'major_label_text_color': 'white',
                'axis_label_text_color': 'white',
                'major_tick_line_color': 'white',
                'minor_tick_line_color': 'white',
                'axis_line_color': "white"
            },

            'ColorBar': {
                'background_fill_color': dark_color,
                'major_label_text_color': 'white',
                'title_text_color': 'white'
            },

            'Plot': {
                'sizing_mode': 'stretch_both',
                'margin': (0, 0, 0, 0)
            }
        }
    })

light_theme = Theme(
    json={
        'attrs': {
            'Figure': {
                'background_fill_color': light_color,
                'border_fill_color': light_color,
                'outline_line_color': '#444444',
            },
            'Title': {
                'text_color': 'black',
                'text_font_size': '14pt'
            },
            'Grid': {
                'grid_line_dash': [6, 4],
                'grid_line_alpha': .9,
            },

            'Axis': {
                'major_label_text_color': 'black',
                'axis_label_text_color': 'black',
                'major_tick_line_color': 'black',
                'minor_tick_line_color': 'black',
                'axis_line_color': 'black'
            },

            'ColorBar': {
                'background_fill_color': light_color,
                'major_label_text_color': 'black',
                'title_text_color': 'black'
            },

            'Plot': {
                'sizing_mode': 'stretch_both',
                'margin': (0, 0, 0, 0)
            }
        }
    })

dark_template = f"""
{{% extends base %}}

{{% block title %}}Instance Hardness dashboard{{% endblock %}}

{{% block preamble %}}
<style>
  @import url(https://fonts.googleapis.com/css?family=Noto+Sans);
  body {{
    font-family: 'Noto Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    color: #fff;
    background: {dark_color};
  }}
</style>
{{% endblock %}}
"""

light_template = f"""
{{% extends base %}}

{{% block title %}}Instance Hardness dashboard{{% endblock %}}

{{% block preamble %}}
<style>
  @import url(https://fonts.googleapis.com/css?family=Noto+Sans);
  body {{
    font-family: 'Noto Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    color: #000;
    background: {light_color};
  }}
</style>
{{% endblock %}}
"""

_my_path = Path(__file__).parent


class App:
    _tabs_id = ['Instance Space', 'Footprint performance', 'Selection explorer']
    _tabs_inner_id = ['Statistics', 'Features', 'Meta-features']

    def __init__(self, workspace: Workspace):
        hv.extension('bokeh')
        hv.renderer('bokeh').theme = light_theme

        self.logger = logging.getLogger(__name__)
        self.workspace = workspace

        df_dataset = workspace.data.copy()
        df_metadata = workspace.extended_metadata
        df_is = workspace.is_coordinates
        df_footprint = workspace.footprints

        if len(df_dataset.columns) > 3:
            X = df_dataset.iloc[:, :-1]
            y = df_dataset.iloc[:, -1]

            pca = PCA(n_components=2)
            X_embedded = pca.fit_transform(X)
            # tsne = TSNE(n_components=2)
            # X_embedded = tsne.fit_transform(X)

            df = pd.DataFrame(X_embedded, columns=[f'Component1',  # ({(100 * pca.explained_variance_ratio_[0]):.2f}%)
                                                   f'Component2'],  # ({(100 * pca.explained_variance_ratio_[1]):.2f}%)
                              index=X.index)
            df_dataset = pd.concat([df, y], axis=1)

        data = df_is.join(df_dataset)
        self.data = data.join(df_metadata)
        self.mlist = ['circle', 'triangle', 'square', 'diamond', 'asterisk', 'hex', '+', 'x']
        self.data_dims = df_dataset.columns.to_list()
        self.class_label = self.data_dims[2]
        self.meta_dims = df_metadata.columns.to_list()

        # Scatter kdims and vdims
        is_cols = df_is.columns.to_list()
        self.is_kdims = is_cols[0]
        self.is_vdims = [is_cols[1], self.class_label] + self.meta_dims
        self.data_kdims = self.data_dims[0]
        self.data_vdims = [self.data_dims[1], self.class_label] + self.meta_dims

        # Panel widgets
        self.w_color = pn.widgets.Select(options=self.meta_dims + [self.class_label], value=self.meta_dims[0])
        self.w_color_range = pn.widgets.RangeSlider(start=0, end=20, value=(0, 5), step=0.5)
        self.w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
        self.w_footprint_on = pn.widgets.Checkbox(name='draw footprint area', value=True)

        val = 'instance_hardness' if 'instance_hardness' in df_footprint.index else ''
        self.w_footprint_algo = pn.widgets.Select(options=df_footprint.index.unique(level='algo').to_list(), value=val)

        self.bbox = None
        self.cmap = 'coolwarm'
        self._page_tabs = pn.Tabs(*[(name, None) for name in self._tabs_id], dynamic=False)
        self._inner_tabs = pn.Tabs(*[(name, None) for name in self._tabs_inner_id], dynamic=True, tabs_location='left')
        self._page_tabs[2] = (self._tabs_id[2], self._inner_tabs)
        self.populate_tabs()

    @staticmethod
    @DeprecationWarning
    def footprint2polygons(footprint: np.ndarray):
        poly_list = np.split(footprint, np.argwhere(np.isnan(footprint).any(axis=1)).flatten())
        return MultiPolygon(list(map(lambda x: Polygon(x[~np.isnan(x).any(axis=1)]), poly_list)))

    @classmethod
    @DeprecationWarning
    def remove_intersection(cls, fp_good: np.ndarray, fp_bad: np.ndarray):
        p_good = MultiPolygon(cls.footprint2polygons(fp_good))
        p_bad = MultiPolygon(cls.footprint2polygons(fp_bad))
        p_diff_good = p_good.difference(p_bad)
        p_diff_bad = p_bad.difference(p_good)

        fp_good_clean = None
        if isinstance(p_diff_good, Polygon):
            x, y = p_diff_good.exterior.coords.xy
            fp_good_clean = np.array([x, y]).T
        else:
            for poly in p_diff_good:
                x, y = poly.exterior.coords.xy
                if fp_good_clean is None:
                    fp_good_clean = np.array([x, y]).T
                else:
                    new = np.append(np.array([[np.nan, np.nan]]), np.array([x, y]).T, axis=0)
                    fp_good_clean = np.append(fp_good_clean, new, axis=0)

        fp_bad_clean = None
        if isinstance(p_diff_bad, Polygon):
            x, y = p_diff_bad.exterior.coords.xy
            fp_bad_clean = np.array([x, y]).T
        else:
            for poly in p_diff_bad:
                x, y = poly.exterior.coords.xy
                if fp_bad_clean is None:
                    fp_bad_clean = np.array([x, y]).T
                else:
                    new = np.append(np.array([[np.nan, np.nan]]), np.array([x, y]).T, axis=0)
                    fp_bad_clean = np.append(fp_bad_clean, new, axis=0)

        return fp_good_clean, fp_bad_clean

    def footprint_area(self, algo):
        try:
            border_points_good = self.workspace.footprints.xs([algo, 'good']).values
        except KeyError:
            border_points_good = np.array([[0, 0]])
        try:
            border_points_best = self.workspace.footprints.xs([algo, 'best']).values
        except KeyError:
            border_points_best = np.array([[0, 0]])

        border_good, border_best = border_points_good, border_points_best

        footprint_good = hv.Polygons([border_good.tolist()], label='Good Footprint').opts(line_width=1, line_alpha=0.2,
                                                                                          line_color='black',
                                                                                          fill_color=footprint_colors[
                                                                                              'good'],
                                                                                          fill_alpha=.2,
                                                                                          show_legend=True)

        footprint_best = hv.Polygons([border_best.tolist()], label='Best Footprint').opts(line_width=1, line_alpha=0.2,
                                                                                          line_color='black',
                                                                                          fill_color=footprint_colors[
                                                                                              'best'],
                                                                                          fill_alpha=.2,
                                                                                          show_legend=True)
        return footprint_good * footprint_best

    def select_instances(self):
        if self.bbox is None:
            return pd.Series(False, index=self.data.index)
        x, y = list(self.bbox.keys())
        if len(self.bbox[x]) == 2:
            V1 = np.column_stack([self.bbox[x], self.bbox[y]])
            V2 = V1.copy()
            V2[0, 1], V2[1, 1] = V1[1, 1], V1[0, 1]
            V = np.array([V1[0, :], V2[0, :], V1[1, :], V2[1, :]])
            contour = list(map(tuple, V))
        else:
            contour = list(map(tuple, np.column_stack([self.bbox[x], self.bbox[y]])))
        polygon = Polygon(contour)
        mask = self.data[[x, y]].apply(lambda p: polygon.contains(Point(p[0], p[1])), raw=True, axis=1)
        return mask

    def data_space(self, c, lim, autorange_on):
        if not autorange_on:
            lim = (np.nan, np.nan)
        cmap = self.cmap
        # hover_list = [c] + hover_list
        # tooltips = [(s, '@' + s) for s in hover_list]
        # hover = HoverTool(tooltips=tooltips)
        scatter1 = hv.Scatter(self.data, kdims=self.data_kdims, vdims=self.data_vdims
                              ).opts(responsive=True, aspect=1.1, color=c,
                                     cmap=cmap, show_grid=True,
                                     marker=dim(self.class_label).categorize(self.mlist),
                                     tools=['lasso_select', 'box_select', 'hover'],
                                     size=7, framewise=True, colorbar=True, clim=lim)
        return scatter1

    def instance_space(self, c, lim, autorange_on):
        if not autorange_on:
            lim = (np.nan, np.nan)
        cmap = self.cmap
        # hover_list = [c] + hover_list
        # tooltips = [(s, '@' + s) for s in hover_list]
        # hover = HoverTool(tooltips=tooltips)
        scatter2 = hv.Scatter(self.data, kdims=self.is_kdims, vdims=self.is_vdims
                              ).opts(responsive=True, aspect=1.1, color=c,
                                     cmap=cmap, show_grid=True,
                                     marker=dim(self.class_label).categorize(self.mlist),
                                     tools=['lasso_select', 'box_select', 'hover'],
                                     size=7, framewise=True, colorbar=True, clim=lim)
        return scatter2

    def get_pane(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value)
        def update_plot1(color, lim, autorange_on):
            return self.data_space(color, lim, autorange_on)

        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value)
        def update_plot2(color, lim, autorange_on):
            return self.instance_space(color, lim, autorange_on)

        def selection_callback1(bbox, region_element, selection_expr, resetting):
            self.bbox = bbox
            if resetting:
                self.bbox = None
            self.populate_tabs()
            return hv.Polygons([[[0, 0]]])

        @pn.depends(footprint=self.w_footprint_algo.param.value, fp_on=self.w_footprint_on.param.value)
        def selection_callback2(bbox, region_element, selection_expr, footprint, fp_on):
            self.bbox = bbox

            self.populate_tabs()

            if fp_on:
                return self.footprint_area(footprint)
            else:
                return (hv.Polygons([[[0, 0]]], label='Good Footprint').opts(fill_color=footprint_colors['good']) *
                        hv.Polygons([[[0, 0]]], label='Best Footprint').opts(fill_color=footprint_colors['best']))
                # hv.Polygons([[[0, 0]]], label='Bad').opts(fill_color=footprint_colors['bad']) * \

        dmap1 = hv.DynamicMap(update_plot1)
        dmap2 = hv.DynamicMap(update_plot2)
        dmap1.opts(title='Principal Components')
        dmap2.opts(title='Instance Space')

        selection1 = hv.streams.SelectionExpr(source=dmap1)
        reset = hv.streams.PlotReset()
        sel1_dmap = hv.DynamicMap(selection_callback1, streams=[selection1, reset])

        selection2 = hv.streams.SelectionExpr(source=dmap2)
        sel2_dmap = hv.DynamicMap(selection_callback2, streams=[selection2])

        def file_cb():
            mask = self.select_instances()
            df = self.workspace.data[mask]
            sio = io.StringIO()
            df.to_csv(sio)
            sio.seek(0)
            return sio

        button = pn.widgets.FileDownload(embed=False, auto=True, callback=file_cb,
                                         filename='selection.csv',
                                         label='Save selected points',
                                         button_type='primary')

        layout = (dmap1 * sel1_dmap + dmap2 * sel2_dmap).cols(2).opts(
            opts.Layout(shared_axes=False, shared_datasource=True, framewise=True),
            opts.Polygons(show_legend=True, legend_position='bottom'))

        gspec = pn.GridSpec(sizing_mode='stretch_both', background=light_color, margin=0)
        gspec[0, 0] = pn.Column('## Color', self.w_color, '### Color Bar', self.w_checkbox, self.w_color_range,
                                pn.Row(pn.Spacer(), height=20),
                                '## Footprint', self.w_footprint_on, self.w_footprint_algo,
                                pn.Row(pn.Spacer(), height=20),
                                '## Selection', button,
                                background=light_color)
        gspec[0, 1:5] = layout
        self._page_tabs[0] = (self._tabs_id[0], gspec)
        self._page_tabs[1] = (self._tabs_id[1], pn.widgets.DataFrame(self.workspace.footprint_performance,
                                                                     name='Performance',
                                                                     disabled=True,
                                                                     sizing_mode='stretch_both'))
        tmpl = pn.Template(light_template)
        tmpl.add_panel(name='IS', panel=self._page_tabs)
        return tmpl

    def populate_tabs(self):
        mask = self.select_instances()
        df_selection = self.workspace.data[mask].copy()
        output_col = df_selection.columns[-1]
        df_selection.loc[:, output_col] = df_selection.iloc[:, -1].apply(lambda x: str(x))
        cols = df_selection.columns[:-1].to_list()

        # selection dataframe tab
        if not mask.any():
            df_table = self.workspace.data[~mask].copy()
            df_table[output_col] = df_table[output_col].apply(lambda x: str(x))
        else:
            df_table = df_selection
        desc_all = pn.widgets.DataFrame(df_table.describe(include='all'), name='Selection',
                                        disabled=True, sizing_mode='stretch_both')

        desc = df_table.groupby(output_col).describe(include='all').unstack(1)
        desc.index = desc.index.set_names(['Feature', 'Statistic'], level=[0, 1])
        desc = desc.reset_index(level=[0]).pivot(columns='Feature').reorder_levels([1, 0]).sort_index()
        desc.columns = desc.columns.droplevel(0)
        desc_class = pn.widgets.DataFrame(desc, name='Selection', disabled=True, sizing_mode='stretch_both',
                                          show_index=True, hierarchical=True)
        table = pn.Column(desc_all, "__Descriptive statistics by class__", desc_class, sizing_mode='stretch_width')

        self._inner_tabs[0] = (self._tabs_inner_id[0], table)

        # metadata selection tab
        df_feat = self.workspace.metadata[mask].filter(regex='^feature_').melt(var_name='feature')
        boxplot_feat = hv.BoxWhisker(df_feat, kdims='feature', vdims='value').opts(responsive=True,
                                                                                   aspect=3,
                                                                                   xrotation=45,
                                                                                   show_grid=True,
                                                                                   box_fill_color=dim('feature').str(),
                                                                                   cmap='glasbey_cool',
                                                                                   tools=['hover'])

        df_algo = self.workspace.metadata[mask].filter(regex='^algo_').melt(var_name='algorithm', value_name='logloss')
        boxplot_algo = hv.BoxWhisker(df_algo, kdims='algorithm', vdims='logloss').opts(responsive=True,
                                                                                       aspect=3,
                                                                                       xrotation=45,
                                                                                       show_grid=True,
                                                                                       box_fill_color=dim(
                                                                                           'algorithm').str(),
                                                                                       cmap='glasbey_cool',
                                                                                       tools=['hover'])

        self._inner_tabs[2] = (self._tabs_inner_id[2],
                               pn.Column('# Distribution of the meta-features', pn.Row(boxplot_feat),
                                         '# Distribution of the algorithms', pn.Row(boxplot_algo),
                                         sizing_mode='stretch_both'))

        integer_cols = [col for col in cols if is_integer_dtype(df_selection[col])]
        float_cols = [col for col in cols if is_float_dtype(df_selection[col])]

        w_var_box = pn.widgets.MultiSelect(name='Features', value=[], options=float_cols)
        w_var_hist = pn.widgets.Select(name='Feature', options=cols)
        w_var_bar = pn.widgets.Select(name='Feature', options=integer_cols)

        @pn.depends(feat_list=w_var_box.param.value)
        def make_box(feat_list):
            return hv.BoxWhisker(df_selection[feat_list + [output_col]].melt(id_vars=output_col, var_name='feature'),
                                 kdims=['feature', output_col],
                                 vdims='value').opts(responsive=True,
                                                     aspect=2.5,
                                                     xrotation=45,
                                                     show_grid=True,
                                                     box_fill_color=dim(output_col).str(),
                                                     box_cmap='Set1',
                                                     tools=['hover'],
                                                     fontscale=1.2)

        @pn.depends(var=w_var_bar.param.value)
        def make_bar(var):
            if var is None:
                bar = hv.Bars([])
            else:
                kdims = [var, output_col]
                s = df_selection[kdims].value_counts()
                s.name = 'Count'
                s = s.to_frame()
                bar = hv.Bars(s)
            tooltips = [(output_col, f'@{output_col}'), ('Count', '@Count')]
            bar.opts(responsive=True,
                     aspect=2.5,
                     multi_level=True,
                     stacked=False,
                     show_grid=True,
                     fontscale=1.2,
                     tools=[HoverTool(tooltips=tooltips)])
            return bar

        @pn.depends(var=w_var_hist.param.value)
        def make_hist(var):
            classes = df_selection.iloc[:, -1].unique()
            hist = [hv.Histogram(np.histogram(df_selection[df_selection[output_col] == c][var]), label=str(c))
                    for c in classes]
            if len(hist) == 0:
                hist = hv.Histogram([])
            else:
                hist = reduce(lambda h1, h2: h1 * h2, hist)
            hist.opts('Histogram',
                      responsive=True,
                      aspect=2.5,
                      alpha=0.8,
                      show_grid=True,
                      muted_fill_alpha=0.1,
                      framewise=True,
                      tools=['hover'],
                      cmap='Set1',
                      fontscale=1.2,
                      xlabel=var)
            return hist

        dmap_box = hv.DynamicMap(make_box)
        dmap_box.opts(framewise=True)

        dmap_hist = hv.DynamicMap(make_hist)
        dmap_hist.opts(framewise=True)

        dmap_bar = hv.DynamicMap(make_bar)
        dmap_bar.opts(framewise=True)

        accordion = pn.Accordion(('Boxplot', pn.Row(w_var_box, dmap_box, sizing_mode='stretch_both')),
                                 ('Histogram', pn.Row(w_var_hist, dmap_hist, sizing_mode='stretch_both')),
                                 ('Barplot', pn.Row(w_var_bar, dmap_bar, sizing_mode='stretch_both')),
                                 sizing_mode='stretch_both')

        self._inner_tabs[1] = (self._tabs_inner_id[1], accordion)

    def show(self, port=5001, **kwargs):
        tmpl = self.get_pane()
        pn.serve(tmpl, port=port, show=True, title='Instance Hardness',
                 websocket_origin=[f'127.0.0.1:{port}', f'localhost:{port}'])


class Demo:
    def __init__(self, datadir=None):
        hv.extension('bokeh', logo=False)

        if datadir is None:
            self.datadir = _my_path / 'data'
        else:
            self.datadir = Path(datadir)

        self.list_dir = [x.name for x in self.datadir.glob('**/*') if x.is_dir()]
        self.list_dir.sort()

        self.w_dir = pn.widgets.Select(options=self.list_dir, value='overlap')
        self.w_color = pn.widgets.Select(options=[], value='')
        self.w_color_range = pn.widgets.IntRangeSlider(start=-40, end=40, value=(-20, 20), step=1)
        self.w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
        self.w_selector_hover = pn.widgets.MultiChoice(value=[], options=[])
        self.w_dim = pn.widgets.RadioButtonGroup(options=['LDA', 'NCA', 'PCA'], value='LDA', button_type='default')

        self.mlist = ['circle', 'triangle', 'square', 'diamond', '+', 'x']
        self.df_data = self.df_metadata = self.df_feat_proc = self.df_is = None
        self.is_kdims = self.data_dims = self.data_kdims = self.class_label = self.meta_dims = []
        self.folder = None

        self.load_data(self.w_dir.value)
        self.update_components()

    def load_data(self, path, dim_method='LDA'):
        if path != self.folder:
            self.folder = path
            path = self.datadir / path
            dataset = pd.read_csv(path / 'data.csv')

            if len(dataset.columns) > 3:
                X = dataset.iloc[:, :-1]
                y = dataset.iloc[:, -1]
                X_embedded = reduce_dim(X, y, method=dim_method)
                df = pd.DataFrame(X_embedded, columns=['V1', 'V2'], index=X.index)
                dataset = pd.concat([df, y], axis=1)

            self.df_metadata = pd.read_csv(path / 'metadata.csv', index_col='instances')
            self.df_is = pd.read_csv(path / 'coordinates.csv', index_col='Row')
            self.df_is.index.name = 'instances'

            dataset.index = self.df_metadata.index
            self.df_data = self.df_is.join(dataset)
            self.df_data = self.df_data.join(self.df_metadata)

            # TODO: organizar kdims e vdims
            self.is_kdims = self.df_is.columns.to_list()[0:2]
            self.data_dims = dataset.columns.to_list()
            self.data_kdims = self.data_dims[0:2]
            self.class_label = self.data_dims[2]
            self.meta_dims = self.df_metadata.columns.to_list()

    def get_ranges(self):
        r = list()
        a = 1.1
        r.append((self.df_data[self.data_kdims[0]].min() * a, self.df_data[self.data_kdims[0]].max() * a))
        r.append((self.df_data[self.data_kdims[1]].min() * a, self.df_data[self.data_kdims[1]].max() * a))
        r.append((self.df_data[self.is_kdims[0]].min() * a, self.df_data[self.is_kdims[0]].max() * a))
        r.append((self.df_data[self.is_kdims[1]].min() * a, self.df_data[self.is_kdims[1]].max() * a))
        return r

    def plotter(self, c, lim, autorange_on, hover_list, **kwargs):
        if not autorange_on:
            lim = (np.nan, np.nan)
        # cmap = 'RdYlBu_r'
        # if c == self.class_label:
        #     cmap = 'Set1'
        # else:
        #     cmap = 'jet'
        cmap = 'coolwarm'

        hover_list = [c] + hover_list if c not in hover_list else hover_list
        tooltips = [('index', '$index')] + [(s, '@' + s) for s in hover_list]
        hover = HoverTool(tooltips=tooltips)

        r = self.get_ranges()

        scatter1_vdims = [self.data_kdims[1], self.class_label] + self.meta_dims + self.is_kdims
        scatter1 = hv.Scatter(self.df_data, kdims=self.data_kdims[0], vdims=scatter1_vdims,
                              label='Original Data').opts(color=c,  # width=490, height=440
                                                          cmap=cmap, show_grid=True,
                                                          marker=dim(self.class_label).categorize(self.mlist),
                                                          xlim=r[0], ylim=r[1], responsive=True, aspect=1.2)

        scatter2_vdims = [self.is_kdims[1], self.class_label] + self.meta_dims + self.data_kdims
        scatter2 = hv.Scatter(self.df_data, kdims=self.is_kdims[0], vdims=scatter2_vdims,
                              label='Instance Space').opts(color=c,
                                                           cmap=cmap, show_grid=True,
                                                           marker=dim(self.class_label).categorize(self.mlist),
                                                           xlim=r[2], ylim=r[3], responsive=True, aspect=1.2)

        # dlink = DataLink(scatter1, scatter2)

        return (scatter1 + scatter2).opts(opts.Scatter(tools=['box_select', 'lasso_select', 'tap', hover],
                                                       size=6, colorbar=True, clim=lim, framewise=True),
                                          opts.Layout(shared_axes=False, shared_datasource=True)).cols(2)

    def update_components(self):
        self.w_color.options = self.meta_dims + [self.class_label]
        self.w_selector_hover.options = self.df_data.columns.to_list()
        self.w_selector_hover.value = self.data_dims + self.is_kdims

    def display(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value, hover_list=self.w_selector_hover.param.value,
                    folder=self.w_dir.param.value, method=self.w_dim.param.value)
        def update_plot(color, lim, autorange_on, hover_list, folder, method, **kwargs):
            self.load_data(folder, method)
            self.update_components()
            return self.plotter(color, lim, autorange_on, hover_list)

        dmap = hv.DynamicMap(update_plot)

        # row = pn.Row(pn.Column(pn.WidgetBox('## Dataset', self.w_dir,
        #                                     '### Dimensionality Reduction', self.w_dim,
        #                                     width=250, ), # height=200
        #                        pn.WidgetBox('## Color', self.w_color,
        #                                     '### Color Bar', self.w_checkbox, self.w_color_range,
        #                                     width=250, ),
        #                        ), dmap, sizing_mode='stretch_width')  # pn.layout.HSpacer()
        # pane = pn.Column(row, '## Hover Info', self.w_selector_hover, sizing_mode='stretch_width', height=200)

        md_color = '<span style="color:#292929">{0}</span>'
        # blue #1A76FF

        gspec = pn.GridSpec(sizing_mode='stretch_both')
        # gspec[0, 0:5] = pn.pane.Markdown('# Instance Hardness dashboard demo', style={'color': '#1A76FF'})
        # gspec[0, 4] = pn.pane.JPG(str(_my_path.parent / 'docs/img/ita_rgb.jpg'), width=100)
        gspec[0:3, 0] = pn.WidgetBox('## Dataset', self.w_dir,
                                     '### Dimensionality Reduction', self.w_dim,
                                     pn.Row(pn.Spacer(), height=20))
        gspec[3:7, 0] = pn.WidgetBox('## Color', self.w_color,
                                     '### Color Bar', self.w_checkbox,
                                     self.w_color_range,
                                     pn.Row(pn.Spacer(), height=20))
        gspec[0:7, 1:5] = dmap

        return gspec  # pane

    def display_notebook(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value, hover_list=self.w_selector_hover.param.value,
                    folder=self.w_dir.param.value, method=self.w_dim.param.value)
        def update_plot(color, lim, autorange_on, hover_list, folder, method, **kwargs):
            self.load_data(folder, method)
            self.update_components()
            return self.plotter(color, lim, autorange_on, hover_list)

        dmap = hv.DynamicMap(update_plot)

        gspec = pn.GridSpec(sizing_mode='stretch_both', max_height=800)
        gspec[0, 0:2] = pn.WidgetBox('## Dataset', self.w_dir,
                                     '### Dimensionality Reduction', self.w_dim)
        gspec[0, 2:] = pn.WidgetBox('## Color', self.w_color,
                                    '### Color Bar', self.w_checkbox, self.w_color_range)
        gspec[1:4, :4] = dmap

        return gspec


if __name__ == "__main__":
    demo = Demo()
    fig = demo.display()
    # fig.servable()
    # fig.show(port=5006, allow_websocket_origin=["localhost:5000"])
    pn.serve(fig.get_root(), port=5006, websocket_origin=["localhost:5000", "127.0.0.1:5000"], show=False)
