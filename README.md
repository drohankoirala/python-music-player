# DRK Player
A combination of react and flask.

## Steps to run on your local machine.
1. Downlaod all files:
2. Run main.py
3. Follow the steps commanded by program [Don't try to be smarter than script]
4. Download some-songs, for that follow scripts command
5. After downloading at lease 2 songs, restart the main.py and you are good to go.

The application will be accessible in your web browser at http://localhost:5000/.

## Features
- Recommend Songs: Generate song recommendations based on user activity.
- A Decent UI [HTMl + CSS + JS(react)]
- Download Music: Download music files from YouTube URLs using the provided commands.
- Download Playlists: Download all songs from a YouTube playlist.
- Move Files: Move downloaded music files to a specified directory using the move command.
- Scan for Missing Files: Scan for missing music files and restore them if found.
- API Endpoints: Access various API endpoints to interact with the application programmatically.

## API Endpoints
- /api/lists: Get information about playlists
- /api/views: Get recommended songs
- /api/view: Get recommended songs for a specific user
- /api/get_songs: Get a list of available songs

  
## Usage
Downloading Music:
- To download a single song, use the dwd -f https://www.youtube.com/watch?v=VIDEO_ID command.
- To download all songs from a playlist, use the dwd -l https://www.youtube.com/playlist?list=PLAYLIST_ID command.

Moving Files:
- Use the move --move-dir-- command to move downloaded music files to a specified directory.

Scanning for Missing Files:
- Use the scan command to scan for missing music files and restore them if found.

Generating Recommendations:
- Use the recommend command to generate song recommendations based on user activity.

## Additional Info
The program tracks your interactions and activities on the page, storing this information in a file on your local machine. Ensure you do not delete this file or modify it in any way. If you need to change its location, use a specific command. The most crucial aspect of running this script is your JSON file, which contains all your activity and music information. If you lose everything except your JSON file, you can easily redownload everything.

## About Developer
View https://rohan-koirala.com.np/ if intrested, Also if you are intrested in src directory of react,
Contact me on contact@rohan-koirala.com.np
