#let points = (
    (10mm, 4mm),
    (35mm, 12mm),
    (15mm, 20mm),
    (35mm, 28mm),
    (10mm, 36mm),
    (5mm, 20mm),
);

#let image = rect(width: 4cm, height: 4cm, inset: 0mm, stroke: none)[
    #place(polygon(
        fill: blue.lighten(20%),
        ..points
    ))

    #for i in range(points.len()) {
        let a = points.at(i);
        let b = points.at(calc.rem(i + 1, points.len()));

        place(line(
            start: a,
            end: b,
            stroke: 1mm + if a.at(0) < b.at(0) {
                green
            } else {
                red
            }
        ))
    }

    #for (x, y) in points {
        place(
            dx: x - 1mm,
            dy: y - 1mm,
            circle(radius: 1mm, fill: black)
        )
    }

    #place(
        dx: 25mm - 1mm,
        dy: 28mm - 1mm,
        circle(radius: 1mm, fill: black)
    )

    #place(
        dx: 21mm,
        dy: 27mm,
    )[$x$]

    #place(
        dx: 30mm - 1mm,
        dy: 20mm - 1mm,
        circle(radius: 1mm, fill: black)
    )
    
    #place(
        dx: 26mm,
        dy: 19mm,
    )[$y$]
]