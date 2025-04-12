import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
from Controller.portfoliocontroller import PortfolioController
from Controller.stockcontroller import StockController
from Controller.portfoliostockcontroller import PortfolioStockController
from Controller.stockdatacontroller import StockDataController
import pandas as pd

user_id = 1

pc = PortfolioController()
sdc = StockDataController()
psc = PortfolioStockController()
sc = StockController()
portfolios = pc.get_portfolios_by_user_id(user_id)
portfolio_options = [{"label": p.portfolio_name, "value": p.portfolio_id} for p in portfolios]

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout
app.layout = html.Div([
    # Top Row: Portfolio Selection and Buttons
    html.Nav([
        dcc.Dropdown(
            id='portfolio-selector',
            placeholder='Select a Portfolio',
            options=portfolio_options,
            style={'width': '60%', 'display': 'inline-block'}
        ),
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed="2020-01-01",
            max_date_allowed="2025-01-01",
            initial_visible_month="2020-01-01",
            end_date="2025-01-01"
        ),
        html.Button('Refresh Portfolios', id='refresh-portfolios-btn', n_clicks=0, style={'margin-left': '10px'}),
        html.Button('Create Portfolio', id='create-portfolio-btn', n_clicks=0, style={'margin-left': '10px'}),
        html.Button('Modify Portfolio', id='modify-portfolio-btn', n_clicks=0, style={'margin-left': '10px'})
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'}),

    # Placeholder for dynamic content
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('portfolio-selector', 'options'),
    Input('refresh-portfolios-btn', 'n_clicks'),
    Input('url', 'pathname')  # Triggers on page load
)
def update_portfolio_options(n_clicks, pathname):
    portfolios = pc.get_portfolios_by_user_id(user_id)  # Fetch fresh data
    return [{"label": p.portfolio_name, "value": p.portfolio_id} for p in portfolios]


# Function for main dashboard page

def render_main_dashboard():
    return html.Div([
        dcc.Graph(id='portfolio-line-chart'),
        html.Div([
            dcc.Graph(id='portfolio-pie-chart',
                      style={'width': '48%', 'display': 'inline-block'}
                      ),
            dcc.Graph(id='portfolio-table', style={'width': '48%', 'display': 'inline-block'})
        ])
    ])


@app.callback(Output("portfolio-pie-chart", "figure"),
              Input("portfolio-selector", "value"),
              prevent_initial_call=True)
def update_pie_chart(portfolio_id):
    portfolio_info = generate_portfolio_info(portfolio_id)
    if len(portfolio_info) == 0:
        return None
    fig = pie_chart_plotter(portfolio_info)
    return fig


@app.callback(Output("portfolio-line-chart", "figure"),
              Input("portfolio-selector", "value"),
              prevent_initial_call=True)
def update_line_chart(portfolio_id):
    portfolio_info = generate_portfolio_info(portfolio_id)
    if len(portfolio_info) == 0:
        return None
    fig = line_graph_plotter(portfolio_info)
    return fig


@app.callback(Output("portfolio-table", "figure"),
              Input("portfolio-selector", "value"),
              prevent_initial_call=True)
def update_table(portfolio_id):
    portfolio_info = generate_portfolio_info(portfolio_id)
    if len(portfolio_info) == 0:
        return None
    fig = table_generator(portfolio_info)
    return fig


# Function for create portfolio page
def render_create_portfolio_page():
    return html.Div([
        html.H3("Create a New Portfolio"),
        html.Div(id="add-portfolio-status", style={'margin-top': '10px'}),
        dcc.Input(id='portfolio-name', type='text', placeholder='Portfolio Name', style={'margin-bottom': '10px'}),
        html.Button('Submit', id='submit-create', n_clicks=0),
        html.Button('Back to Dashboard', id='back-create', n_clicks=0, style={'margin-left': '10px'})
    ])


# Function for modify portfolio page
def render_modify_portfolio_page():
    portfolios = pc.get_portfolios_by_user_id(user_id)
    portfolio_options = [{"label": p.portfolio_name, "value": p.portfolio_id} for p in portfolios]

    return html.Div([
        html.Div([html.H3("Modify Portfolio")]),
        dcc.Dropdown(id='modify-portfolio-selector', options=portfolio_options,
                     placeholder='Select Portfolio to Modify',
                     style={'width': '60%', 'display': 'inline-block'}),
        html.Div(id='add-stock-section', style={'margin-top': '20px'}),
        html.Div(id='rmv-stock-section', style={'margin-top': '20px'}),
        html.Div(id='upd-name-section', style={'margin-top': '20px'}),

    ])


# Function for adding stocks to the portfolio
def render_add_stock_section(portfolio_id):
    stocks = sc.get_all_stocks()

    stock_options = [{"label": f"{stock.ticker_symbol} - {stock.company_name}", "value": stock.stock_id} for stock in
                     stocks]

    return html.Div([
        html.H4("Add Stocks to Portfolio"),
        dcc.Dropdown(id='stock-selector', style={'width': '60%'}, placeholder='Select a Stock', options=stock_options),
        dcc.Input(id='stock-quantity', type='number', placeholder='Quantity', style={'margin-top': '10px'}),
        html.Button('Add Stock', id='add-stock-btn', n_clicks=0, style={'margin-top': '10px'}),
        html.Div(id='add-stock-status', style={'margin-top': '10px'})
    ])

def render_update_name_section():

    return html.Div([
        html.H4("Update Portfolio Name"),
        dcc.Input(id='new-portfolio-name', type='text', placeholder='Insert New Name', style={'margin-top': '10px'}),
        html.Button('Update Name', id='upd-name-btn', n_clicks=0, style={'margin-top': '10px'}),
        html.Div(id='upd-name-status', style={'margin-top': '10px'})
    ])


def render_remove_stock_section(portfolio_id):
    portfolio_stocks = psc.get_all_portfolio_stocks_from_portfolio_id(portfolio_id)
    stocks = [sc.get_stock(portfolio_stock.stock_id) for portfolio_stock in portfolio_stocks]
    portfolio_stocks_options = []
    for portfolio_stock in portfolio_stocks:
        for stock in stocks:
            if portfolio_stock.stock_id == stock.stock_id:
                portfolio_pair = {"label": stock.company_name, "value": portfolio_stock.portfolio_stock_id}
                portfolio_stocks_options.append(portfolio_pair)

    return html.Div([
        html.H4("Remove Stocks from Portfolio"),
        dcc.Dropdown(id='stock-selector-rmv', style={'width': '60%'}, placeholder='Select a Stock', options=portfolio_stocks_options),
        dcc.Input(id='stock-quantity-rmv', type='number', placeholder='Quantity', style={'margin-top': '10px'}),
        html.Button('Remove Stock', id='rmv-stock-btn', n_clicks=0, style={'margin-top': '10px'}),
        html.Div(id='rmv-stock-status', style={'margin-top': '10px'}),
        html.Button('Delete Portfolio', id='delete-btn', n_clicks=0, style={'margin-top': '10px'}),
        html.Div(id='delete-status', style={'margin-top': '10px'}),
    ])


# Callback for navigation triggered by create/modify buttons
@app.callback(
    Output('url', 'pathname'),
    [Input('create-portfolio-btn', 'n_clicks'),
     Input('modify-portfolio-btn', 'n_clicks')],
    prevent_initial_call=True
)
def navigate_to_pages(n_create, n_modify):
    ctx = dash.callback_context
    if not ctx.triggered:
        return '/'

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'create-portfolio-btn':
        return '/create-portfolio'
    elif button_id == 'modify-portfolio-btn':
        return '/modify-portfolio'
    return '/'


# Callback for navigation triggered by back-create button
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('back-create', 'n_clicks')],
    prevent_initial_call=True
)
def navigate_back_create(n_back_create):
    if n_back_create:
        return '/'
    return '/'


# Callback for navigation triggered by back-modify button
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('back-modify', 'n_clicks')],
    prevent_initial_call=True
)
def navigate_back_modify(n_back_modify):
    if n_back_modify:
        return '/'
    return '/'


# Page content callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/create-portfolio':
        return render_create_portfolio_page()
    elif pathname == '/modify-portfolio':
        return render_modify_portfolio_page()
    return render_main_dashboard()

# Callback for creating a new portfolio
@app.callback(
    Output("add-portfolio-status", "children"),
    [Input('submit-create', 'n_clicks')],
    [Input('portfolio-name', 'value')],
    prevent_initial_call=True
)
def create_portfolio(n_clicks, portfolio_name):
    if n_clicks and portfolio_name:
        portfolio_controller = PortfolioController()
        all_portfolios = portfolio_controller.get_all_portfolios()
        for portfolio in all_portfolios:
            if portfolio.portfolio_name == portfolio_name:
                return

        # Create the new portfolio
        portfolio_controller.add_portfolio(portfolio_name=portfolio_name, user_id=user_id)
        all_portfolios = portfolio_controller.get_all_portfolios()
        for portfolio in all_portfolios:
            print(portfolio.portfolio_name)
        return html.Div("Portfolio created successfully!", style={'color': 'green'})
    return dash.no_update

# Callback to populate the modify portfolio selector
@app.callback(
    Output('modify-portfolio-selector', 'options'),
    [Input('url', 'pathname')]
)
def populate_modify_portfolio_selector(pathname):
    if pathname == '/modify-portfolio':
        portfolio_controller = PortfolioController()
        portfolios = portfolio_controller.get_all_portfolios()
        options = [{"label": p.portfolio_name, "value": p.portfolio_id} for p in portfolios]
        return options
    return []


# Callback to show the add stock section when a portfolio is selected
@app.callback(
    Output('add-stock-section', 'children'),
    [Input('modify-portfolio-selector', 'value')]
)
def show_add_stock_section(portfolio_id):
    if portfolio_id:
        return render_add_stock_section(portfolio_id)
    return html.Div()


@app.callback(
    Output('rmv-stock-section', 'children'),
    [Input('modify-portfolio-selector', 'value')]
)
def show_remove_stock_section(portfolio_id):
    if portfolio_id:
        return render_remove_stock_section(portfolio_id)
    return html.Div()


@app.callback(
    Output('upd-name-section', 'children'),
    [Input('modify-portfolio-selector', 'value')]
)
def show_update_name_section(portfolio_id):
    if portfolio_id:
        return render_update_name_section()
    return html.Div()


# Callback to add a stock to the portfolio
@app.callback(
    Output('add-stock-status', 'children'),
    [Input('add-stock-btn', 'n_clicks')],
    [State('modify-portfolio-selector', 'value'),
     State('stock-selector', 'value'),
     State('stock-quantity', 'value')]
)
def add_stock_to_portfolio(n_clicks, portfolio_id, stock_id, quantity):
    if n_clicks and portfolio_id and stock_id and quantity:
        try:
            # Get the latest stock data to determine the purchase price
            stock_data_controller = StockDataController()
            latest_stock_data = stock_data_controller.get_latest_stock_data_by_stock_id(stock_id)
            if not latest_stock_data:
                return html.Div("Error: No stock data found for the selected stock.", style={'color': 'red'})

            # Add the stock to the portfolio
            portfolio_stock_controller = PortfolioStockController()
            portfolio_stock_controller.add_portfolio_stock(
                portfolio_stock_id=None,  # Let the database auto-generate the ID
                portfolio_id=portfolio_id,
                stock_id=stock_id,
                quantity=quantity,
                purchase_date="2024-10-01"  # You can modify this to use the current date
            )

            return html.Div("Stock added to portfolio successfully!", style={'color': 'green'})
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={'color': 'red'})
    return html.Div()


@app.callback(
    Output('rmv-stock-status', 'children'),
    [Input('rmv-stock-btn', 'n_clicks')],
    [State('modify-portfolio-selector', 'value'),
     State('stock-selector-rmv', 'value'),
     State('stock-quantity-rmv', 'value')]
)
def remove_stock_from_portfolio(n_clicks, portfolio_id, portfolio_stock_id, quantity):
    if n_clicks and portfolio_id and portfolio_stock_id and quantity:
        try:
            old_quantity = psc.get_portfolio_stock(portfolio_stock_id).quantity
            new_quantity = old_quantity - quantity

            if new_quantity <= 0:
                psc.delete_portfolio_stock(portfolio_stock_id=portfolio_stock_id)
            else:
                psc.update_portfolio_stock(portfolio_stock_id=portfolio_stock_id, quantity=new_quantity)

            return html.Div("Stock Quantity Removed Successfully!", style={'color': 'green'})
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={'color': 'red'})
    return html.Div()


@app.callback(
    Output('delete-status', "children"),
    [Input("delete-btn", "n_clicks")],
    [State('modify-portfolio-selector', 'value')]
)
def delete_portfolio(n_clicks, portfolio_id):
    if n_clicks and portfolio_id:
        try:
            pc.delete_portfolio(portfolio_id)
            return html.Div("Portfolio Deleted Successfully", style={'color': 'green'})
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={'color': 'red'})

@app.callback(
    Output('upd-name-status', 'children'),
    [Input('upd-name-btn', 'n_clicks')],
    [State('modify-portfolio-selector', 'value'),
     State('new-portfolio-name', 'value')],
    prevent_initial_call=True
)
def update_portfolio_name(n_clicks, portfolio_id, new_name):
    if n_clicks and portfolio_id and new_name:
        try:
            # Check if the new name is not empty
            if not new_name.strip():
                return html.Div("Error: Portfolio name cannot be empty", style={'color': 'red'})

            # Check if the name already exists
            portfolio_controller = PortfolioController()
            all_portfolios = portfolio_controller.get_all_portfolios()
            for portfolio in all_portfolios:
                if portfolio.portfolio_name == new_name and portfolio.portfolio_id != portfolio_id:
                    return html.Div("Error: A portfolio with this name already exists", style={'color': 'red'})

            # Update the portfolio name
            pc.update_portfolio(portfolio_id, portfolio_name=new_name)
            return html.Div("Portfolio name updated successfully!", style={'color': 'green'})

        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={'color': 'red'})
    return html.Div()


def generate_portfolio_info(portfolio_id):
    portfolio_stocks = psc.get_all_portfolio_stocks_from_portfolio_id(portfolio_id)
    stock_ids = [portfolio_stock.stock_id for portfolio_stock in portfolio_stocks]
    stock_infos = []
    for stock_id in stock_ids:
        stock_info = {"name": sc.get_stock(stock_id).company_name,
                      "ticker": sc.get_stock(stock_id).ticker_symbol,
                      "no-stocks": psc.get_portfolio_stock_by_portfolio_id_and_stock_id(portfolio_id,
                                                                                        stock_id).quantity,
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
    if len(stock_infos) == 0:
        return None

    for stock in stock_infos:
        info = {"name": stock["name"], "value": stock["no-stocks"] * stock["current-value"]}
        pie_info.append(info)
    pie_info = pd.DataFrame(pie_info)
    fig = go.Figure(data=[go.Pie(labels=pie_info["name"], values=pie_info["value"])])
    return fig


def line_graph_plotter(stock_infos, date_before="2020-01-01", date_after="2025-01-01"):
    sets = []
    dataframes = []
    if len(stock_infos) == 0:
        return None

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


def table_generator(stock_infos):
    if len(stock_infos) == 0:
        return None

    names = [stock["name"] for stock in stock_infos]
    no_stocks = [stock["no-stocks"] for stock in stock_infos]
    current_values = [stock["current-value"] for stock in stock_infos]
    total_values = [stock["no-stocks"] * stock["current-value"] for stock in stock_infos]
    sectors = [stock["sector"] for stock in stock_infos]
    industries = [stock["industry"] for stock in stock_infos]
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
    return fig


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
