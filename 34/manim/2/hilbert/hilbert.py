from point_turtle import PointTurtle


def draw_curve(turtle: PointTurtle, depth: int):
    if depth == 0:
        return
    
    turtle.left()

    turtle.flip()
    draw_curve(turtle, depth - 1)
    turtle.flip()

    turtle.forward()
    turtle.right()

    draw_curve(turtle, depth - 1)

    turtle.forward()

    draw_curve(turtle, depth - 1)

    turtle.right()
    turtle.forward()

    turtle.flip()
    draw_curve(turtle, depth - 1)
    turtle.flip()

    turtle.left()
    

def generate_curve(depth: int) -> tuple[int, int]:
    turtle = PointTurtle()

    draw_curve(turtle, depth)

    return turtle.points
