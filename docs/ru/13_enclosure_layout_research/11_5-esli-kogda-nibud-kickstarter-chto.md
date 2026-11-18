> Часть документа 13 ([индекс](../13_enclosure_layout_research.md)): 5. Если когда-нибудь Kickstarter: что решать уже сейчас

## 5. Если когда-нибудь Kickstarter: что решать уже сейчас

Ты делаешь устройство для себя, но допускаешь краудфандинг. Несколько решений дешевле принять сразу, чем потом переделывать.

| Тема | Факт | Вывод |
|---|---|---|
| Лицензии кода | Код Kick — AGPL-3.0 ([GitHub](https://github.com/MusicTribeOpenSource/0700-AAM/blob/main/README.md)); JUCE — AGPLv3 или коммерческая ([Wikipedia](https://en.wikipedia.org/wiki/JUCE)); Ableton Link — GPLv2+ или проприетарная ([GitHub](https://www.Github.com/Ableton/link)) | Если берём код Kick или JUCE по AGPL, наша прошивка тоже должна быть открытой. Решить заранее: открытый проект или закрытый |
| Долгая доступность | CM5 выпускают минимум до января 2036 года ([CM5 brief](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008181-DS-10-cm5-product-brief.pdf)) | Выбирать компоненты с объявленным сроком выпуска |
| Радио | Wi-Fi и Bluetooth требуют радио-сертификации (Директива ЕС RED) | Только готовые сертифицированные модули |
| Аккумулятор | ЕС: с 18.02.2027 батарея снимается и меняется пользователем, запчасти 5 лет ([ComplianceGate](https://www.compliancegate.com/removable-and-replaceable-battery-requirements-european-union/)) | Съёмный модуль (документ 11) |
| Питание от сети | — | Внешний сертифицированный блок или USB-C PD, чтобы не сертифицировать сетевую часть самим |
| Деньги | Краудфандинг подходит, чтобы проверить спрос и выпустить продукт, но доходом становится только при очень большом успехе ([Hackaday](https://hackaday.com/2021/09/12/successfully-crowdfunded-hardware-everything-behind-the-scenes)); Aodyo с синтами Loom Omega оказалась на грани банкротства, производство встало ([Synthtopia](https://www.synthtopia.com/content/2024/09/26/aodyo-says-production-of-loom-omega-synths-in-limbo-bankruptcy-coming-if-they-cant-raise-additional-funds/)) | Сначала рабочий прототип и видео, потом кампания |
| Видео | ШИМ WS2812 мерцает на камере (документ 10) | Матричные драйверы светодиодов |
