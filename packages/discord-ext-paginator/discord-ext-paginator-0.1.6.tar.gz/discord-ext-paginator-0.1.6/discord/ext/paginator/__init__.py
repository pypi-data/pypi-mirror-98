import discord
from discord.ext import commands
from typing import Union, List, Optional
from contextlib import suppress



class Paginator:
	
	__slots__ = ('_pages', 'index', 'current', 'timeout', 'ctx', 'message', 'compact', '_buttons',)
	
	
	def __init__(self, *, entries: Union[List[discord.Embed], discord.Embed] = None, timeout: float = 90.0,):
			
		self._pages = entries 
		self.index = 0
		self.current = 1
		self.timeout = timeout
		self.ctx = None
		self.message = None
		if len(self._pages) == 2:
			self.compact = True
			self._buttons = {
		"◀️": "stop",
		"▶️": "plus",
		"⏹️": "minus",
		}
		else:
			self.compact = False
			self._buttons = {
		"⏩": "stop",
		"▶️": "plus",		
		"◀️": "last",
		"⏪": "first",
		"⏹️": "minus"
		    }
	
	async def start(self, ctx):
		    self.ctx = ctx
		    
		    await self._paginate()
		    
	async def _paginate(self):
		    with suppress(discord.HTTPException, discord.Forbidden, IndexError):
		    	self.message = await self.ctx.send(embed=self._pages[0])
		    for b in self._buttons:
		    	await self.message.add_reaction(b)
		    def check(reaction, user):
		    	return str(reaction.emoji) in self._buttons and user == self.ctx.author
		    while True:
		    	try:
		    		reaction, user = await self.ctx.bot.wait_for("reaction_add", check=check, timeout=self.timeout)
		    		if str(reaction.emoji) == "⏹️":
		    			await self.message.delete()
		    		if str(reaction.emoji) == "▶️" and self.current != len(self._pages):
		    			self.current += 1
		    			await self.message.edit(embed=self._pages[self.current-1])	
		    		if str(reaction.emoji) == "◀️" and self.current > 1:
		    			self.current -= 1
		    			await self.message.edit(embed=self._pages[self.current-1])
		    		if str(reaction.emoji) == "⏩":
		    			self.current = len(self._pages)
		    			await self.message.edit(embed=self._pages[self.current-1])
		    		if str(reaction.emoji) == "⏪":
		    			self.current = len(self._pages)-len(self._pages)
		    			await self.message.edit(embed=self._pages[self.current-1])		    				
		    	except:
		    		with suppress(discord.Forbidden, discord.HTTPException):
		    			for b in self._buttons:
		    				await self.message.remove_reaction(b, self.ctx.bot.user)
		    		break
