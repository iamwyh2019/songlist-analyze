# song-list-analyze
This project applies simple analysis to your song list. Currently it supports QQ music. I may add support for Netease music some day (frankly, probably not).

This project does statistics of the authors, languages, time of publish, and genres of all songs in your list, and draws a bar chart and a pie chart to each of the four attributes.



## Deployment

### Setting up API

The QQ-music info API comes from [this project](https://github.com/jsososo/QQMusicApi) (many thanks!).You need to install node.js on your server and follow that project's instruction.

I hard-coded my API address in the code. Technically you can use my API and I will not add a blockage, but I kindly ask you to build your own, or at least keep the requests at a reasonable amount.



### Deploying this project

1. Clone this project, and upload all the files onto your server.

2. Make sure you installed the following Python dependencies:
   - Matplotlib
   - Pandas
   - Quart
   - Jinja2
   - tqdm

3. Make sure port 5000 of your server is not occupied. If yes, please go to `main.py`  line 37, and specify a different port. Example: `app.run(host = '0.0.0.0', port = 5005)`.
4. **(Optional)** If you want to add an ssl certificate, specify the path of your certification and private key, and pass them to parameters `certfile` and `keyfile`. Example: `app.run(host = '0.0.0.0', certfile = '/etc/nginx/fullchaim.pem', keyfile = '/etc/nginx/privkey.pem')`.
5. Run `main.py`. View the frontend on http://your-domain:5000 . Note that
   - "your-domain" could be the domain or ip address of your server. If you are running locally, it's "127.0.0.1" or "localhost".
   - If you specified another port on step 3, change 5000 to that port.
   - If you added an ssl certificate, use "https" instead of "http".



## Open-source

You may use any part of this project arbitrarily with no need to cite the source, as long as BOTH the following conditions are met:

1. I am NOT responsible for anything related to or incurred from this project.
2. You build your own music info API.

Or you can use this project (but need to cite the source) under the first condition. Yet I kindly ask you to build your own API, or at least keep the API requests at a reasonable amount.
