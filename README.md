# Pictures-to-Obsidian-Daily-Notes

Searches your photos folder for new photos, copies them to your Obsidian Vault, and links them in your daily notes. 

**Daily notes in Obsidian must be in the format MMMM Do, YYYY (November 22nd, 2021) for this to work.**

You can run this just with your computer's files, but I chose to have it access my home server's files so that when I take a picture on my phone it automatically uploads into my daily Obsidian notes. 

Only new images will be added while the program is running. They will be inserted with a timestamp in front of it. 

# Getting started

- Open the python file in a text editor
- Inside the quotation marks next to **DailyNotesPath**, paste the path to where you keep your obsidian daily notes.
- Inside the quotation marks next to **ObsidianVaultPathImages**, paste the path to where you want to keep your pictures in your Obsidian vault. Note that **DailyNotesPath** and **ObsidianVaultPathImages** can be the same path if you want. 
- Inside the quotation marks next to **ImageFolderPath**, paste the path to where you keep the pictures you want to have upload new files. 
- If you want to embed images, set the exclMark variable to True. 
- There is a delay if you exceed a certain amount of photos in 5 minutes, so that you don't overcrowd your daily notes. By default it is set to 10 but you can set it to whatever you want. 




