import os
import re
import string
import unicodedata
from pathlib import Path
import sys

try:
    import ftfy
    def fix_text(s):
        return ftfy.fix_text(s)
except Exception:
    def fix_text(s):
            return s

try:
        from spellchecker import SpellChecker
        SPELLCHECKER_AVAILABLE = True
        _SPELL = SpellChecker()
except Exception:
        SPELLCHECKER_AVAILABLE = False
        _SPELL = None

FILES_DIR = Path('./files')
OUT_DIR = Path('./data/cleaned')

IMAGE_WIKI_RE = re.compile(r'!\[\[.*?\]\]')
IMAGE_MD_RE = re.compile(r'!\[.*?\]\(.*?\)')
WIKI_LINK_RE = re.compile(r'\[\[(.*?)\]\]')
CODE_BLOCK_RE = re.compile(r'```.*?```', re.DOTALL)
INLINE_CODE_RE = re.compile(r'`([^`]*)`')
HTML_TAG_RE = re.compile(r'<[^>]+>')
MULTI_WS_RE = re.compile(r"\s+", re.MULTILINE)
FRONTMATTER_RE = re.compile(r'^---\s*.*?\s*---\s*', re.DOTALL | re.MULTILINE)

PUNCT_TRANSLATOR = str.maketrans('', '', string.punctuation)


def clean_text(text: str, correct_spelling: bool = True) -> str:
    text = fix_text(text)
    # remove frontmatter if any
    text = re.sub(FRONTMATTER_RE, ' ', text)
    # remove fenced code blocks
    text = re.sub(CODE_BLOCK_RE, ' ', text)
    # remove image embeds
    text = re.sub(IMAGE_WIKI_RE, ' ', text)
    text = re.sub(IMAGE_MD_RE, ' ', text)
    # replace wiki links [[A|B]] or [[A]] -> inner
    def wiki_repl(m):
        inner = m.group(1)
        # take part after pipe if present
        return inner.split('|')[-1]
    text = re.sub(WIKI_LINK_RE, wiki_repl, text)
    # inline code
    text = re.sub(INLINE_CODE_RE, r"\1", text)
    # strip html tags
    text = re.sub(HTML_TAG_RE, ' ', text)
    # normalize unicode
    text = unicodedata.normalize('NFKC', text)
    # remove punctuation
    text = text.translate(PUNCT_TRANSLATOR)
    # normalize whitespace
    text = re.sub(MULTI_WS_RE, ' ', text)
    text = text.strip()
    # lowercasing for normalization
    text = text.lower()

    # optional spelling correction (best-effort; requires `pyspellchecker`)
    if correct_spelling:
        if SPELLCHECKER_AVAILABLE:
            words = text.split()
            misspelled = _SPELL.unknown(words)
            if misspelled:
                corrected_words = []
                for w in words:
                    if w in misspelled:
                        c = _SPELL.correction(w)
                        corrected_words.append(c if c else w)
                    else:
                        corrected_words.append(w)
                text = ' '.join(corrected_words)
        else:
            # warn once that spellchecker is unavailable
            print('Warning: spellchecker package not available; skipping spelling correction', file=sys.stderr)

    return text


def process_file(path: Path, out_dir: Path = OUT_DIR, write: bool = False, correct_spelling: bool = True):
    """Process a markdown file and return cleaned text.

    If `write` is True the cleaned text will be saved to `out_dir` and the
    output Path will be returned. If `write` is False (default) the cleaned
    string is returned (suitable for in-memory indexing).
    """
    with path.open('r', encoding='utf-8') as f:
        raw = f.read()
    cleaned = clean_text(raw, correct_spelling=correct_spelling)
    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / (path.stem + '.clean.txt')
        with out_path.open('w', encoding='utf-8') as f:
            f.write(cleaned)
        return out_path
    return cleaned


def main():
    files = list(FILES_DIR.glob('*.md'))
    if not files:
        print('No markdown files found in', FILES_DIR)
        return
    results = []
    for p in files:
        cleaned = process_file(p, write=False)
        results.append((p.name, cleaned))
    print('Processed', len(results), 'files (in-memory). Previews:')
    for src, cleaned in results:
        preview = cleaned[:200].replace('\n', ' ')
        print(f'- {src}: {len(cleaned)} chars; preview: {preview!s}')


if __name__ == '__main__':
    main()
