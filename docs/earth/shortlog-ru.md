# Описание файла shortlog.xml для симулятора Орбита 2.0

Перечень параметров файла вывода в формате shortlog.xml:

* **probe** - название аппарата;
* **tournament** - уникальный идентификатор турнира;
* **planet** - планета (Earth)
* **mission** - тип миссии:
  * dzz - Дистанционное зондирование Земли;
  * inspect - Инспекция спутника;
  * sms - SMS везде;
  * telecom - Связь с геостационарной орбиты;
  * crystal - Белковый кристалл;
* **flight_time** - продолжительность миссии (с);
* **ground_centers** - набор точек, задающие положение наземных измерительных пунктов (м);
* **data** - массив данных, описывающих полет аппарата;
* **status** - результат полета:
  * completed - Миссия завершена успешно;
  * failed - Миссия завершена неудачно;
  * notelemetry - Судьба миссии неизвеста, поскольку на Земле не удалось установить связь с аппаратом;
* **events** - массив событий для каждого этапа симулятора. первая строка - формат описания событий. Возможные события:
  * engine on - включение двигателя;
  * engine off - выключение двигателя;
  * radio on - включение радиопередатчика;
  * radio off - выключение радиопередатчика;
  * load on - включение полезной нагрузки;
  * load off - выключение полезной нагрузки;
  * dark side - вход аппарата в тень Земли;
  * light side - выход аппарата в освещенное пространство;
  * atmosphere on - вход аппарата в атмосферу;
  * atmosphere off - выход аппарата из атмосферы;
  * dead - выход аппарата из строя (перегрев, ошибка программы и т.п.);
  * crushed - разрушение аппарата о поверхность или в атмосфере;
* **limits** - стандартное ограничения пространста полетов аппаратов (аппарат в норме не может подняться выше этого уровня, но теоретически может):
  * min x, max x - по горизонтали (м);
  * min y, max y - по вертикали (м);
**target_data** - массив данных, описывающих положение цели (если она есть);
**target_orbit** - высота целевой орбиты (м).
