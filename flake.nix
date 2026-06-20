{
  description = "Development shell for embedded and IoT learning labs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in {
          default = pkgs.mkShell {
            packages = [
              pkgs.python3
              pkgs.micropython
            ];

            shellHook = ''
              echo "learning-embedded-iot dev shell"
              echo "Try: python3 projects/sensor-simulator/test_sensor_simulator.py"
              echo "Try: micropython projects/micropython-rp2-blink/main.py"
            '';
          };
        });
    };
}
