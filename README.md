# NeoHack Arcade Android

Frontend nativo para Android que carrega o núcleo FBNeo por meio da interface Libretro. O núcleo usa código upstream do projeto FBNeo; este aplicativo é uma integração/frontend, não um emulador escrito do zero.

## Compatibilidade e desempenho

- APK preparado para `armeabi-v7a` (ARM 32-bit) e `arm64-v8a` (ARM 64-bit).
- Versão mínima prevista: Android 5.0 (API 21). Dispositivos muito antigos ou fora dessas arquiteturas podem não ser compatíveis.
- O desempenho depende do processador, GPU, memória, sistema e do jogo. Ainda não foi testado em um Galaxy J8 nem em outros aparelhos físicos; não há garantia de funcionamento sem travamentos em todos os celulares.

## ROMs e BIOS

O projeto e o APK não incluem ROMs, BIOS nem arquivos de jogos. Selecione apenas arquivos que você tenha direito de usar. No app, escolha a ROM Neo Geo e, quando necessário, a BIOS Neo Geo usando o seletor de arquivos do Android.

## Licenças

O núcleo FBNeo é distribuído conforme a licença incluída no APK em `assets/FBNeo-LICENSE.txt`. A integração Android LibretroDroid também tem sua licença incluída no APK em `assets/LibretroDroid-LICENSE.txt`. Consulte os textos completos e os repositórios upstream: [FBNeo](https://github.com/libretro/FBNeo) e [LibretroDroid](https://github.com/Swordfish90/LibretroDroid).
