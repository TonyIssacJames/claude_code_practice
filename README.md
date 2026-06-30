# claude_code_practice


# Tips

- How to set shift + Enter
- C:\Users\tonyj\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json

-         {
            "command":
            {
                "action": "sendInput",
                "input": "\n"
            },
            "id": "User.sendInput.DFCDAF06"
        }
		
- The above block  is only the action definition.
  For Shift+Enter to actually fire it, you also need a keybinding entry that references this id, somewhere in your keybindings array:



    "keybindings": 
    [
        {
            "id": "User.splitPane.A6751878",
            "keys": "alt+shift+d"
        },
        {
            "id": "User.sendInput.DFCDAF06",
            "keys": "shift+enter"
        },
	],