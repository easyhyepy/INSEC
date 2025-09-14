def generate_docs_for_language(language: str = typer.Argument(..., callback=language_callback, autocompletion=autocomplete_language)) -> None:
    """
    Generate the documentation for a specified language.
    """
    special_env_file = os.environ.get("SPECIAL_ENV_FILE")
    print(f"Special environment file: {special_env_file}")
    language_directory: Path = Path("documentation") / language
    typer.echo(f"Generating documentation for: {language}")
    final_doc_path = docs_build_path / language
    if language == "en":
        output_directory = main_docs_path
    else:
        output_directory = main_docs_path / language
        shutil.rmtree(output_directory, ignore_errors=True)
    initial_directory = os.getcwd()
    os.chdir(language_directory)
    shutil.rmtree(final_doc_path, ignore_errors=True)
    subprocess.run(["mkdocs", build, "--site-dir", final_doc_path], check=True)
    shutil.copytree(final_doc_path, output_directory, dirs_exist_ok=True)
    os.chdir(initial_directory)
    typer.secho(f"Documentation successfully generated for: {language}", color=typer.colors.GREEN)
