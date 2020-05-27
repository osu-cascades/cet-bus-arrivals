with import <nixpkgs> {};
let
  my-packages = python-packages: with python-packages; [
    python3Packages.flask
    beautifulsoup4
  ];
  python-with-my-packages = python3.withPackages my-packages;
in
  pkgs.mkShell {
    buildInputs = [ python-with-my-packages python3Packages.flask ];
  }
