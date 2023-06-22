#let image = rect(width: 5cm, height: 3.5cm, inset: 0mm, stroke: none)[
    #place(polygon(
        fill: blue,
        (1cm, 0.5cm), (4cm, 2cm),
        (4cm, 3.5cm), (1cm, 3.5cm)
    ))
    #place(line(
        start: (1cm, 0.5cm),
        end: (4cm, 2cm),
        stroke: 1mm
    ))
    #place(
        dx: 1cm - 1.5mm,
        dy: 0.5cm - 1.5mm,
        circle(radius: 1.5mm, fill: black)
    )
    #place(
        dx: 4cm - 1.5mm,
        dy: 2cm - 1.5mm,
        circle(radius: 1.5mm, fill: black)
    )
]
