import marimo

__generated_with = "0.10.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        ATTACH IF NOT EXISTS 'md:FG_DWH'
        """
    )
    return (FG_DWH,)


@app.cell
def _(mo):
    mo.md(r"""Let's start investigating the RAW table for the Schema and how to transform it into an intermediate table then a fact table""")
    return


@app.cell
def _():
    return


@app.cell
def _(FG_DWH, mo, totalpowerraw2022_2023):
    _df = mo.sql(
        f"""
        SELECT * FROM FG_DWH.mockdashraw.totalpowerraw2022_2023 
        USING SAMPLE 100
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        DESCRIBE "FG_DWH".mockdashraw.totalpowerraw2022_2023
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### Initial Draft of the intermediate table

        This will eventually become the fact table. I'm working on the Date and Time dimensions first. 

        After that I will move the sources to their own dimension table.

        - [x] Work on Time Dimension Table
        - [x] Transform Raw Table for the Time Dimension Table
        - [ ] Create Intermediate Table from Raw Table with TimeDim Key
        - [ ] Work on Date Dimension Table
        - [x] Transform Raw Table for Date Dimension Table
        - [ ] Create Intermediate Table from previous intermediate table for DateDim Key
        - [ ] Create Source Dimension Table
        """
    )
    return


@app.cell
def _(FG_DWH, mo, totalpowerraw2022_2023):
    testdf = mo.sql(
        f"""
        SELECT startTime::DATE as StartDate,
        startTime::TIME as StartTime,
        endTime::DATE as EndDate,
        endTime::TIME as EndTime, 
        "Wind power production - real time data" as WindPowerGenerated,
        "Nuclear power production - real time data" as NuclearPowerGenerated,
        "Hydro power production - real time data" as HydroPowerGenerated,
        "Electricity production in Finland - real time data" as AllPowerGenerated
        FROM FG_DWH.mockdashraw.totalpowerraw2022_2023
        USING SAMPLE 100
        """
    )
    return (testdf,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
