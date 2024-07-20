# Domestic Tranqulity in the 21st century

Uses [AI Vision](https://pypi.org/project/groundlight/) to insure the domestic tranquility
by keeping an eye on how clean your kitchen is.

# Setting up

## Installing python dependencies

```
pip3 install -r requirements.txt
sudo apt update && sudo apt install -y mpg321
```


## Camera configuration and preview

You need to customize the `framegrab.yaml` file to point to the correct camera.
See [framegrab](https://github.com/groundlight/framegrab) for reference, but this
file is a pretty good starting point.  It can use a local Raspberry Pi or USB camera,
or most any networked RTSP camera.  

You can check that the camera code is all working properly by seeing a preview in
your terminal (if you have an advanced terminal program such as
[iTerm2](https://iterm2.com/)).

```
python3 trycamera.py
```

## Stashing your secrets

Put your secrets in the file `.secret-env` that looks like:

```
export CAMERA_PASSWORD=rtsp-password...
export GROUNDLIGHT_API_TOKEN=api_...
```

Then before you run this code run:

```
source .secret-env
```


## Groundlight account setup

You can use a free Groundlight account.  Then get an
[API token](https://code.groundlight.ai/python-sdk/docs/getting-started/api-tokens) and save it as an environment variable:

```
export GROUNDLIGHT_API_TOKEN="api_..."
```


## Running the real thing

```
python3 app.py
```

You might want to edit the motion detection parameters to make it more or less sensitive.


## Hardware

I used a Raspberry Pi 4.  It will work anywhere you have the right python
and libraries installed.  I used Groundlight's [pre-built Raspberry Pi image](https://github.com/groundlight/groundlight-pi-gen).


### Audio

On Raspberry pi, alsa is what I've used.  You can check that it's working with:

```
speaker-test -t wav -c 2
```

Try editing your `/etc/asound.conf` file to set the correct device.  Then run:

```
sudo alsa force-reload
```

And set the environment variable so pygame uses it:

```
export SDL_AUDIODRIVER=alsa
```

You might want to add this to your `.secret-env` file so you don't have to keep
setting it up.

