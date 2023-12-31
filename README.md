# TrackTrove
## Context

TrackTrove is an application that allows users to download music from Spotify using the Spotify API. it provides a basic 
User Interface that allows users to easily operate and authenticate Spotify Links and download songs.

## Prerequisites

* Python3.x must be compatible and installed on your machine.

* A Spotify developer account to access the required API keys.

## Setup and Installation

Clone the repository to your local machine:

```bash
  git clone https://github.com/fynn07/TrackTrove
```
```bash
  cd TrackTrove
```

Install the required dependencies:

```bash
  pip install pytube
```
```bash
  pip install dotenv
```

Create a `.env` file containing your Spotify API keys.
```
CLIENT_ID      =  <<your spotify api client id here>>
CLIENT_SECRET  =  <<your spotify api client secret here>>
```

Run the application locally:

```bash
  python GUI.py
```

## Usage
1. Launch the application and choose from the three buttons the spotify download format of your choice.

2. Press the download button and choose the directory of the download.

3. Wait for the download to finish.

4. Enjoy! and thank you for using TrackTrove.

## Notes

This application is for education purposes only and should not be used to violate Spotify's terms of service. Downloaded music should be used responsibly and in compliance with copyright laws.