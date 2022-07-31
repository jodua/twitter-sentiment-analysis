def load_nltk_modules(module_names: list[str]) -> None:
    import nltk
    for module_name in module_names:
        try:
            nltk.download(module_name, quiet=True)
        except Exception:
            raise


def get_plot_title(filename: str) -> str:
    return 'Frequency distribution of words in ' + filename.split('/')[-1].split('.')[0]
