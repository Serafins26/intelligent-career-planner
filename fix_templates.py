import pathlib, re

templates = pathlib.Path(r'D:\Meu Portfolio e HUB\templates')

for f in templates.glob('*.html'):
    txt = f.read_text(encoding='utf-8')
    # Replace {{% with {% and %}} with %}
    fixed = txt.replace('{{% ', '{% ').replace(' %}}', ' %}').replace('%}}', '%}').replace('{{% ', '{% ')
    # Also handle end tags without spaces: {%endfor%}
    fixed = fixed.replace('{{%', '{%').replace('%}}', '%}')
    # Replace {{{{ with {{ and }}}} with }}
    fixed = fixed.replace('{{{{', '{{').replace('}}}}', '}}')
    f.write_text(fixed, encoding='utf-8')
    print(f'Fixed: {f.name}')

print('Done.')
