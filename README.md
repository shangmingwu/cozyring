# Cozyring: make the internet cozier

I love webrings.
If you love wandering on the internet, clicking down into rabbit holes at your leisure, then I promise you'll love webrings too.

## Installation

Cozyring uses Python 3.9 with FastAPI, Uvicorn and Jinja2.

### Manual installation

This clones the repository, creates a virtual environment, then installs the dependencies in the virtual environment.

```sh
git clone https://github.com/shangmingwu/cozyring.git
cd cozyring
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure to configure the sites you want in your webring with slugs and URLs in the config.toml file.
Then, you can start the server with Uvicorn.
By default, Uvicorn will start on 0.0.0.0:8000, and you can edit `main.py` to change the port.
**If you decide to use Uvicorn to deploy from a server manually, make sure to set reload to false in production by editing `main.py`.**

```sh
python main.py
```

### Vercel deployment

Cozyring can be deployed on Vercel using serverless functions.
You can deploy a fork of this GitHub repository to Vercel, or you can deploy a local modified copy from the command line.

```sh
yarn global add vercel
vercel login
vercel .
```

## Usage

### Navigating a webring

A webring works by having each site in the ring provide links to the previous and next sites in the ring.
Visitors can then easily traverse the ring of sites in sequence.
When you add a site to Cozyring, whoever runs that site should the links to the next and previous sites in the ring corresponding to their own site.

### Adding sites to Cozyring

You can add sites to Cozyring by adding entries into `sites.json` and then restarting the Cozyring deployment.
An example list of sites is found in `sites.example.json`.
Once the site shows up in the list, the owner of the site needs to add links to the appropriate next and previous endpoints.

### Customization

The landing and error page are built from templates in the `templates` folder using Jinja2.
You can edit `landing.html`, `error.html`, `instructions_list.html` and `instructions.html`.
Additionally, you can add or change static assets (custom CSS files, images, icons, etc.) in the `static/` folder.
