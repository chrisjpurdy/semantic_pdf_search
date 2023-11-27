# semantic_pdf_search

A small cmd line tool to return a list of papers in a folder that match a specified concept/topic.

Example use:
```bash
$ python3 semantic_pdf_search.py ../my_pdfs "A higher order logic, but just for natural numbers"
../my_pdfs/cyclic-proof-system-for-hfln.pdf
```

The tool requires a valid OpenAI API key, stored in the `OPENAI_API_KEY` environment variable. It can also be provided in a `.env` file.
