import pandas as pd


class FileProcessor:
    """Handles processing files from ZTM. Example operations include:
    - unzipping file archive
    - filtering files on a given column
    - removing selected columns from the files
    - setting new column names"""

    def unzip_file_archive(self, file_path: str, destination_path: str = None) -> bool:
        """Opens file archive provided by ZTM and unpacks the files to the provided directory."""
        # TODO
        pass

    def filter_on_column(
        self, df: pd.DataFrame, col_name: str, col_value: str | int | float | bool
    ) -> pd.DataFrame:
        """Filters the provided DataFrame so that only the rows
        with the provided column value are included."""
        return df[df[col_name] == col_value]

    def remove_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Removes chosen columns from the provided DataFrame."""
        return df.drop(columns, axis=1)

    def set_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Sets new column names in the provided DataFrame."""
        df_copy = df.copy()
        df_copy.columns = columns
        return df_copy
