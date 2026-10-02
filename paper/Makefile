.PHONY: draft check manuscript supplementary clean

draft:
	powershell -NoProfile -ExecutionPolicy Bypass -File .\build.ps1 -Mode draft

check:
	powershell -NoProfile -ExecutionPolicy Bypass -File .\build.ps1 -Mode check

manuscript:
	powershell -NoProfile -ExecutionPolicy Bypass -File .\build.ps1 -Mode manuscript

supplementary:
	powershell -NoProfile -ExecutionPolicy Bypass -File .\build.ps1 -Mode supplementary

clean:
	powershell -NoProfile -Command "Remove-Item -LiteralPath '.\build\draft','.\build\supplementary' -Recurse -Force -ErrorAction SilentlyContinue"
