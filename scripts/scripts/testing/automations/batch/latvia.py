import os
import pandas as pd


class Latvia:
    location: str = "Latvia"
    units: str = "tests performed"
    source_label: str = "Center for Disease Prevention and Control"
    source_url: str = "https://data.gov.lv/dati/dataset/f01ada0a-2e77-4a82-8ba2-09cf0cf90db3/resource/d499d2f0-b1ea-4ba2-9600-2c701b03bd4a/download/covid_19_izmeklejumi_rezultati.csv"
    source_url_ref: str = "https://data.gov.lv/dati/eng/dataset/covid-19"
    notes: str = "Collected from the Latvian Open Data Portal"
    rename_columns: dict = {
        "Datums": "Date",
        "TestuSkaits": "Daily change in cumulative total",
    }

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.source_url, usecols=["Datums", "TestuSkaits"], sep=";")

    def pipe_rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=self.rename_columns)

    def pipe_date(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Date"] = df["Date"].str[:-1]
        df["Date"] = df["Date"].str.replace(".", "-", regex=True)
        return df

    def pipe_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.assign(
            **{
                "Country": self.location,
                "Units": self.units,
                "Source URL": self.source_url_ref,
                "Source label": self.source_label,
                "Notes": self.notes,
            }
        )

    def pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.pipe(self.pipe_rename_columns).pipe(self.pipe_date).pipe(self.pipe_metadata)

    def export(self):
        output_path = f"automated_sheets/{self.location}.csv"
        df = self.read().pipe(self.pipeline)
        df.to_csv(output_path, index=False)


def main():
    Latvia().export()


if __name__ == "__main__":
    main()
