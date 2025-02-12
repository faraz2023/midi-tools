{ pkgs }: {
    deps = [
        pkgs.python39
        pkgs.fluidsynth
        pkgs.pkg-config
        pkgs.alsaLib
        pkgs.glib
        pkgs.libsndfile
        pkgs.readline
        pkgs.ncurses
    ];
}