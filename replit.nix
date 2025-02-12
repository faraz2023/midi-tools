{ pkgs }: {
    deps = [
        pkgs.python39
        pkgs.fluidsynth
        pkgs.pkg-config
        pkgs.libfluidsynth
        pkgs.alsa-lib
    ];
}