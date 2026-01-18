import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def search(keyword: str):
  print(f"searching for {keyword} in database")


@app.command()
def summarize(file: str):
  print(f"summarizing {file}")


if __name__ == "__main__":
  app()