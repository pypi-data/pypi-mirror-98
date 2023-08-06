# discord-ext-paginator

An package for discord pagination.

# How to install
```
pip install discord-ext-paginator
```

## Example
```python
from discord.ext import paginator

def get_pages():
	   pages = []
	   # Generate a list of 5 embeds
	   for i in range(1, 6):
	   	   embed = discord.Embed()
	   	   embed.title = f"I'm the embed {i}!"
	   	   pages.append(embed)
	   return pages

@bot.command()
async def paginator(ctx):
	pag = paginator.Paginator(pages=get_pages())
	await pag.start(ctx)
```