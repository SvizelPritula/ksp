#set document(
    title: "35-5-S - Součin",
    author: "Benjamin Swart"
)
#set page("a4")
#set text(lang: "cs")
#set par(justify: true)

Z předchozího odstavce se dozvídáme, že pro každé lineární zobrazení $T$ vyjadřuje jeho determinant $det T$ poměr mezi obsahem tělesa a obsahem obrazu tělesa.
Pokud mělo těleso původně obsah $a$, obsah obrazu bude $a det T$.
Pokud máme dvě lineární zobrazení $A$ a $B$, tak $A B$ představuje zobrazení vzniklé tím, že nejprve provedeme zobrazení $B$ a poté $A$.
Obsah obrazu tělesa toto zobrazení změní stejně, jako bychom aplikovali obě zobrazení postupně, tedy se nejprve zvětší $det B$ krát a poté $det A$ krát.
Determinant $det(A B)$ tedy musí být rovný $det A det B$.
