import time
import pandas as pd
import plotly.offline as offline
from plotly.subplots import make_subplots
import plotly.graph_objs as graph_obj
from stock_data_frame_generater import StockDataFrameGenerater


class StockGraphGenerater:

    __export_path = './export/graph/{filename}.html'

    @classmethod
    def generate_graph(cls, summary, data_frame):
        start = time.time()

        # Get empty date
        date_all = pd.date_range(start=data_frame['date'].iloc[0], end=data_frame['date'].iloc[-1])
        date_obs = [d.strftime('%Y-%m-%d') for d in data_frame['date']]
        date_breaks = [d for d in date_all.strftime('%Y-%m-%d').tolist() if not d in date_obs]

        # 1, 2 = Daily graph
        # 3    = Volume graph 
        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            specs=[[{"rowspan": 2}],
                   [None],
                   [{}]])

        fig.add_trace(graph_obj.Candlestick(
            x=data_frame.date,
            open=data_frame.open,
            high=data_frame.high,
            low=data_frame.low,
            close=data_frame.close,

            increasing_line_color='red',
            decreasing_line_color='blue',
            # y=data_frame.close,
            name='일봉'),
            row=1, col=1)

        for column_name in StockDataFrameGenerater.get_ma_column_names():
            fig.add_trace(graph_obj.Scatter(
                x=data_frame.date,
                y=data_frame[column_name],
                name=column_name),
                row=1, col=1)

        fig.add_trace(graph_obj.Bar(x=data_frame.date,
                                    y=data_frame.volume,
                                    name='거래량'),
                      row=3, col=1)

        # Title
        fig.update_layout(title='{name} - {score}'.format(name=summary.name, score=summary.trend_score))

        # Disable range slider
        fig.update_xaxes(rangeslider_visible=False)

        # Hide empty dates
        fig.update_xaxes(rangebreaks=[dict(values=date_breaks)])

        # cls.show_graph(fig)
        cls.save_graph(summary, fig)

        log = 'StockGraphGenerater.generate_graph({name})'.format(name = summary.name)
        print(log, round(time.time() - start, 4))


    @classmethod
    def save_graph(cls, summary, fig):

        path_name = cls.__export_path.format(filename=summary.name)

        offline.plot(
            fig,
            auto_open=False,
            filename=path_name)

    @classmethod
    def show_graph(cls, fig):
        fig.show()
