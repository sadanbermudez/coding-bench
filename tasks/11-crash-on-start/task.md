Running `python -m notes stats sample` crashes with:

```
Traceback (most recent call last):
  ...
  File "notes/storage.py", line 2, in <module>
    from notes.models import Note
  File "notes/models.py", line 2, in <module>
    from notes.storage import slugify
ImportError: cannot import name 'slugify' from partially initialized module 'notes.storage' (most likely due to a circular import)
```

Fix the root cause so the command works and prints `2 notes, 8 words, tags: ai, chess`. `notes.models.Note`, `notes.storage.load_folder` and `notes.storage.slugify` must all still be importable from where they are now.
