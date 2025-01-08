from plotly.data import gapminder  # dataset
from dash import dcc, html, Dash, callback, Input, Output  # layout and widgets
import plotly.express as px  # graphs and charts
import plotly.graph_objects as go  # table creation

######################  DATASET  ######################
css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

gapminder_df = gapminder()  # Removed incorrect parameters from gapminder()
gapminder_df["Year"] = gapminder_df["year"]  # Correct column name capitalization
gapminder_df["Year"] = gapminder_df["Year"].astype(int)

###################  CHARTS  #########################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(gapminder_df.columns), align='left'),
        cells=dict(values=[gapminder_df[col] for col in gapminder_df.columns], align='left')
    )])
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t": 0, "l": 0, "r": 0, "b": 0}, height=700)
    return fig


def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["continent"] == continent) & (gapminder_df["Year"] == year)]
    filtered_df = filtered_df.sort_values(by="pop", ascending=False).head(15)

    fig = px.bar(filtered_df, x="country", y="pop", color="country",
                 title=f"Population for {continent} Continent in {year}", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["continent"] == continent) & (gapminder_df["Year"] == year)]
    filtered_df = filtered_df.sort_values(by="gdpPercap", ascending=False).head(15)

    fig = px.bar(filtered_df, x="country", y="gdpPercap", color="country",
                 title=f"GDP per Capita for {continent} Continent in {year}", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df["continent"] == continent) & (gapminder_df["Year"] == year)]
    filtered_df = filtered_df.sort_values(by="lifeExp", ascending=False).head(15)

    fig = px.bar(filtered_df, x="country", y="lifeExp", color="country",
                 title=f"Life Expectancy for {continent} Continent in {year}", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig


def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df["Year"] == year]

    fig = px.choropleth(filtered_df, color=variable,
                        locations="iso_alpha", locationmode="ISO-3",
                        color_continuous_scale="RdYlBu", hover_data=["country", variable],
                        title=f"{variable} Choropleth Map [{year}]")
    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6",
                      height=600, margin={"l": 0, "r": 0})
    return fig


##########################  WIDGETS  ######################
continents = [{"label": cont, "value": cont} for cont in gapminder_df["continent"].unique()]
years = [{"label": yr, "value": yr} for yr in sorted(gapminder_df["Year"].unique())]

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia", clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=years, value=1952, clearable=False)

cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia", clearable=False)
year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952, clearable=False)

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia", clearable=False)
year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952, clearable=False)

var_map = dcc.Dropdown(id="var_map", options=[
    {"label": "Population", "value": "pop"},
    {"label": "GDP per Capita", "value": "gdpPercap"},
    {"label": "Life Expectancy", "value": "lifeExp"}
], value="lifeExp", clearable=False)

year_map = dcc.Dropdown(id="year_map", options=years, value=1952, clearable=False)

#######################  APP LAYOUT  ######################
app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Dataset Analysis", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs([
            dcc.Tab(label="Dataset", children=[
                html.Br(),
                dcc.Graph(id="dataset", figure=create_table())
            ]),

            dcc.Tab(label="Population", children=[
                html.Br(),
                "Continent", cont_population, "Year", year_population, html.Br(),
                dcc.Graph(id="population")
            ]),

            dcc.Tab(label="GDP per Capita", children=[
                html.Br(),
                "Continent", cont_gdp, "Year", year_gdp, html.Br(),
                dcc.Graph(id="gdp")
            ]),

            dcc.Tab(label="Life Expectancy", children=[
                html.Br(),
                "Continent", cont_life_exp, "Year", year_life_exp, html.Br(),
                dcc.Graph(id="life_expectancy")
            ]),

            dcc.Tab(label="Choropleth Map", children=[
                html.Br(),
                "Variable", var_map, "Year", year_map, html.Br(),
                dcc.Graph(id="choropleth_map")
            ])
        ])
    ], className="col-8 mx-auto"),
], style={"background-color": "#e5ecf6", "height": "100vh"})


#################  CALLBACKS  #################
@callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value")])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)


@callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value")])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)


@callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value")])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)


@callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value")])
def update_map(variable, year):
    return create_choropleth_map(variable, year)


if __name__ == "__main__":
    app.run(debug=True)
