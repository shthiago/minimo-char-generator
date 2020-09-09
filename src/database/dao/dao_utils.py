'''Module for avoid code repetition'''


SQL_THEME_FILTER_CONDITION = '''AND t.id IN (
                SELECT id FROM theme WHERE name IN :filter_themes
            )'''
