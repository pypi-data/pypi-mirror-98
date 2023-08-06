# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xh1scr']
install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'xh1scr',
    'version': '1.0.6',
    'description': 'TikTok Magic API Wrapper',
    'long_description': "#ENG\n## How to use\nIMPORT AsyncTok module\n```sh\nfrom xh1scr import AsyncTok\n```\nMake task in asynchronous func\n```sh\nasync def func():\n\tawait AsyncTok.run('xh1c2')\n\tstatus = await AsyncTok.status()\n\tlikes = await AsyncTok.likes()\n\tfollowers = await AsyncTok.followers()\n\tfollowing = await AsyncTok.following()\n\tnickname = await AsyncTok.nickname()\n\tavatar = await AsyncTok.getavatar()\n```\nbtw u can get list in run\n```sh\nfrom xh1scr import AsyncTok\nasync def func2():\n\tawait AsyncTok.run(['xh1c2','example','example2','and','more'])\n\tstatus = await AsyncTok.status()\n\tlikes = await AsyncTok.likes()\n\tfollowers = await AsyncTok.followers()\n\tfollowing = await AsyncTok.following()\n\tnickname = await AsyncTok.nickname()\n\tavatar = await AsyncTok.getavatar()\n```\n```sh\nand now that library can be not asyncronous\n```\nIMPORT TikTok module\n```sh\nfrom xh1scr import TikTok\n```\nMake task in normal func\n```sh\nasync def func():\n\tTikTok.run('xh1c2')\n\tstatus = TikTok.status()\n\tlikes = TikTok.likes()\n\tfollowers = TikTok.followers()\n\tfollowing = TikTok.following()\n\tnickname = TikTok.nickname()\n\tavatar = TikTok.getavatar()\n```\n```sh\nfrom xh1scr import TikTok\nasync def func2():\n\tTok.run(['xh1c2','example','example2','and','more'])\n\tstatus = TikTok.status()\n\tlikes = TikTok.likes()\n\tfollowers = TikTok.followers()\n\tfollowing = TikTok.following()\n\tnickname = TikTok.nickname()\n\tavatar = TikTok.getavatar()\n```\n#RU\n\n## Как использовать\nДля работы с ним надо сделать task в асинхронной функции\n(я знаю есть такое же API но с подключенной авторизацией и поиском по id но плюс моего API это удобство использования)\n```sh\nfrom xh1scr import TikTok\ndef func():\n\tTikTok.run('xh1c2') \n\tstatus = TikTok.status() \n\tlikes = TikTok.likes()\n\tfollowers = TikTok.followers()\n\tfollowing = TikTok.following()\n\tnickname = TikTok.nickname()\n\tavatar = TikTok.getavatar()\n```\nТак же в run можно передать список значений\n```sh\nfrom xh1scr import AsyncTok\ndef func2():\n\tTikTok.run(['xh1c2','example','example2','and','more'])\n\tstatus = TikTok.status()\n\tlikes = TikTok.likes()\n\tfollowers = TikTok.followers()\n\tfollowing = TikTok.following()\n\tnickname = TikTok.nickname()\n\tavatar = TikTok.getavatar()\n```\n",
    'author': 'perfecto',
    'author_email': 'rektnpc@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
