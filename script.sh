#!/bin/bash

DOTFILES_DIR=~/dotfiles
CONFIG_DIR=~/.config

rsync -av --progress "$DOTFILES_DIR"/ "$CONFIG_DIR"/

reboot