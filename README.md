# pawfetch

pawfetch is the cutest fetch script, featuring (trans)puppies! pawfetch provides an aesthetically pleasing terminal fetch with system information, all displayed in the catppuccin color scheme! (https://catppuccin.com/)

## dependencies
1. python
2. python-psutil

## installation
   ```
   git clone https://github.com/jade-gay/pawfetch.git
   cd pawfetch
   makepkg -si
   ```

## configuration
the configuration file is located at ~/.config/pawfetch/config.paw. the default settings can be found in the load_config() function in the script.

example configuration:
```
[settings]
title_color = #f5c2e7
info_color = #cdd6f4
ascii_color1 = #74c7ec
ascii_color2 = #f5c2e7
ascii_color3 = #cdd6f4
hostname_format = {user}@{hostname}
```

## dependencies
python 3
psutil

## license
this project is licensed under the GPL license

## repository
https://github.com/jade-gay/pawfetch
