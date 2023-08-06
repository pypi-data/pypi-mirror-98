from robotjes import Robo


def execute(robo: Robo):
    robo.right(2)
    robo.paintWhite()
    while robo.frontIsClear():
        robo.forward()
    robo.left()
    while not robo.frontIsBeacon():
        robo.forward()
    robo.pickUp()
    robo.stopPainting()
