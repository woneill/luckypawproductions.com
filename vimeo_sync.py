#!/usr/bin/env python3
import os,re,requests,vimeo
from slugify import slugify
from dotenv import load_dotenv
from textwrap import indent

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SHOWCASE_ID = os.getenv('SHOWCASE_ID')

portfolio_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "content",
    "portfolio"
)

client = vimeo.VimeoClient(
    token=ACCESS_TOKEN,
    key=CLIENT_ID,
    secret=CLIENT_SECRET
)

presets = client.get(f'https://api.vimeo.com/me/presets', params={'fields': 'uri,name'})
showcase_preset_id = next(os.path.basename(preset['uri']) for preset in presets.json()["data"] if preset['name'] == 'Showcase')

response = client.get(f'https://api.vimeo.com/me/albums/{SHOWCASE_ID}/videos', params={'per_page': 100, 'fields': 'uri,name,description,tags,link,pictures.base_link'})
showcase = response.json()["data"]

weight = -100
for video in showcase:
    weight += 1
    video_dir = slugify(video["name"])
    dirname = os.path.join(portfolio_dir, video_dir)
    vimeo_id = os.path.basename(video["uri"])
    # role_line_regex = re.compile('^Role:.*$', re.MULTILINE)
    # date_range_regex = re.compile('\d{4}(?: to \d{4})?')
    # description = role_line_regex.sub('', video["description"])
    # date_range = ""

    # role_line = role_line_regex.search(video["description"])
    # if role_line:
    #     if date_range_regex.search(role_line.group()):
    #         date_range = date_range_regex.search(role_line.group()).group()

    # Add embed presets
    r = client.put(f'https://api.vimeo.com/videos/{vimeo_id}/presets/{showcase_preset_id}')
    print(r.status_code)

    # Add 'luckypawproductions.com' to video whitelist
    r = client.put(f'https://api.vimeo.com/videos/{vimeo_id}/privacy/domains/luckypawproductions.com')
    print(r.status_code)

    # Set embed privacy to whitelist
    r = client.patch(f'https://api.vimeo.com/videos/{vimeo_id}', data={"privacy":{"embed":"whitelist"}})

    if not os.path.exists(dirname):
        print(f"Making directory {dirname}")
        os.mkdir(dirname)

    r = requests.get(video["pictures"]["base_link"] + ".jpg")
    if r.status_code == 200:
        with open(os.path.join(dirname, "thumbnail.jpg"), 'wb') as f:
            f.write(r.content)

    f = open(os.path.join(dirname, "index.md"), "w")
    f.write(fr"""---
title: |
{indent(video["name"], '     ')}
description: |
{indent(video["name"], '     ')}
work: {video["tags"]}
thumbnail: {video_dir}/thumbnail.jpg
projectUrl:
weight: {weight}
---
{{{{< vimeo {vimeo_id} >}}}}

***

{video["description"]}
""")
