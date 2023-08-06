import typer
from modoo import mapid, fixid, adddocmeta, validate, mergeza, convid, checkwd

app = typer.Typer()


@app.command()
def map_id(input_json_path: str, rw_dir_path: str):
    mapid.run(input_json_path, rw_dir_path)


@app.command()
def fix_id(input_json_path: str, id_map_file_path: str):
    fixid.run(input_json_path, id_map_file_path)


@app.command()
def add_doc_meta(input_json_path: str, rw_dir_path: str):
    adddocmeta.run(input_json_path, rw_dir_path)


@app.command()
def valid(input_json_path: str, schema_path: str):
    validate.run(input_json_path, schema_path)


@app.command()
def merge_za(zas_file_path: str, zao_file_path: str, new_file_id: str):
    mergeza.run(zas_file_path, zao_file_path, new_file_id)


@app.command()
def conv_id(input_json_path: str):
    convid.run(input_json_path)


@app.command()
def check_wd(input_json_path: str):
    checkwd.run(input_json_path)


def main():
    app()


if __name__ == "__main__":
    main()
