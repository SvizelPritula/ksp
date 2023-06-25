#set document(
    title: "35-5-S - Obsah mnohoúhelníku",
    author: "Benjamin Swart"
)
#set page("a4", numbering: "1")
#set text(lang: "cs")
#set par(justify: true)

#import "images/area.typ"
#import "images/lines.typ"
#import "visualize.typ": area_diagram

Projdeme všechny orientované úsečky mnohoúhelníka, buď po nebo proti směru hodinových ručiček, a spočítáme obsah plochy pod každou z nich.
Obsahy pod úsečkami vedoucími doprava sečteme, obsah pod úsečkami vedoucími doleva od součtu odečteme.

#figure(
    area.image,
    caption: "Plocha pod úsečkou"
) <area>

Obsah plochy (viz @area[obrázek]) pod úsečkou s vrcholy $(x_1, y_1)$ a $(x_2, y_2)$ vypočítáme pomocí vzorce $A = 1 / 2 (x_2 - x_1) (y_1 + y_2)$.
Jedná se o vzorec pro obsah obdélníka, do kterého byla dosazena průměrná výška plochy.
Tím získáme orientovaný obsah plochy pod touto úsečkou, který bude kladný tehdy, kdy bude druhý bod napravo od prvního.

Tyto orientované obsahy prostě sečteme.
V závislosti na tom, jestli jsme body procházeli po nebo proti směru hodinových ručiček, nám vyjde buď obsah našeho mnohoúhelníku, nebo hodnota obsahu opačná.
Vezmeme tedy absolutní hodnotu výsledku a získáme řešení.

Algoritmus využívá jednoduchého pozorování.
Podívejme se pro daný bod na rozdíl počtu úseček vedoucími nad ním doprava a doleva. 
Každý bod uvnitř mnohoúhelníku má nad sebou o jednu více úsečku procházející doprava, zatímco bod mimo mnohoúhelník má nad sebou obou druhů úseček stejně.
Například bod $x$ na @lines[obrázku] je uvnitř mnohoúhelníka a má nad sebou dvě úsečky vedoucí doprava a jen jednu vedoucí doleva, zatímco bod $y$ má od každé jednu.

#figure(
    lines.image,
    caption: "Bod uvnitř a vně mnohoúhleníku"
) <lines>

Obsahy ploch pod úsečkami budou záviset na zvolené ose $x$, ale celkový součet to neovlivní.
Pokud osu $x$ posuneme dolu o $Delta y$, tak ke každému obsahu přičteme $Delta y (x_2 - x_1)$.
Součet rozdílů po sobě jdoucích souřadnic $x$ bude zjevně nulový, protože začínáme a končíme ve stejném bodě.

Na @trace[obrázku] je znázorněn běh tohoto algoritmu. Modře je vyznačena aktuálně sečtená plocha, zeleně a červeně jsou označeny přičítané a odčítané plochy.

Tento algoritmus poběží v čase $cal(O)(n)$. Paměti mu stačí $cal(O)(1)$, pokud může číst souřadnice bodů postupně.

#{
    let points = (
        (1, 1),
        (6, 3),
        (11, 1),
        (17, 5),
        (12, 4),
        (10, 6),
        (19, 9),
        (15, 13),
        (12, 9),
        (8, 9),
        (13, 12),
        (6, 10),
        (3, 11),
    );

    let width = 20;
    let height = 16;

    let cells = ();

    for step in range(points.len() + 2) {
        cells.push(stack(
            dir: ltr,
            text(size: 1.2em)[#{step + 1}.],
            h(0.8em),
            area_diagram(points, step, width, height, 2mm)
        ));
    }

    [#figure(
        grid(
            columns: (1fr, 1fr, 1fr),
            gutter: 3mm,
            ..cells
        ),
        caption: "Průběh programu"
    ) <trace>]
}
