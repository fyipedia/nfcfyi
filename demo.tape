# nfcfyi — Python NFC API Client Demo
Output demo.gif

Set FontSize 20
Set Width 1000
Set Height 560
Set Shell "zsh"
Set Theme "Catppuccin Mocha"
Set TypingSpeed 30ms
Set Padding 24

Type "uv run --with nfcfyi python3"
Enter
Sleep 2s

Type "from nfcfyi import NFCFYI"
Enter
Sleep 1s

Type "client = NFCFYI()"
Enter
Sleep 1s

Type "# Search NFC chips"
Enter
Sleep 0.5s

Type "client.search('ntag')"
Enter
Sleep 2.5s

Type "# Look up a chip"
Enter
Sleep 0.5s

Type "client.chip('ntag-216')"
Enter
Sleep 3s

Type "exit()"
Enter
Sleep 1s
