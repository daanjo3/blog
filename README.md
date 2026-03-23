# Blog

My minimalistic blogging environment, inspired by [Veit's blog](https://blog.veitheller.de/).

## Stack

This blog is powered by a markdown-first environment, because I like writing that the most. The following tools are used to transform a collection of markdown files into the blog:

- [markdown-it-py](https://markdown-it-py.readthedocs.io)
- [jinja](https://jinja.palletsprojects.com/en/stable/)
- [CloudFlare Pages](https://developers.cloudflare.com/pages/)

## Deployment

CloudFlare Pages are used to host this blog. For the time being the Wrangler CLI is used for this.

```sh
# link CloudFlare session to CLI
pnpx wrangler login

# builld the latest state of the blog
source ./venv/bin/activate
python ./generator/main.py

# deploy the latest state
pnpx wrangler pages deploy build
```

At some point Github Actions will be used to automatically push changes on the main branch to the live environment.