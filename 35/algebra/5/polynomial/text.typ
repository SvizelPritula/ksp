#set page("a4", numbering: "1")
#set text(lang: "cs")
#set par(justify: true)

Hledaný polynom můžeme vyjádřit ve tvaru $a x^2 + b x + c = 0$.
Hledáme koeficienty $a$, $b$ a $c$.
Snažíme se tedy vyřešit tuto soustavu rovnic:

$
    a x_0^2 + b x_0 + c &= y_0 \
    a x_1^2 + b x_1 + c &= y_1 \
    a x_2^2 + b x_2 + c &= y_2 \
$

Tuto soustavu můžeme zapsat pomocí matice:

$ mat(
    x_0^2, x_0, 1;
    x_1^2, x_1, 1;
    x_2^2, x_2, 1;
) vec(a, b, c) = vec(y_0, y_1, y_2) $

Tuto matici označíme $A$.
Tato rovnice bude mít jednoznačné řešení právě tehdy, když jsou řádky matice $A$ lineárně nezávislé.

Lineární nezávislost těchto tří vektorů dokážeme sporem.
Předpokládejme, že jsou tyto tři vektory lineárně závislé.
To znamená, že jeden z nich je možné vyjádřit jako lineární kombinaci zbylých dvou.
Vlastnosti, že $x_0 < x_1 < x_2$, budeme využívat jen z části.
Bude nám stačit to, že jsou všechny hodnoty $x$ navzájem různé.
Teď všechny tři vektory zastávají ekvivalentní role, takže můžeme bez ztráty na obecnosti předpokládat, že je možné jako lineární kombinaci ostatních vyjádřit právě třetí řádek.
Získáme soustavu rovnic:

$
    a x_0^2 + b x_1^2 &= x_2^2 \
    a x_0 + b x_1 &= x_2 \
    a + b &= 1 \
$

Snadno můžeme $b$ vyjádřit jako $1 - a$ a tento člen dosadit do druhé rovnice.

$

    a x_0 + (1 - a) x_1 &= x_2 \
    a x_0 + x_1 - a x_1 &= x_2 \
    a (x_0 - x_1) &= x_2 - x_1 \
$

Víme, že $x_0 != x_1$, takže můžeme rovnici vydělit $x_0 - x_1$.

$
    a = (x_2 - x_1) / (x_0 - x_1)
$

Podobně můžeme postupovat s první rovnicí.

$
    a x_0^2 + (1 - a) x_1^2 = x_2^2 \
    a x_0^2 + x_1^2 - a x_1^2 = x_2^2 \
    a (x_0^2 - x_1^2) = x_2^2 - x_1^2 \
$

Tuto rovnici můžeme vydělit $x_0^2 - x_1^2$ za předpokladu, že $x_0^2 != x_1^2$.
Kdyby tomu tak bylo, mohli bychom první rovnici upravit do této podoby:

$
    a x_0^2 + b x_0^2 &= x_2^2 \
    x_0^2 (a + b) &= x_2^2 \
    x_0^2 &= x_2^2 \
$

To by znamenalo, že $abs(x_0) = abs(x_1) = abs(x_2)$.
Neexistují tři různá reálná čísla se stejnou absolutní hodnotou.
To znamená, že můžeme rovnici vydělit $x_0^2 - x_1^2$.
Získáme druhou rovnici s $a$ na levé straně.
Jednu definici $a$ dosadíme do druhé a získáme rovnici bez $a$ a $b$.

$
    a = (x_2^2 - x_1^2) / (x_0^2 - x_1^2) \
    (x_2^2 - x_1^2) / (x_0^2 - x_1^2) = (x_2 - x_1) / (x_0 - x_1) \
$

Využijeme toho, že $a^2 - b^2 = (a + b)(a - b)$ a rovnici vydělíme její pravou stranou.
To můžeme udělat, protože ani čitatel ani jmenovatel zlomku na pravé straně nemůže být nulový.

$
    ((x_2 - x_1) (x_2 + x_1)) / ((x_0 - x_1) (x_0 + x_1)) = (x_2 - x_1) / (x_0 - x_1) \

    (x_2 + x_1) / (x_0 + x_1) = 1 \
$

Provedeme pár prostých úprav:

$
    x_2 + x_1 = x_0 + x_1 \
    x_2 = x_0 \
$

Došli jsme k závěru, že $x_0 = x_2$, což odporuje našim předpokladům.
Dosáhli jsme tedy sporu, což znamená, že musí být řádky $A$ nezávislé.
To znamená, že vždy existuje jednoznačné řešení.
