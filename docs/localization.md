# How to use localization

The localization is based on the [gettext](https://www.gnu.org/software/gettext/) library.
The translation files are located in the `locale` directory.

---

To sync translation files with the source code, run the following command:

```bash
pybabel extract -o locale/messages.pot .
```

To update the translation files, run the following command:

```bash
pybabel update -i locale/messages.pot -d locale
```

If you want to add a new language, run the following command:

```bash
pybabel init -i locale/messages.pot -d locale -l <language_code>
```

---

Translate the strings in the `locale/<language_code>/LC_MESSAGES/messages.po` file.
After that, run the following command to compile the translation:

```bash
pybabel compile -d locale
```

