# How to get root
https://askubuntu.com/questions/515292/how-to-get-gui-sudo-password-prompt-without-command-line
https://www.freedesktop.org/software/polkit/docs/0.105/ref-api.html
https://stackoverflow.com/questions/41177874/how-do-i-connect-dbus-and-policykit-to-my-function-in-python
https://pypi.org/project/policykit/

checkout `main` in https://github.com/storaged-project/blivet-gui/blob/master/blivet-gui
Starts a daemon with pkexec that does the root stuff. They talk using a socket.
client code in `blivet-gui/blivetgui/communication/client.py` and server in `blivet-gui/blivetgui/communication/server.py`

# gtk4
https://developer.gnome.org/gtk4/stable/gtk.html
https://lazka.github.io/pgi-docs/Gtk-3.0/classes/TreeView.html

