from Controller.stockdatacontroller import StockDataController
from Controller.stockcontroller import StockController
from Controller.portfoliostockcontroller import PortfolioStockController
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px


sc = StockController()
sdc = StockDataController()
psc = PortfolioStockController()
"""
# newlist = [expression for item in iterable if condition == True]

historic_price = [{"date": str(stockdata.date), "price":float(stockdata.close_price)}for stockdata in sd.get_all_stock_data_from_stock_id(sc.get_stock_by_ticker_symbol("GOOGL").stock_id)]

df = pd.DataFrame(historic_price)
df = df.sort_values(by="date", ignore_index=True)

data = [go.Scatter(
    x=df["date"],
    y=df["price"],
    mode="lines",
    name="Historical Data"
)]

layout = go.Layout(title="Historical Data")
fig = go.Figure(data=data, layout=layout)

pyo.plot(fig)"""

#print(df)

def generate_portfolio_info(portfolio_id):
    portfolio_stocks = psc.get_all_portfolio_stocks_from_portfolio_id(portfolio_id)
    stock_ids = [portfolio_stock.stock_id for portfolio_stock in portfolio_stocks]
    stock_infos = []
    for stock_id in stock_ids:
        stock_info = {"name": sc.get_stock(stock_id).company_name,
                      "ticker": sc.get_stock(stock_id).ticker_symbol,
                      "no-stocks": psc.get_portfolio_stock_by_portfolio_id_and_stock_id(portfolio_id, stock_id).quantity,
                      "current-value": float(sdc.get_latest_stock_data_by_stock_id(stock_id).close_price),
                      "sector": sc.get_stock(stock_id).sector,
                      "industry": sc.get_stock(stock_id).industry,
                      "historical-data": generate_historical_stock_data(stock_id)
                      }
        stock_infos.append(stock_info)

    return stock_infos


def generate_historical_stock_data(stock_id):
    historic_price = [{"date": str(stockdata.date), "price": float(stockdata.close_price)} for stockdata in
                      sdc.get_all_stock_data_from_stock_id(stock_id)]

    df = pd.DataFrame(historic_price)
    df = df.sort_values(by="date", ignore_index=True)

    return df



def pie_chart_plotter(stock_infos):
    pie_info = []
    for stock in stock_infos:
        info = {"name": stock["name"], "value": stock["no-stocks"]*stock["current-value"]}
        pie_info.append(info)
    pie_info = pd.DataFrame(pie_info)
    fig = go.Figure(data=[go.Pie(labels=pie_info["name"], values=pie_info["value"])])
    return fig

def line_graph_plotter(stock_infos, date_before="2020-01-01", date_after="2025-01-01"):
    sets = []
    dataframes = []
    for stock_info in stock_infos:
        data = stock_info["historical-data"]
        data = data[data["date"] >= date_before]
        data = data[data["date"] < date_after]
        trace = go.Scatter(
                x=data["date"],
                y=data["price"],
                mode="lines",
                name=f"{stock_info['name']}",
                stackgroup="one"
        )
        sets.append(trace)
        dataframes.append(data)
    combined_df = pd.concat(dataframes)
    combined_df = combined_df.groupby("date", as_index=False)["price"].sum()

    combined_trace = go.Scatter(
        x=combined_df["date"],
        y=combined_df["price"],
        mode="lines",
        name="Portfolio Value"
    )
    sets.append(combined_trace)
    fig = go.Figure(data=sets)
    return fig


def table_generator(stock_info_list):
    names = [stock["name"] for stock in stock_info_list]
    no_stocks = [stock["no-stocks"] for stock in stock_info_list]
    current_values = [stock["current-value"] for stock in stock_info_list]
    total_values = [stock["no-stocks"] * stock["current-value"] for stock in stock_info_list]
    sectors = [stock["sector"] for stock in stock_info_list]
    industries = [stock["industry"] for stock in stock_info_list]
    data = go.Table(
        header=dict(
            values=["Name", "No. Stocks", "Current Value", "Total Value", "Sector", "Industry"],
            fill_color="lightgray",
            align="left"
        ),
        cells=dict(
            values=[names, no_stocks, current_values, total_values, sectors, industries],
            align="left"
        )
    )
    fig = go.Figure(data=data)
    return fig.show()




def render_remove_stock_section(portfolio_id):
    portfolio_stocks = psc.get_all_portfolio_stocks_from_portfolio_id(portfolio_id)
    stocks = [sc.get_stock(portfolio_stock.stock_id) for portfolio_stock in portfolio_stocks]
    portfolio_stocks_names = {}
    for portfolio_stock in portfolio_stocks:
        for stock in stocks:
            if portfolio_stock.stock_id == stock.stock_id:
                portfolio_stocks_names[stock.company_name] = portfolio_stock.portfolio_stock_id

    return portfolio_stocks_names

print(render_remove_stock_section(1)[0])


"""
fig = go.Figure(data=[go.Table(
    header=dict(values=['A Scores', 'B Scores'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[[100, 90, 80, 90], # 1st column
                       [95, 85, 75, 95]], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

"""