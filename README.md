# blender-text-to-speech
### blender wrapper for pyttsx3 (offline text to speech)
* make audio captions quickly
* options for pitch, rate and different voices
* convert closed captions files to audio (.srt, .srb and .txt) audio strips placed at timecodes if provided
* importing .txt files with no timecodes will place the audio strips in sequence based on order and text length
* import/export to csv file to save pitch/rate and voice options of individual strips
* export the audio clips generated by the tool in your timeline to closed captions files in .srt, .srb and .txt format
* export generates new timecodes based on audio strips starting frames
* caption data saved to blendfile

<a href="https://www.buymeacoffee.com/marcolinilA" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>


![alt text](https://github.com/technisculpt/blender-text-to-speech-offline/blob/main/ui_preview.png)

### Installation:
* To install zip the directory "Text to Speech" and install the addon via preferences menu
* This addon will install pyttsx3 to your Blender python interpreter
* Linux users must open a terminal and type:

```sudo apt install -y espeak ffmpeg libespeak1```
* Windows users will need to open Blender as administrator for install only
* May not work on OSX for Blender versions before 3.0.1

[![youtube intro video](https://github.com/technisculpt/blender-text-to-speech-offline/blob/main/youtube.PNG)](https://www.youtube.com/watch?v=dB4xzx1406I)

## Voice options differ depending on OS:
### Windows:
* David - Male - English (US)
* Zira - Female - English (US)

### OSX:
* Alex - Male - English (US)
* Alice - Female - Italiano (Italia)
* Alva - Female - Svenska (Sverige)
* Amelie - Female - Français (Canada)
* Anna - Female - Deutsch (Deutschland)
* Carmit - Female - עברית (ישראל)
* Damayanti - Female - Indonesia (Indonesia)
* Daniel - Male - English (United kingdom)
* Diego - Male - Español (Argentina)
* Ellen - Female - Nederlands (België)
* Fiona - Female - En-Scotland
* Fred - Male - English (United States)
* Ioana - Female - Română (România)
* Joana - Female - Português (Portugal)
* Jorge - Male - Español (España)
* Juan - Male - Español (México)
* Kanya - Female - ไทย (ไทย)
* Karen - Female - English (Australia)
* Kyoko - Female - 日本語 (日本)
* Laura - Female - Slovenčina (Slovensko)
* Lekha - Female - हिन्दी (भारत)
* Luca - Male - Italiano (Italia)
* Luciana - Female - Português (Brasil)
* Maged - Male - العربية (المملكة العربية السعودية)
* Mariska - Female - Magyar (Magyarország)
* Mei-jia - Female - Zh_tw
* Melina - Female - Ελληνικά (ελλάδα)
* Milena - Female - Русский (Pоссия)
* Moira - Female - English (Ireland)
* Monica - Female - Español (España)
* Nora - Female - Norsk Bokmål (Norge)
* Paulina - Female - Español (México)
* Rishi - Male - English (India)
* Samantha - Female - English (United States)
* Sara - Female - Dansk (Danmark)
* Satu - Female - Suomi (Suomi)
* Sin-ji - Female - Zh_hk
* Tessa - Female - English (South Africa)
* Thomas - Male - Français (France)
* Ting-ting - Female - Zh_cn
* Veena - Female - English (India)
* Victoria - Female - English (United States)
* Xander - Male - Nederlands (Nederland)
* Yelda - Female - Türkçe (Türkiye)
* Yuna - Female - 한국어 (대한민국)
* Yuri - Male - Русский (Pоссия)
* Zosia - Female - Polski (Polska)
* Zuzana - Female - Čeština (česko)

### Linux:
* Afrikaans - Male
* Aragonese - Male
* Bulgarian - Male
* Bosnian - Male
* Catalan - Male
* Czech - Male
* Welsh - Male
* Danish - Male
* German - Male
* Greek - Male
* Default - Male
* English - Male
* En-scottish - Male
* English-north - Male
* English_rp - Male
* English_wmids - Male
* English-us - Male
* En-westindies - Male
* Esperanto - Male
* Spanish - Male
* Spanish-latin-am - Male
* Estonian - Male
* Persian - Male
* Persian-pinglish - Male
* Finnish - Male
* French-belgium - Male
* French - Male
* Irish-gaeilge - Male
* Greek-ancient - Male
* Hindi - Male
* Croatian - Male
* Hungarian - Male
* Armenian - Male
* Armenian-west - Male
* Indonesian - Male
* Icelandic - Male
* Italian - Male
* Lojban - Male
* Georgian - Male
* Kannada - Male
* Kurdish - Male
* Latin - Male
* Lingua_franca_nova - Male
* Lithuanian - Male
* Latvian - Male
* Macedonian - Male
* Malayalam - Male
* Malay - Male
* Nepali - Male
* Dutch - Male
* Norwegian - Male
* Punjabi - Male
* Polish - Male
* Brazil - Male
* Portugal - Male
* Romanian - Male
* Russian - Male
* Slovak - Male
* Albanian - Male
* Serbian - Male
* Swedish - Male
* Swahili-test - Male
* Tamil - Male
* Turkish - Male
* Vietnam - Male
* Vietnam_hue - Male
* Vietnam_sgn - Male
* Mandarin - Male
* Cantonese - Male
