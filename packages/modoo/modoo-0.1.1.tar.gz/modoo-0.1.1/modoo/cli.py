import typer
from modoo import mapid, fixid, adddocmeta, validate, mergeza, convid

app = typer.Typer()


@app.command()
def map_id(input_file_path: str, rw_dir_path: str, result_path: str):
    mapid.run(input_file_path, rw_dir_path, result_path)


@app.command()
def fix_id(input_json_path: str, id_map_file_path: str, output_json_path: str):
    fixid.run(input_json_path, id_map_file_path, output_json_path)


@app.command()
def add_doc_meta(input_json_path: str, rw_dir_path: str, annotation_level: str,  output_json_path: str):
    adddocmeta.run(input_json_path, rw_dir_path,
                   annotation_level, output_json_path)


@app.command()
def valid(input_json_path: str, schema_path: str, log_path: str):
    validate.run(input_json_path, schema_path, log_path)


@app.command()
def merge_za(zas_file_path: str, zao_file_path: str, new_file_id: str):
    mergeza.run(zas_file_path, zao_file_path, new_file_id)


@app.command()
def conv_id(input_json_path: str, output_json_path: str):
    convid.run(input_json_path, output_json_path)


def main():
    app()


if __name__ == "__main__":
    main()
