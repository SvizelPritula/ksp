#let area_diagram(points, step, width, height, scale) = {
    let width = width * scale;
    let height = height * scale;

    let points = points.map(((x, y)) => (x * scale, y * scale));

    box(
        width: width,
        height: height,
        inset: 0pt
    )[
        #if step >= points.len() + 1 {
            place(polygon(fill: blue, ..points))
        } else if step > 0 {
            let from = points.at(step - 1);
            let to = points.at(calc.rem(step, points.len()));

            let right = from.at(0) < to.at(0);

            let under = if step >= points.len() {
                points
            } else if right {
                points.slice(0, step)
            } else {
                points.slice(0, step + 1)
            }

            if under.len() >= 2 {
                if step < points.len() {
                    under.push((under.last().at(0), height));
                    under.push((under.at(0).at(0), height));
                }

                place(polygon(fill: blue, ..under))
            }

            let change = (
                from,
                to,
                (to.at(0), height),
                (from.at(0), height),
            );

            let color = if right { green } else { red };

            place(polygon(fill: color, ..change))
        }

        #place[#polygon(stroke: 0.2mm + black, ..points)]

        #for (x, y) in points {
            let radius = 0.5mm;

            place(
                dx: x - radius,
                dy: y - radius,
                circle(radius: radius, fill: black, stroke: none)
            )
        }
    ]
}
