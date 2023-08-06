# discord-ext-paginator
<a href="https://pypi.org/project/discord-ext-paginator" traget="_blank">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/discord-ext-paginator">
</a>

<a href="https://pypi.org/project/discord-ext-paginator" traget="_blank">
	<img alt="PyPI - Downloads" src="https://pepy.tech/badge/discord-ext-paginator">
</a>

An package for discord pagination.

# How to install

```shell
pip install discord-ext-paginator
```

## Example
```python
from discord.ext import paginator

def get_pages():
	   pages = [discord.Embed(title=f"I'm the embed {i}!") for i in range(1, 6)]

@bot.command()
async def paginator(ctx):
	pag = paginator.Paginator(pages=get_pages())
	await pag.start(ctx)
```
